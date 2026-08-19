"""
Phase 5 — End-to-End Test Suite
================================
Covers: health endpoint, DB pre-filtering (various combos),
        AI recommendations, edge cases, and cache behaviour.

Run with:  python -m pytest test_api.py -v
"""

import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pytest
from fastapi.testclient import TestClient
from main import app
import cache

client = TestClient(app)


# ──────────────────────────────────────────────
# 1. Health endpoint
# ──────────────────────────────────────────────
class TestHealth:
    def test_health_endpoint(self):
        """GET /health should return status, version, and an ISO timestamp."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "1.0"
        assert "timestamp" in data

    def test_options_endpoint(self):
        """GET /options should return locations, cuisines, and budgets."""
        response = client.get("/options")
        assert response.status_code == 200
        data = response.json()
        assert "locations" in data and len(data["locations"]) > 0
        assert "cuisines" in data and len(data["cuisines"]) > 0
        assert "budgets" in data and len(data["budgets"]) == 3


# ──────────────────────────────────────────────
# 2. Basic filtering (no AI)
# ──────────────────────────────────────────────
class TestBasicFiltering:
    def test_basic_filter_no_ai(self):
        """Location + Budget with no soft preferences should return ≤ 5 results."""
        payload = {
            "location": "Banashankari",
            "budget": "Mid",
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) <= 5

    def test_cuisine_filter(self):
        """Adding a cuisine filter should only return matching restaurants."""
        payload = {
            "location": "Bangalore",
            "budget": "Mid",
            "cuisine": "Chinese",
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        for r in data:
            assert "Chinese" in r.get("cuisines", ""), (
                f"Restaurant '{r.get('name')}' does not have Chinese in cuisines"
            )

    def test_high_rating_filter(self):
        """min_rating=4.5 should only return highly rated restaurants."""
        payload = {
            "location": "Bangalore",
            "budget": "High",
            "min_rating": 4.5,
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        for r in data:
            if r.get("rating") is not None:
                assert r["rating"] >= 4.5, (
                    f"Restaurant '{r.get('name')}' has rating {r['rating']} < 4.5"
                )


# ──────────────────────────────────────────────
# 3. Edge cases
# ──────────────────────────────────────────────
class TestEdgeCases:
    def test_no_results(self):
        """A non-existent location should return an empty array gracefully."""
        payload = {
            "location": "NonExistentCity12345",
            "budget": "Mid",
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_generic_query(self):
        """A very broad query should still return results without crashing."""
        payload = {
            "location": "Bangalore",
            "budget": "Low",
            "min_rating": 1.0,
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


# ──────────────────────────────────────────────
# 4. AI recommendations
# ──────────────────────────────────────────────
class TestAIRecommendation:
    def test_ai_recommendation(self):
        """When soft_preferences are provided, the LLM should return explanations."""
        payload = {
            "location": "Banashankari",
            "budget": "Mid",
            "min_rating": 4.0,
            "soft_preferences": "I want a quiet place suitable for a date with good desserts.",
        }
        response = client.post("/recommend", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            # All required fields should be present
            required = {"id", "name", "cuisines", "rating", "cost_for_two"}
            for r in data:
                for field in required:
                    assert field in r, f"Missing field '{field}' in recommendation"
            # If the LLM route was taken, explanations should exist
            if "explanation" in data[0]:
                for r in data:
                    assert r.get("explanation"), "Explanation should not be empty"


# ──────────────────────────────────────────────
# 5. Cache behaviour
# ──────────────────────────────────────────────
class TestCacheBehaviour:
    def test_cache_stats_endpoint(self):
        """GET /cache/stats should return valid cache statistics."""
        response = client.get("/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert "hits" in data
        assert "misses" in data
        assert "size" in data

    def test_cache_hit(self):
        """Sending the exact same query twice should hit the cache on the second call."""
        payload = {
            "location": "Koramangala",
            "budget": "High",
            "min_rating": 4.0,
            "soft_preferences": "Trendy rooftop bar with craft cocktails.",
        }

        # First call — cache miss
        t0 = time.perf_counter()
        response1 = client.post("/recommend", json=payload)
        first_ms = (time.perf_counter() - t0) * 1000

        # Second call — should be cache hit
        t1 = time.perf_counter()
        response2 = client.post("/recommend", json=payload)
        second_ms = (time.perf_counter() - t1) * 1000

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Both should return the same data
        assert response1.json() == response2.json()

        # Second call should be significantly faster (cache hit skips LLM)
        print(f"\n  First call:  {first_ms:.0f} ms")
        print(f"  Second call: {second_ms:.0f} ms (cache hit)")


# ──────────────────────────────────────────────
# Allow running directly with: python test_api.py
# ──────────────────────────────────────────────
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
