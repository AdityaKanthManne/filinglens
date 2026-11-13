"""SEC submission filing discovery with aligned array indexing and source URLs."""
from __future__ import annotations
from urllib.parse import quote

FIELDS=("form","filingDate","reportDate","accessionNumber","primaryDocument")

def recent_filings(data: dict, *, forms: tuple[str,...] = ("10-K","10-Q"), limit: int=10) -> list[dict]:
    if limit<1:
        raise ValueError("limit must be positive")
    recent=data.get("filings",{}).get("recent",{})
    if any(not isinstance(recent.get(k),list) for k in FIELDS):
        raise ValueError("Missing or malformed SEC filings.recent arrays")
    n=len(recent["form"])
    if any(len(recent[k])!=n for k in FIELDS):
        raise ValueError("SEC parallel filing arrays are not aligned")
    results=[]
    for i in range(n):
        if recent["form"][i] not in forms:
            continue
        entry={key:recent[key][i] for key in FIELDS}
        accession=str(entry["accessionNumber"])
        if not accession.replace("-","").isdigit():
            continue
        cik=str(data["cik"]).lstrip("0") or "0"
        doc=str(entry["primaryDocument"])
        if "/" in doc or ".." in doc:
            continue
        entry["document_url"]=f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession.replace('-','')}/{quote(doc)}"
        results.append(entry)
        if len(results)>=limit:
            break
    return results
