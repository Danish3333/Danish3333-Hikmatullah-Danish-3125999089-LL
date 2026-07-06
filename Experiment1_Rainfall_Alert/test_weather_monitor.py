# =============================================
# Test Results: Run with: pytest test_weather_monitor.py -v
# Expected: 10/10 tests PASS
# =============================================
"""pytest test suite for Experiment 1: Rainfall Alert System.
Tests check_alert(), get_rainfall_category(), and log_alert().
No live API calls — fetch_weather is excluded."""

import os
import pytest
from weather_monitor import check_alert, get_rainfall_category, log_alert


def test_check_alert_normal_zero():
    """Rain=0: must return Green, Normal."""
    level, status, color = check_alert(0)
    assert level == "Green"
    assert status == "Normal"


def test_check_alert_normal_boundary():
    """Rain=9.99: still Green/Normal, not Moderate (boundary just below 10)."""
    level, status, color = check_alert(9.99)
    assert level == "Green"


def test_check_alert_moderate_exact():
    """Rain=10.0: must return Yellow, Moderate (exact lower boundary of Yellow)."""
    level, status, color = check_alert(10.0)
    assert level == "Yellow"
    assert status == "Moderate"


def test_check_alert_moderate_mid():
    """Rain=15: Yellow, Moderate (mid-range of Yellow band)."""
    level, status, color = check_alert(15.0)
    assert level == "Yellow"


def test_check_alert_heavy_exact():
    """Rain=20.0: must return Red, Heavy - ALERT (exact boundary)."""
    level, status, color = check_alert(20.0)
    assert level == "Red"


def test_check_alert_heavy_extreme():
    """Rain=100: Red, Heavy - ALERT (extreme rainfall)."""
    level, status, color = check_alert(100)
    assert level == "Red"


def test_check_alert_returns_tuple():
    """check_alert must return a 3-tuple: (level, status, rgba_color_string)."""
    result = check_alert(15.0)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert isinstance(result[2], str)
    assert result[2].startswith("rgba")


def test_get_category_light():
    """Rain=5 → should contain 'Light' (CMA classification)."""
    cat = get_rainfall_category(5)
    assert "Light" in cat


def test_get_category_torrential():
    """Rain=35 → should contain 'Torrential'."""
    cat = get_rainfall_category(35)
    assert "Torrential" in cat


def test_log_alert_creates_file(tmp_path):
    """log_alert() must create alert_log.txt containing city name and rainfall value."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        entry = log_alert(25.0, "Red", "Heavy - ALERT", "TestCity")
        assert os.path.exists("alert_log.txt"), "alert_log.txt was not created"
        with open("alert_log.txt") as f:
            content = f.read()
        assert "TestCity" in content, "City name missing from log"
        assert "25.00" in content, "Rainfall value not formatted to 2 decimals"
    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])