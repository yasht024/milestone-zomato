import hashlib
import json
import threading
import time
from typing import Any, Dict, Optional

# ---------- Configuration ----------
CACHE_TTL_SECONDS = 600   # 10 minutes
CACHE_MAX_SIZE = 100       # Maximum cached entries

# ---------- Internal Storage ----------
_cache: Dict[str, Dict[str, Any]] = {}
_lock = threading.Lock()
_stats = {"hits": 0, "misses": 0}


def _make_key(location: str, budget: str, cuisine: Optional[str],
              min_rating: Optional[float], soft_preferences: Optional[str]) -> str:
    """Generate a deterministic hash key from the normalised request parameters."""
    raw = json.dumps({
        "location": (location or "").strip().lower(),
        "budget": (budget or "").strip().lower(),
        "cuisine": (cuisine or "").strip().lower(),
        "min_rating": min_rating,
        "soft_preferences": (soft_preferences or "").strip().lower(),
    }, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def get(location: str, budget: str, cuisine: Optional[str],
        min_rating: Optional[float], soft_preferences: Optional[str]) -> Optional[Any]:
    """Return cached result if it exists and hasn't expired, else None."""
    key = _make_key(location, budget, cuisine, min_rating, soft_preferences)
    with _lock:
        entry = _cache.get(key)
        if entry is None:
            _stats["misses"] += 1
            return None
        if time.time() - entry["timestamp"] > CACHE_TTL_SECONDS:
            # Expired — evict
            del _cache[key]
            _stats["misses"] += 1
            return None
        _stats["hits"] += 1
        return entry["data"]


def put(location: str, budget: str, cuisine: Optional[str],
        min_rating: Optional[float], soft_preferences: Optional[str],
        data: Any) -> None:
    """Store a result in the cache, evicting oldest entry if at capacity."""
    key = _make_key(location, budget, cuisine, min_rating, soft_preferences)
    with _lock:
        # Evict oldest entry if we're at max capacity
        if len(_cache) >= CACHE_MAX_SIZE and key not in _cache:
            oldest_key = min(_cache, key=lambda k: _cache[k]["timestamp"])
            del _cache[oldest_key]
        _cache[key] = {"data": data, "timestamp": time.time()}


def get_stats() -> Dict[str, Any]:
    """Return cache statistics for observability."""
    with _lock:
        return {
            "size": len(_cache),
            "max_size": CACHE_MAX_SIZE,
            "ttl_seconds": CACHE_TTL_SECONDS,
            "hits": _stats["hits"],
            "misses": _stats["misses"],
            "hit_rate": (
                round(_stats["hits"] / (_stats["hits"] + _stats["misses"]), 3)
                if (_stats["hits"] + _stats["misses"]) > 0
                else 0.0
            ),
        }
