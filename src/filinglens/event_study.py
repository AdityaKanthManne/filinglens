"""Transparent event-study statistics. Inputs must be point-in-time aligned.

This module does not download prices or claim predictive alpha. Returns are decimal
period returns, e.g. 0.01 for 1%, and must use comparable event windows.
"""
from __future__ import annotations
from math import sqrt
from statistics import mean, stdev


def abnormal_returns(asset_returns: list[float], benchmark_returns: list[float]) -> list[float]:
    if len(asset_returns) != len(benchmark_returns) or not asset_returns:
        raise ValueError("Equal nonempty return series are required")
    return [float(asset) - float(benchmark) for asset, benchmark in zip(asset_returns, benchmark_returns)]


def event_summary(asset_returns: list[float], benchmark_returns: list[float]) -> dict[str, float | int | None]:
    """Mean market-adjusted return and descriptive one-sample t statistic.

    A t statistic is not proof of alpha: overlapping events, dependence, event
    selection and multiple hypotheses can invalidate its usual interpretation.
    """
    excess = abnormal_returns(asset_returns, benchmark_returns)
    n = len(excess)
    avg = mean(excess)
    sd = stdev(excess) if n > 1 else None
    t_stat = (avg / (sd / sqrt(n))) if sd is not None and sd > 0 else None
    return {"n": n, "mean_abnormal_return": avg, "sample_std": sd, "t_statistic": t_stat}
