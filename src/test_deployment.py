import os
import pytest
from fastapi.testclient import TestClient
from main import app
import cache

client = TestClient(app)

class TestPhase4Verification:
    """
    Phase 4 Automated Verification Suite
    Validates all endpoints and workflows defined in deployment-plan.md Phase 4.
    """

    def test_01_backend_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "Zomato" in data["service"]

    def test_02_backend_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0"
        assert "timestamp" in data

    def test_03_backend_options_population(self):
        response = client.get("/options")
        assert response.status_code == 200
        data = response.json()
        assert "locations" in data and len(data["locations"]) > 0
        assert "cuisines" in data and len(data["cuisines"]) > 0
        assert "budgets" in data and len(data["budgets"]) == 3

    def test_04_strict_filtering_recommendation(self):
        payload = {
            "location": "Indiranagar",
            "budget": "Mid",
            "min_rating": 4.0
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Validate data structure
        first = data[0]
        assert "name" in first
        assert "rating" in first
        assert first["rating"] >= 4.0

    def test_05_soft_preferences_fallback_and_structure(self):
        payload = {
            "location": "Koramangala",
            "budget": "Mid",
            "min_rating": 3.8,
            "soft_preferences": "quiet romantic dinner place"
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_06_in_memory_cache_hit_performance(self):
        payload = {
            "location": "Indiranagar",
            "budget": "Mid",
            "cuisine": "North Indian",
            "min_rating": 4.0
        }
        # First request populates cache
        res1 = client.post("/recommend", json=payload)
        assert res1.status_code == 200

        # Second request must hit cache
        res2 = client.post("/recommend", json=payload)
        assert res2.status_code == 200
        assert res1.json() == res2.json()

        # Cache stats must record hits
        stats_res = client.get("/cache/stats")
        assert stats_res.status_code == 200
        stats = stats_res.json()
        assert stats["hits"] >= 1
