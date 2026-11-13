from filinglens.finance import annual_revenue,growth,compare_annual
from filinglens.filings import recent_filings
import pytest

def test_growth():
    assert growth(100,125)==25
    assert growth(0,10) is None

def test_annual_selection_no_duplicate_period():
    items=[
        {"start":"2024-01-01","end":"2024-12-31","val":100,"form":"10-K","filed":"2025-02-01","accn":"0001"},
        {"start":"2024-01-01","end":"2024-12-31","val":110,"form":"10-K","filed":"2025-03-01","accn":"0002"},
        {"start":"2025-01-01","end":"2025-12-31","val":121,"form":"10-K","filed":"2026-02-01","accn":"0003"},
        {"start":"2025-01-01","end":"2025-06-30","val":50,"form":"10-Q","filed":"2025-07-01","accn":"0004"}
    ]
    payload={"cik":320193,"facts":{"us-gaap":{"Revenues":{"units":{"USD":items}}}}}
    selected=annual_revenue(payload)
    assert len(selected)==2
    assert selected[0].value==110
    assert compare_annual(selected)[0]["growth_pct"]==10

def test_filing_urls_and_alignment():
    d={"cik":320193,"filings":{"recent":{"form":["8-K","10-K"],"filingDate":["2026-01-01","2025-10-31"],"reportDate":["2025-12-31","2025-09-27"],"accessionNumber":["0000320193-26-000001","0000320193-25-000079"],"primaryDocument":["a.htm","aapl-20250927.htm"]}}}
    result=recent_filings(d)
    assert len(result)==1
    assert result[0]["filingDate"]=="2025-10-31"
    assert result[0]["document_url"].endswith("/000032019325000079/aapl-20250927.htm")

def test_misaligned_arrays_rejected():
    d={"cik":1,"filings":{"recent":{"form":["10-K"],"filingDate":[],"reportDate":["x"],"accessionNumber":["x"],"primaryDocument":["x"]}}}
    with pytest.raises(ValueError):
        recent_filings(d)
