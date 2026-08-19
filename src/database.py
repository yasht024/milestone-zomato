import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Index
from sqlalchemy.orm import declarative_base, sessionmaker

from pathlib import Path

# Resolve path to zomato.db (prefer project root, fallback to current dir)
ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / "zomato.db" if (ROOT_DIR / "zomato.db").exists() else Path(__file__).resolve().parent / "zomato.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String, index=True)
    budget_tier = Column(String, index=True) # Will store things like 'low', 'mid', 'high'
    rating = Column(Float, index=True)
    cost_for_two = Column(Integer)
    cuisines = Column(String)
    features = Column(String) # To store combined features/reviews for soft filtering

    # Composite index for the most common filter combination (Phase 5 optimisation)
    __table_args__ = (
        Index("ix_location_budget_rating", "location", "budget_tier", "rating"),
    )

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
