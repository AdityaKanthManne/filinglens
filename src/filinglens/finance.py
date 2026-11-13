"""Auditable XBRL annual revenue selection and deterministic calculations."""
from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Any

CONCEPTS = ("RevenueFromContractWithCustomerExcludingAssessedTax","Revenues","SalesRevenueNet")

@dataclass(frozen=True)
class AnnualFact:
    cik: str
    concept: str
    year: int
    value: int
    start: str
    end: str
    filed: str
    accession: str
    form: str

def annual_revenue(data: dict[str, Any], *, concept: str | None = None) -> list[AnnualFact]:
    """Select 10-K annual-duration observations only. Never conflate concepts.

    Preference is latest filing date per fiscal period, keeping its accession
    for traceability. This is not a general restatement-resolution system.
    """
    available = data.get("facts",{}).get("us-gaap",{})
    chosen = concept or next((c for c in CONCEPTS if "USD" in available.get(c,{}).get("units",{})), None)
    if chosen is None:
        return []
    facts = available.get(chosen,{}).get("units",{}).get("USD",[])
    result = {}
    for item in facts:
        if item.get("form") != "10-K" or not all(item.get(k) is not None for k in ("start","end","val","filed","accn")):
            continue
        try:
            start,end = date.fromisoformat(item["start"]),date.fromisoformat(item["end"])
        except ValueError:
            continue
        duration=(end-start).days+1
        if not 350<=duration<=380:
            continue
        year=end.year
        observation=AnnualFact(str(data.get("cik","")).zfill(10),chosen,year,int(item["val"]),item["start"],item["end"],item["filed"],item["accn"],item["form"])
        key=(item["start"],item["end"])
        old=result.get(key)
        if old is None or (observation.filed,observation.accession)>(old.filed,old.accession):
            result[key]=observation
    return sorted(result.values(),key=lambda row:(row.end,row.filed))

def growth(previous: int | float, current: int | float) -> float | None:
    if previous==0:
        return None
    return round((current-previous)/abs(previous)*100,2)

def compare_annual(facts: list[AnnualFact]) -> list[dict]:
    rows=[]
    for previous,current in zip(facts,facts[1:]):
        # Avoid misrepresenting nonconsecutive or incompatible periods as YoY.
        gap=(date.fromisoformat(current.end)-date.fromisoformat(previous.end)).days
        if previous.concept!=current.concept or not 350<=gap<=380:
            continue
        rows.append({"prior_period":previous.end,"current_period":current.end,"prior_revenue":previous.value,"current_revenue":current.value,"growth_pct":growth(previous.value,current.value),"source_accessions":[previous.accession,current.accession]})
    return rows
