import json
from pathlib import Path

import pytest
from filinglens.sec import normalize_cik, require_user_agent, fetch_companyfacts, revenue_observations


def test_cik_normalization():
    assert normalize_cik(320193) == "0000320193"
    with pytest.raises(ValueError):
        normalize_cik("../etc/passwd")
    with pytest.raises(ValueError):
        normalize_cik("12345678901")


def test_user_agent_required():
    with pytest.raises(ValueError):
        require_user_agent("FilingLens contact@example.com")
    assert require_user_agent("FilingLens analyst@legitimate.org") == "FilingLens analyst@legitimate.org"


def test_sort_and_preserve_provenance():
    payload = {"facts": {"us-gaap": {"RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [
        {"start": "2024-01-01", "end": "2024-03-31", "val": 10, "filed": "2024-04-15", "form": "10-Q", "accn": "0001"},
        {"start": "2023-01-01", "end": "2023-12-31", "val": 35, "filed": "2024-02-15", "form": "10-K", "accn": "0002"},
    ]}}}}}
    rows = revenue_observations(payload, limit=1)
    assert len(rows) == 1
    assert rows[0]["val"] == 10
    assert rows[0]["accn"] == "0001"


def test_cache_is_usable_offline_without_user_agent(tmp_path: Path):
    cache = tmp_path / "CIK0000320193.json"
    cache.write_text(json.dumps({"cik": 320193, "facts": {}, "entityName": "Example"}))
    assert fetch_companyfacts("320193", cache_dir=tmp_path)["entityName"] == "Example"


def test_revenue_rejects_bad_limit():
    with pytest.raises(ValueError):
        revenue_observations({"facts": {}}, limit=0)
