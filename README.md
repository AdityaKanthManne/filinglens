# FilingLens

**Week 1 of the AI Engineering Bootcamp (Nov 2–8, 2026)**

A source-grounded financial research tool built on public SEC EDGAR data. The first vertical slice retrieves XBRL company facts and displays reported revenue observations with filing provenance. Later milestones add period normalization, evaluation, document retrieval, and cited questions.

## Day 1: retrieve financial facts

Requirements: Python 3.11+, internet connection for the first fetch; no paid APIs.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
python -m pip install -e '.[dev]'
# Identify yourself to SEC by setting an actual contact email (do not commit it):
# macOS/Linux: export SEC_USER_AGENT='FilingLens research contact@example.com'
# PowerShell: $env:SEC_USER_AGENT='FilingLens research contact@example.com'
python -m filinglens.cli --cik 0000320193 --limit 5
pytest -q
```

An honest, descriptive User-Agent with real contact information is required; placeholder addresses will be rejected by the CLI. Requests are cached locally under `.cache/` and throttled. Cache files and credentials are not committed.

## Scope and limitations

- Current Day 1 output is **raw reporting observations**, not normalized quarters, growth rates, a finished RAG system, or investment advice.
- Revenue XBRL tags vary by filer; `RevenueFromContractWithCustomerExcludingAssessedTax` and `Revenues` are initial candidates and **must not be silently mixed**.
- Multiple filing records can refer to the same accounting period; do not sum them or treat them as independent quarters.
- The SEC XBRL APIs cover standardized entity-wide concepts, not every disclosure or custom tag.

## Roadmap

| Day | Build | Exit criterion |
|---|---|---|
| 1 | SEC ingestion + cache + basic provenance | CLI fetch and offline tests work |
| 2 | Normalize concepts and annual/quarterly periods | Tested handling of duplicates and durations |
| 3 | SQLite schema and five-company ingestion | Reproducible local dataset |
| 4 | Filing text acquisition, chunking and search | Retrieval returns source locations |
| 5 | Answer synthesis and evaluation | 30 labelled questions and citation checks |
| 6 | Streamlit UI + API/error handling | End-to-end demonstration |
| 7 | Test, document, profile and release | Reproducible local release |

## Data source

Official SEC EDGAR XBRL Company Facts API: https://www.sec.gov/search-filings/edgar-application-programming-interfaces

SEC data is public. Respect SEC fair-access guidelines and identify your application in the User-Agent.
