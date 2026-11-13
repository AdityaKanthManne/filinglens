from unittest.mock import patch
from filinglens.research import research_company

def test_research_company_offline():
    data={"cik":320193,"entityName":"Apple Inc.","facts":{"us-gaap":{"Revenues":{"units":{"USD":[
        {"start":"2023-10-01","end":"2024-09-30","val":100,"filed":"2024-11-01","accn":"A01","form":"10-K"},
        {"start":"2024-10-01","end":"2025-09-30","val":125,"filed":"2025-11-01","accn":"A02","form":"10-K"}
    ]}}}}}
    with patch("filinglens.research.fetch_companyfacts",return_value=data):
        result=research_company("0000320193")
    assert result["company"]=="Apple Inc."
    assert result["comparisons"][0]["growth_pct"]==25.0
    assert result["comparisons"][0]["source_accessions"]==["A01","A02"]
