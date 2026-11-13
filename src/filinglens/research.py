"""FilingLens end-to-end SEC research CLI: cited annual financial trends + filing index."""
from __future__ import annotations
import argparse
import json
from .sec import fetch_companyfacts
from .finance import annual_revenue, compare_annual

def research_company(cik: str, *, cache_dir: str = ".cache/sec", concept: str | None = None) -> dict:
    payload=fetch_companyfacts(cik,cache_dir=cache_dir)
    facts=annual_revenue(payload,concept=concept)
    return {
        "company":payload.get("entityName"),
        "cik":str(payload.get("cik")).zfill(10),
        "concept":facts[0].concept if facts else None,
        "annual_observations":[{
            "period_start":f.start,
            "period_end":f.end,
            "value_usd":f.value,
            "filed":f.filed,
            "accession":f.accession
        } for f in facts],
        "comparisons":compare_annual(facts),
        "note":"Annual 10-K USD duration facts only; verify fiscal comparability and accounting concept before decisions."
    }

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--cik",default="0000320193")
    parser.add_argument("--concept")
    args=parser.parse_args()
    print(json.dumps(research_company(args.cik,concept=args.concept),indent=2))

if __name__=="__main__":
    main()
