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

## Current end-to-end annual financial research command

```bash
export SEC_USER_AGENT="FilingLens actual-contact@yourdomain.com"
python -m filinglens.research --cik 0000320193
```

The command uses live SEC Company Facts unless a valid cache exists, selects annual-duration observations reported on 10-Ks, computes only consecutive-period growth, and preserves accession numbers. It is a **numerical research baseline**. It does not yet ingest full narrative documents, provide hybrid retrieval/RAG, expose a deployed frontend, or demonstrate benchmarked analyst-time savings. Fiscal-period and restatement logic require additional validation before investment use.

Run tests with `pytest -q`. Tests use fixtures and do not query the SEC.

## Quant research extension (experimental)

`filinglens.event_study` exposes `abnormal_returns(asset_returns, benchmark_returns)` and `event_summary(...)` for market-adjusted event-window returns and a descriptive t statistic. Run `pytest -q tests/test_event_study.py`. **Not yet connected to historical price ingestion or SEC filing-event alignment.** Event selection, timing, overlapping windows, transaction costs and out-of-sample testing remain requirements before drawing alpha conclusions.

**Planned next:** point-in-time filing/price joins, transparent event-window selection, bootstrap confidence intervals, transaction-cost sensitivity, walk-forward signal backtests, and RAG grounding evaluations.
