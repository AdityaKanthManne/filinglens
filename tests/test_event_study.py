from filinglens.event_study import abnormal_returns, event_summary
import pytest


def test_market_adjustment():
    assert abnormal_returns([0.04, -0.02], [0.01, -0.01]) == pytest.approx([0.03, -0.01])


def test_event_summary():
    result = event_summary([0.03, 0.05, 0.07], [0.01, 0.01, 0.01])
    assert result["n"] == 3
    assert result["mean_abnormal_return"] == pytest.approx(0.04)
    assert result["t_statistic"] is not None


def test_invalid_inputs_and_degenerate_t():
    with pytest.raises(ValueError):
        event_summary([0.1], [])
    assert event_summary([0.01], [0.0])["t_statistic"] is None
