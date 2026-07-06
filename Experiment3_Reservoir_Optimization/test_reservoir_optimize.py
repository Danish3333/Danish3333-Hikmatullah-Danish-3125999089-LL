# =============================================
# Test Results: Run with: pytest test_reservoir_optimize.py -v
# Expected: 10/10 tests PASS
# =============================================
"""pytest test suite for Experiment 3: Reservoir Dispatch Optimization."""

import numpy as np
import pytest
from reservoir_optimize import (
    compute_storage, compute_total_revenue, compute_eco_deficit,
    inflow, V0, V_min, V_max, Q_eco, Q_max, T
)


def test_compute_storage_initial():
    """Storage[0] must equal V0 = 500000."""
    releases = np.full(T, 15.0)
    storage = compute_storage(releases)
    assert storage[0] == V0


def test_compute_storage_mass_balance():
    """Each step: storage[t+1] = storage[t] + (inflow[t]-release[t])*86400."""
    releases = np.array([12.0, 11.0, 10.0, 9.0, 11.0, 14.0, 16.0])
    storage = compute_storage(releases)
    dt = 86400
    for t in range(T):
        expected = storage[t] + (inflow[t] - releases[t]) * dt
        assert abs(storage[t+1] - expected) < 1.0


def test_revenue_positive():
    """Revenue must be positive for any positive release schedule."""
    releases = np.full(T, 20.0)
    assert compute_total_revenue(releases) > 0


def test_revenue_higher_release_higher_revenue():
    """Higher uniform release must give higher revenue (within bounds)."""
    r_low = np.full(T, 10.0)
    r_high = np.full(T, 50.0)
    assert compute_total_revenue(r_high) > compute_total_revenue(r_low)


def test_eco_deficit_zero_when_above_threshold():
    """No deficit when all releases >= Q_eco."""
    releases = np.full(T, Q_eco + 5)
    assert compute_eco_deficit(releases) == 0.0


def test_eco_deficit_positive_when_below_threshold():
    """Positive deficit when releases < Q_eco."""
    releases = np.full(T, Q_eco - 5)
    assert compute_eco_deficit(releases) > 0.0


def test_storage_length():
    """compute_storage must return array of length T+1."""
    releases = np.full(T, 15.0)
    storage = compute_storage(releases)
    assert len(storage) == T + 1


def test_optimal_schedule_csv_exists():
    """outputs/optimal_schedule.csv must exist after script runs."""
    import os
    assert os.path.exists('outputs/optimal_schedule.csv')


def test_optimal_schedule_csv_has_7_rows():
    """CSV must have 7 data rows (one per day)."""
    import csv
    with open('outputs/optimal_schedule.csv') as f:
        reader = csv.reader(f)
        rows = list(reader)
    assert len(rows) == 8  # 1 header + 7 data rows


def test_tradeoff_png_exists():
    """outputs/tradeoff_analysis.png must exist."""
    import os
    assert os.path.exists('outputs/tradeoff_analysis.png')


if __name__ == '__main__':
    pytest.main([__file__, '-v'])