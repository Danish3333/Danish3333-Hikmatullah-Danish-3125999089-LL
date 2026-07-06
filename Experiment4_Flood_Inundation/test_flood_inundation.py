# =============================================
# Test Results: Run with: pytest test_flood_inundation.py -v
# Expected: 10/10 tests PASS
# =============================================
"""pytest test suite for Experiment 4: Flood Inundation Analysis."""

import numpy as np
import pytest
from flood_inundation import generate_dem, calculate_flood, simulate_rising_water, validate


def test_dem_shape():
    """DEM must be 100x100 2D array."""
    dem = generate_dem(100, seed=42)
    assert dem.shape == (100, 100)


def test_dem_elevation_range():
    """DEM elevations must be in [30, 80] meters range."""
    dem = generate_dem(100, seed=42)
    assert dem.min() >= 29.9
    assert dem.max() <= 80.1


def test_dem_reproducible():
    """Same seed must produce identical DEM."""
    dem1 = generate_dem(100, seed=42)
    dem2 = generate_dem(100, seed=42)
    assert np.allclose(dem1, dem2)


def test_flood_zero_at_low_water():
    """Water level below min elevation → 0% flooded."""
    dem = generate_dem(100, seed=42)
    result = calculate_flood(dem, dem.min() - 1)
    assert result['percentage'] < 0.01


def test_flood_hundred_at_high_water():
    """Water level above max elevation → 100% flooded."""
    dem = generate_dem(100, seed=42)
    result = calculate_flood(dem, dem.max() + 1)
    assert abs(result['percentage'] - 100.0) < 0.01


def test_flood_percentage_between_0_and_100():
    """Flood percentage must be in [0, 100]."""
    dem = generate_dem(100, seed=42)
    result = calculate_flood(dem, 55.0)
    assert 0 <= result['percentage'] <= 100


def test_flood_50m_greater_than_40m():
    """Flood extent at 50m must be >= flood extent at 40m."""
    dem = generate_dem(100, seed=42)
    r40 = calculate_flood(dem, 40.0)
    r50 = calculate_flood(dem, 50.0)
    assert r50['percentage'] >= r40['percentage']


def test_depth_array_nonnegative():
    """All depth values must be >= 0."""
    dem = generate_dem(100, seed=42)
    result = calculate_flood(dem, 55.0)
    assert np.all(result['depth_array'] >= 0)


def test_simulate_rising_water_monotonic():
    """Flood percentage must be non-decreasing as water level rises."""
    dem = generate_dem(100, seed=42)
    levels = np.linspace(30, 80, 10)
    sim = simulate_rising_water(dem, levels)
    pcts = sim['percentages']
    for i in range(len(pcts)-1):
        assert pcts[i+1] >= pcts[i] - 1e-6


def test_validate_all_pass():
    """Built-in validate() function must return all True results."""
    dem = generate_dem(100, seed=42)
    results = validate(dem)
    assert len(results) == 5
    for name, passed in results:
        assert passed, f"Validation failed: {name}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])