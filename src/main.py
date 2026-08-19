import os
import time
import logging
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Union

from database import SessionLocal, Restaurant
from schemas import RecommendationRequest, RestaurantResponse, AIRecommendationResponse
from llm_service import get_ai_recommendations
import cache

# ──────────────────────────────────────────────
# Logging setup
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger("api")

app = FastAPI(title="Zomato Restaurant Recommendation API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust for production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    """Root endpoint for service discovery and health ping."""
    return {
        "service": "Zomato Restaurant Recommendation API",
        "status": "healthy",
        "docs_url": "/docs",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
def health_check():
    """Returns the health status of the API."""
    return {
        "status": "healthy",
        "version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/cache/stats")
def cache_stats():
    """Returns current cache statistics for observability."""
    return cache.get_stats()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/options")
def get_filter_options(db: Session = Depends(get_db)):
    """Returns unique locations and cuisines available in the database."""
    # Distinct locations
    raw_locs = db.query(Restaurant.location).distinct().filter(Restaurant.location != None).all()
    locations = sorted([loc[0].strip() for loc in raw_locs if loc[0] and loc[0].strip()])

    # Distinct cuisines
    raw_cuisines = db.query(Restaurant.cuisines).distinct().filter(Restaurant.cuisines != None).all()
    cuisine_set = set()
    for row in raw_cuisines:
        if row[0]:
            for c in row[0].split(","):
                cleaned = c.strip()
                if cleaned:
                    cuisine_set.add(cleaned)
    cuisines = sorted(list(cuisine_set))

    return {
        "locations": locations,
        "cuisines": cuisines,
        "budgets": ["Low", "Mid", "High"],
    }

@app.post("/recommend", response_model=Union[List[AIRecommendationResponse], List[RestaurantResponse]])
def recommend_restaurants(request: RecommendationRequest, db: Session = Depends(get_db)):
    # ── Check cache first ──────────────────────────────────
    cached = cache.get(
        request.location, request.budget,
        request.cuisine, request.min_rating,
        request.soft_preferences,
    )
    if cached is not None:
        logger.info("Cache HIT — returning %d cached results", len(cached))
        return cached

    # ── Database pre-filtering ─────────────────────────────
    t0 = time.perf_counter()

    query = db.query(Restaurant)

    # Apply strict filters
    # 1. Location (case-insensitive substring)
    if request.location:
        query = query.filter(Restaurant.location.ilike(f"%{request.location}%"))
        
    # 2. Budget Tier (case-insensitive exact match)
    if request.budget:
        query = query.filter(Restaurant.budget_tier.ilike(request.budget))
        
    # 3. Cuisine (case-insensitive substring)
    if request.cuisine:
        query = query.filter(Restaurant.cuisines.ilike(f"%{request.cuisine}%"))
        
    # 4. Minimum Rating
    if request.min_rating is not None:
        query = query.filter(Restaurant.rating >= request.min_rating)
        
    # Order by rating descending and limit to top 30
    results = query.order_by(Restaurant.rating.desc()).limit(30).all()

    db_ms = (time.perf_counter() - t0) * 1000
    logger.info("DB query returned %d results in %.1f ms", len(results), db_ms)

    # Serialize results to dictionaries for LLM injection
    serialized_results = [
        {
            "id": r.id,
            "name": r.name,
            "location": r.location,
            "budget_tier": r.budget_tier,
            "rating": r.rating,
            "cost_for_two": r.cost_for_two,
            "cuisines": r.cuisines,
            "features": r.features
        } for r in results
    ]
    
    # ── LLM inference (if soft preferences are provided) ───
    if request.soft_preferences and serialized_results:
        t1 = time.perf_counter()
        # Pass only top 10 to avoid payload size limits
        ai_recs = get_ai_recommendations(request.soft_preferences, serialized_results[:10])
        llm_ms = (time.perf_counter() - t1) * 1000
        logger.info("LLM inference completed in %.1f ms — %d recommendations", llm_ms, len(ai_recs))

        if ai_recs:
            # Store in cache before returning
            cache.put(
                request.location, request.budget,
                request.cuisine, request.min_rating,
                request.soft_preferences,
                ai_recs,
            )
            return ai_recs
        
    # Fallback or if no soft preferences, return top 5
    final = serialized_results[:5]

    # Cache the fallback result too
    cache.put(
        request.location, request.budget,
        request.cuisine, request.min_rating,
        request.soft_preferences,
        final,
    )
    return final
