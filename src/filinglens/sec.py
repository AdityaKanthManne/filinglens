"""Minimal, cached SEC company-facts client using only the Python standard library."""
from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SEC_BASE = "https://data.sec.gov/api/xbrl/companyfacts"
USER_AGENT_PATTERN = re.compile(r"^.{3,}\s+[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_cik(cik: str | int) -> str:
    value = str(cik).strip()
    if not value.isdigit() or len(value) > 10:
        raise ValueError("CIK must contain 1–10 digits")
    return value.zfill(10)


def require_user_agent(value: str | None = None) -> str:
    agent = (value if value is not None else os.getenv("SEC_USER_AGENT", "")).strip()
    if not USER_AGENT_PATTERN.match(agent) or "example.com" in agent.lower():
        raise ValueError("Set SEC_USER_AGENT to 'AppName your-real-email@domain.com' before fetching SEC data")
    return agent


def fetch_companyfacts(cik: str | int, *, cache_dir: Path | str = ".cache/sec", user_agent: str | None = None, max_age_seconds: int = 86400) -> dict:
    """Fetch SEC Company Facts with on-disk cache and request spacing.

    The SEC generally allows up to 10 requests/sec; use a much slower client-side pace.
    """
    cik = normalize_cik(cik)
    cache_path = Path(cache_dir) / f"CIK{cik}.json"
    if cache_path.is_file() and time.time() - cache_path.stat().st_mtime <= max_age_seconds:
        return json.loads(cache_path.read_text(encoding="utf-8"))

    agent = require_user_agent(user_agent)
    request = Request(f"{SEC_BASE}/CIK{cik}.json", headers={
        "User-Agent": agent,
        "Accept": "application/json",
        "Accept-Encoding": "identity",
    })
    # A single call per CLI invocation; don't issue concurrent SEC requests.
    time.sleep(0.2)
    try:
        with urlopen(request, timeout=25) as response:
            data = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"SEC returned HTTP {exc.code} for CIK {cik}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach SEC API: {exc.reason}") from exc
    if not isinstance(data, dict) or "facts" not in data or "cik" not in data:
        raise ValueError("SEC response did not contain expected company facts fields")
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    temp = cache_path.with_suffix(".tmp")
    temp.write_text(json.dumps(data), encoding="utf-8")
    temp.replace(cache_path)
    return data


def revenue_observations(data: dict, *, concept: str = "RevenueFromContractWithCustomerExcludingAssessedTax", limit: int = 10) -> list[dict]:
    """Return raw reported USD observations; no inference or period normalization."""
    if limit < 1:
        raise ValueError("limit must be positive")
    concept_data = data.get("facts", {}).get("us-gaap", {}).get(concept, {})
    observations = concept_data.get("units", {}).get("USD", [])
    selected = sorted(observations, key=lambda x: (x.get("filed", ""), x.get("end", "")), reverse=True)[:limit]
    return [{key: entry.get(key) for key in ("start", "end", "val", "form", "fy", "fp", "frame", "filed", "accn")} for entry in selected]
