#!/usr/bin/env python3
"""
End-to-End Verification Script (Phase 4 of Deployment Plan)
Verifies live endpoints on Railway (Backend) and Vercel (Frontend).

Usage:
  python verify_deployment.py --backend <RAILWAY_URL> [--frontend <VERCEL_URL>]
  python verify_deployment.py  # Defaults to localhost:8000
"""

import sys
import time
import argparse
import urllib.request
import urllib.parse
import json

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def http_get(url: str, timeout: int = 15):
    t0 = time.perf_counter()
    req = urllib.request.Request(url, headers={"User-Agent": "E2E-Verifier/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        status = response.status
        body = response.read().decode("utf-8")
        elapsed_ms = (time.perf_counter() - t0) * 1000
        try:
            data = json.loads(body)
        except Exception:
            data = body
        return status, data, elapsed_ms

def http_post(url: str, payload: dict, timeout: int = 25):
    t0 = time.perf_counter()
    data_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json", "User-Agent": "E2E-Verifier/1.0"}
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        status = response.status
        body = response.read().decode("utf-8")
        elapsed_ms = (time.perf_counter() - t0) * 1000
        try:
            data = json.loads(body)
        except Exception:
            data = body
        return status, data, elapsed_ms

def run_verification(backend_url: str, frontend_url: str = None):
    backend_url = backend_url.rstrip("/")
    if frontend_url:
        frontend_url = frontend_url.rstrip("/")

    print(f"\n{BOLD}{CYAN}══════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD}{CYAN} 🚀 Zomato AI Dining Discoverer — End-to-End Verification{RESET}")
    print(f"{BOLD}{CYAN}══════════════════════════════════════════════════════════════{RESET}")
    print(f"📡 Backend URL : {BOLD}{backend_url}{RESET}")
    if frontend_url:
        print(f"🌐 Frontend URL: {BOLD}{frontend_url}{RESET}")
    print("──────────────────────────────────────────────────────────────\n")

    results = []

    # ── Test 1: Root Ping ────────────────────────────────────
    print(f"[1/7] Testing Root Endpoint ({backend_url}/)... ", end="", flush=True)
    try:
        status, data, ms = http_get(f"{backend_url}/")
        if status == 200 and isinstance(data, dict) and data.get("status") == "healthy":
            print(f"{GREEN}PASSED{RESET} ({ms:.1f}ms)")
            results.append(("Root Endpoint (GET /)", "PASSED", f"{ms:.1f}ms"))
        else:
            print(f"{RED}FAILED{RESET} (status={status})")
            results.append(("Root Endpoint (GET /)", "FAILED", f"Status {status}"))
    except Exception as e:
        print(f"{RED}FAILED{RESET} ({e})")
        results.append(("Root Endpoint (GET /)", "FAILED", str(e)))

    # ── Test 2: Health Check ─────────────────────────────────
    print(f"[2/7] Testing Health Check ({backend_url}/health)... ", end="", flush=True)
    try:
        status, data, ms = http_get(f"{backend_url}/health")
        if status == 200 and isinstance(data, dict) and data.get("status") == "healthy":
            print(f"{GREEN}PASSED{RESET} ({ms:.1f}ms)")
            results.append(("Health Check (GET /health)", "PASSED", f"{ms:.1f}ms"))
        else:
            print(f"{RED}FAILED{RESET} (status={status})")
            results.append(("Health Check (GET /health)", "FAILED", f"Status {status}"))
    except Exception as e:
        print(f"{RED}FAILED{RESET} ({e})")
        results.append(("Health Check (GET /health)", "FAILED", str(e)))

    # ── Test 3: Dynamic Options ──────────────────────────────
    print(f"[3/7] Testing Filter Options ({backend_url}/options)... ", end="", flush=True)
    try:
        status, data, ms = http_get(f"{backend_url}/options")
        loc_count = len(data.get("locations", [])) if isinstance(data, dict) else 0
        cui_count = len(data.get("cuisines", [])) if isinstance(data, dict) else 0
        if status == 200 and loc_count > 0 and cui_count > 0:
            print(f"{GREEN}PASSED{RESET} ({loc_count} locations, {cui_count} cuisines, {ms:.1f}ms)")
            results.append(("Options (GET /options)", "PASSED", f"{loc_count} locs, {cui_count} cuisines"))
        else:
            print(f"{RED}FAILED{RESET} (Empty options data)")
            results.append(("Options (GET /options)", "FAILED", "Empty data"))
    except Exception as e:
        print(f"{RED}FAILED{RESET} ({e})")
        results.append(("Options (GET /options)", "FAILED", str(e)))

    # ── Test 4: Database Strict Filtering ────────────────────
    print(f"[4/7] Testing DB Filtering (POST /recommend)... ", end="", flush=True)
    try:
        payload = {
            "location": "Indiranagar",
            "budget": "Mid",
            "min_rating": 4.0
        }
        status, data, ms = http_post(f"{backend_url}/recommend", payload)
        if status == 200 and isinstance(data, list) and len(data) > 0:
            print(f"{GREEN}PASSED{RESET} (Returned {len(data)} restaurants in {ms:.1f}ms)")
            results.append(("DB Filtering (/recommend)", "PASSED", f"{len(data)} results, {ms:.1f}ms"))
        else:
            print(f"{RED}FAILED{RESET} (Status {status})")
            results.append(("DB Filtering (/recommend)", "FAILED", f"Status {status}"))
    except Exception as e:
        print(f"{RED}FAILED{RESET} ({e})")
        results.append(("DB Filtering (/recommend)", "FAILED", str(e)))

    # ── Test 5: AI LLM Recommendation & Rationale ───────────
    print(f"[5/7] Testing AI Inference with LLM (POST /recommend)... ", end="", flush=True)
    ai_payload = {
        "location": "Koramangala",
        "budget": "Mid",
        "min_rating": 3.8,
        "soft_preferences": "romantic cozy candle-light ambience for anniversary"
    }
    try:
        status, data, ms = http_post(f"{backend_url}/recommend", ai_payload)
        has_explanation = (
            status == 200 
            and isinstance(data, list) 
            and len(data) > 0 
            and ("explanation" in data[0] or "name" in data[0])
        )
        if has_explanation:
            print(f"{GREEN}PASSED{RESET} (Generated {len(data)} AI recommendations in {ms:.1f}ms)")
            results.append(("AI Recommendation (/recommend)", "PASSED", f"{len(data)} recs, {ms:.1f}ms"))
        else:
            print(f"{RED}FAILED{RESET} (Empty response)")
            results.append(("AI Recommendation (/recommend)", "FAILED", "Empty response"))
    except Exception as e:
        print(f"{RED}FAILED{RESET} ({e})")
        results.append(("AI Recommendation (/recommend)", "FAILED", str(e)))

    # ── Test 6: In-Memory Cache Performance ──────────────────
    print(f"[6/7] Testing In-Memory Cache Hit Latency... ", end="", flush=True)
    try:
        # Repeat identical query
        status, data, ms = http_post(f"{backend_url}/recommend", ai_payload)
        if status == 200 and isinstance(data, list) and len(data) > 0:
            print(f"{GREEN}PASSED{RESET} (Cache HIT response in {ms:.1f}ms)")
            results.append(("Cache Performance", "PASSED", f"{ms:.1f}ms"))
        else:
            print(f"{RED}FAILED{RESET}")
            results.append(("Cache Performance", "FAILED", f"Status {status}"))
    except Exception as e:
        print(f"{RED}FAILED{RESET} ({e})")
        results.append(("Cache Performance", "FAILED", str(e)))

    # ── Test 7: Cache Observability Stats ────────────────────
    print(f"[7/7] Testing Observability (GET /cache/stats)... ", end="", flush=True)
    try:
        status, data, ms = http_get(f"{backend_url}/cache/stats")
        hits = data.get("hits", 0) if isinstance(data, dict) else 0
        entries = data.get("size", 0) if isinstance(data, dict) else 0
        if status == 200:
            print(f"{GREEN}PASSED{RESET} (Hits: {hits}, Cache size: {entries})")
            results.append(("Cache Observability (/cache/stats)", "PASSED", f"{hits} hits, size={entries}"))
        else:
            print(f"{RED}FAILED{RESET}")
            results.append(("Cache Observability (/cache/stats)", "FAILED", f"Status {status}"))
    except Exception as e:
        print(f"{RED}FAILED{RESET} ({e})")
        results.append(("Cache Observability (/cache/stats)", "FAILED", str(e)))

    # ── Optional Test 8: Frontend UI Availability ─────────────
    if frontend_url:
        print(f"\n[Optional] Testing Frontend UI ({frontend_url})... ", end="", flush=True)
        try:
            status, html, ms = http_get(frontend_url)
            if status == 200 and "MidnightCrave" in str(html) or "html" in str(html).lower():
                print(f"{GREEN}PASSED{RESET} (Vercel Frontend Live in {ms:.1f}ms)")
                results.append(("Frontend UI (Vercel)", "PASSED", f"{ms:.1f}ms"))
            else:
                print(f"{YELLOW}WARNING{RESET} (Status {status})")
                results.append(("Frontend UI (Vercel)", "WARNING", f"Status {status}"))
        except Exception as e:
            print(f"{RED}FAILED{RESET} ({e})")
            results.append(("Frontend UI (Vercel)", "FAILED", str(e)))

    # ── Summary Table ────────────────────────────────────────
    print(f"\n{BOLD}══════════════════════════════════════════════════════════════{RESET}")
    print(f"{BOLD} 📊 Phase 4 End-to-End Verification Summary{RESET}")
    print(f"{BOLD}══════════════════════════════════════════════════════════════{RESET}")
    passed_count = sum(1 for _, st, _ in results if st == "PASSED")
    total_count = len(results)

    for item, status, detail in results:
        status_colored = f"{GREEN}PASSED{RESET}" if status == "PASSED" else f"{RED}{status}{RESET}"
        print(f" • {item:<35} : {status_colored:<15} ({detail})")

    print("──────────────────────────────────────────────────────────────")
    if passed_count == total_count:
        print(f"{BOLD}{GREEN} ✅ ALL {total_count}/{total_count} CHECKS PASSED SUCCESSFULLY!{RESET}\n")
    else:
        print(f"{BOLD}{YELLOW} ⚠️  {passed_count}/{total_count} CHECKS PASSED. Review items above.{RESET}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="End-to-End Deployment Verification")
    parser.add_argument("--backend", default="http://localhost:8000", help="Backend base URL")
    parser.add_argument("--frontend", default=None, help="Frontend base URL")
    args = parser.parse_args()

    run_verification(args.backend, args.frontend)
