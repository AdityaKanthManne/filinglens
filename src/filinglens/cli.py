"""Inspect raw SEC Company Facts with original filing references."""
from __future__ import annotations

import argparse
from .sec import fetch_companyfacts, normalize_cik, revenue_observations


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve reported SEC revenue facts (not normalized quarters)")
    parser.add_argument("--cik", default="0000320193", help="Company CIK, e.g. 0000320193 (Apple)")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--concept", default="RevenueFromContractWithCustomerExcludingAssessedTax")
    args = parser.parse_args()
    data = fetch_companyfacts(normalize_cik(args.cik))
    print(f"Entity: {data.get('entityName', 'Unknown')} | CIK: {data.get('cik')}")
    print(f"Concept: us-gaap:{args.concept} | Raw SEC-reported observations")
    rows = revenue_observations(data, concept=args.concept, limit=args.limit)
    if not rows:
        print("No matching observations. Try --concept Revenues; inspect concepts before comparison.")
    for row in rows:
        print(f"{row['start']} to {row['end']} | USD {row['val']:,} | {row['form']} | filed {row['filed']} | accession {row['accn']}")
    print("NOTE: Values may overlap or be restated; do not sum observations as quarters.")


if __name__ == "__main__":
    main()
