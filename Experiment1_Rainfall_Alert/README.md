# Experiment 1: Rainfall Alert System

**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026 | **Xi'an Jiaotong University**

Real-time rainfall monitoring and alert dashboard for 5 Chinese cities (Beijing, Shanghai, Guangzhou, Shenzhen, Wuhan). Integrates OpenWeatherMap API with a Streamlit dashboard featuring interactive pydeck map, 3-level color-coded alerts, and timestamped event logging.

---

## Directory Structure

| File | Purpose |
|------|---------|
| `weather_monitor.py` | Main application — API integration, alert logic, Streamlit dashboard |
| `test_weather_monitor.py` | pytest test suite — 10 tests for alert thresholds and logging |
| `test_api.py` | Standalone API connection test |
| `validate_rainfall_alert.py` | Physical validation — 13 automated checks |
| `validation_report.txt` | Auto-generated validation results (13/13 PASSED) |
| `generate_report.py` | Batch weather report generator for all 5 cities |
| `alert_log.txt` | Runtime alert log — timestamped Red-level events |
| `prompt_log.md` | AI-assisted development documentation (~2000 words) |
| `requirements.txt` | Python dependencies with pinned versions |
| `outputs/` | Generated output files (weather_report.txt, alert_report.txt, weather_data.csv) |
| `screenshot/` | Program screenshots |
| `chat_history/` | AI interaction history |

## Quick Start

### Prerequisites
Python 3.10+

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Dashboard
```bash
streamlit run weather_monitor.py
```
Open http://localhost:8501 in your browser.

### Run Tests
```bash
pytest test_weather_monitor.py -v
```
**Expected output:** 10/10 tests PASS

### Run Validation
```bash
python validate_rainfall_alert.py
```
**Expected output:** 13/13 checks PASSED

### Generate Reports
```bash
python generate_report.py
```
Creates `outputs/weather_report.txt`, `outputs/alert_report.txt`, `outputs/weather_data.csv`.

## Expected Output

```
$ pytest test_weather_monitor.py -v
============================= test session starts =============================
test_weather_monitor.py::test_check_alert_normal_zero PASSED              [ 10%]
test_weather_monitor.py::test_check_alert_normal_boundary PASSED          [ 20%]
test_weather_monitor.py::test_check_alert_moderate_exact PASSED           [ 30%]
test_weather_monitor.py::test_check_alert_moderate_mid PASSED             [ 40%]
test_weather_monitor.py::test_check_alert_heavy_exact PASSED              [ 50%]
test_weather_monitor.py::test_check_alert_heavy_extreme PASSED            [ 60%]
test_weather_monitor.py::test_check_alert_returns_tuple PASSED            [ 70%]
test_weather_monitor.py::test_get_category_light PASSED                   [ 80%]
test_weather_monitor.py::test_get_category_torrential PASSED              [ 90%]
test_weather_monitor.py::test_log_alert_creates_file PASSED              [100%]
============================= 10 passed in 0.73s =============================
```

```
$ python validate_rainfall_alert.py
[PASS] V01: Zero rainfall is Green — result: Green
[PASS] V02: Rain=9.99 stays Normal — result: Normal
[PASS] V03: Exact boundary Rain=10 = Moderate — result: Yellow
[PASS] V04: Rain=19.99 stays Yellow — result: Yellow
[PASS] V05: Exact boundary Rain=20 = Red — result: Red
[PASS] V06: Rain=100 = Red (extreme) — result: Red
[PASS] V07: check_alert returns 3-tuple — length=3
[PASS] V08: Color string is rgba format — result: rgba(255, 255, 0, 0...
[PASS] V09: Rain=5 category contains Light
[PASS] V10: Rain=35 category contains Torrential
[PASS] V11: Rain=75 category contains Extreme
[PASS] V12: log_alert contains city name
[PASS] V13: log_alert formats rainfall to 2 decimals
─────────────────────────────
Validation Summary: 13/13 checks PASSED
```

## Alert Threshold System

| Level  | Color  | Threshold    | CMA Category                   | Action      |
|--------|--------|-------------|--------------------------------|-------------|
| Green  | 🟢     | < 10 mm/h    | Light rain / Moderate rain     | Normal      |
| Yellow | 🟡     | 10–19.99 mm/h | Heavy rain                     | Watch       |
| Red    | 🔴     | ≥ 20 mm/h    | Torrential rain / Extreme      | ALERT + Log |

## System Architecture

| Module            | Key Function              | Description                    |
|-------------------|---------------------------|--------------------------------|
| weather_monitor   | `fetch_weather()`         | OpenWeatherMap API call        |
| weather_monitor   | `check_alert()`           | 3-level threshold classification |
| weather_monitor   | `log_alert()`             | Write alert event to file      |
| weather_monitor   | `get_rainfall_category()` | CMA rainfall classification    |
| weather_monitor   | `main()`                  | Streamlit dashboard            |

## Test Results
Run: `pytest test_weather_monitor.py -v`  
**10/10 tests passed.** See [`screenshot/test_results.png`](./screenshot/).

## Validation Results
Run: `python validate_rainfall_alert.py`  
**13/13 validation checks passed.** See [`validation_report.txt`](./validation_report.txt).

## Screenshots
See [`screenshot/`](./screenshot/) for test results, validation output, and dashboard images.

## Prompt Log
See [`prompt_log.md`](./prompt_log.md) for full AI-assisted development documentation (8 prompts, error table, 5 design decisions, reflection).