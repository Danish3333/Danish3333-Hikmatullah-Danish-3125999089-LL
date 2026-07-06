# Experiment 3: Reservoir Dispatch Optimization

**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026 | **Xi'an Jiaotong University**

Multi-objective optimization for a 7-day hydropower reservoir dispatch using SLSQP. Balances revenue maximization against ecological flow requirements with 6 physical constraints, Pareto frontier analysis, and comprehensive validation.

---

## Directory Structure

| File | Purpose |
|------|---------|
| `reservoir_optimize.py` | Main optimization — SLSQP solver, revenue calculation, Pareto analysis |
| `test_reservoir_optimize.py` | pytest test suite — 10 tests for storage, revenue, deficit, outputs |
| `validate_reservoir.py` | Physical validation — 13 automated checks |
| `validation_report.txt` | Auto-generated validation results (13/13 PASSED) |
| `prompt_log.md` | AI-assisted development documentation (~2000 words) |
| `requirements.txt` | Python dependencies with pinned versions |
| `outputs/` | Generated files (optimal_schedule.csv, tradeoff_analysis.png) |
| `screenshot/` | Program screenshots |
| `chat_history/` | AI interaction history |

## Reservoir Parameters

| Parameter | Symbol | Value | Unit |
|-----------|--------|-------|------|
| Initial storage | V₀ | 500,000 | m³ |
| Min storage | V_min | 100,000 | m³ |
| Max storage | V_max | 1,000,000 | m³ |
| Ecological min release | Q_eco | 10 | m³/s |
| Max release | Q_max | 100 | m³/s |
| Hydraulic head | H | 30 | m |
| Turbine efficiency | η | 0.85 | — |

## 7-Day Inflow & Price Schedule

| Day | Inflow (m³/s) | Price ($/kWh) |
|-----|---------------|---------------|
| 1 | 15 | 0.08 |
| 2 | 12 | 0.08 |
| 3 | 10 | 0.08 |
| 4 | 8 | 0.08 |
| 5 | 12 | 0.10 |
| 6 | 15 | 0.12 |
| 7 | 18 | 0.10 |

## Physical Constraints

| Constraint | Description | Verified |
|-----------|-------------|----------|
| C1 | V[t] ≥ 100,000 m³ | ✅ V03 |
| C2 | V[t] ≤ 1,000,000 m³ | ✅ V04 |
| C3 | Q[t] ≥ 10 m³/s | ✅ V01 |
| C4 | Q[t] ≤ 100 m³/s | ✅ V02 |
| C5 | Mass balance | ✅ V05 |
| C6 | Revenue > 0 | ✅ V06 |

## Quick Start

### Prerequisites
Python 3.10+

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Optimization
```bash
python reservoir_optimize.py
```
**Expected:** Total Revenue: $54,910.69, Ecological Deficit: 0.00

### Run Tests
```bash
pytest test_reservoir_optimize.py -v
```
**Expected output:** 10/10 tests PASS

### Run Validation
```bash
python validate_reservoir.py
```
**Expected output:** 13/13 checks PASSED

## Expected Output

```
$ python reservoir_optimize.py
All outputs generated successfully.
  Total Revenue: $54,910.69
  Ecological Deficit: 0.00

$ python validate_reservoir.py
[PASS] V01: All releases >= Q_eco=10.0 — min=10.00
[PASS] V02: All releases <= Q_max=100.0 — max=25.41
[PASS] V03: Storage >= V_min=100000 — min=100500
[PASS] V04: Storage <= V_max=1000000 — max=999500
[PASS] V05: Mass balance holds at all time steps
[PASS] V06: Total revenue > 0 — $54,910.69
...
─────────────────────────────
Validation Summary: 13/13 checks PASSED
```

## Test Results
Run: `pytest test_reservoir_optimize.py -v`  
**10/10 tests passed.** See [`screenshot/`](./screenshot/).

## Validation Results
Run: `python validate_reservoir.py`  
**13/13 validation checks passed.** See [`validation_report.txt`](./validation_report.txt).

## System Architecture

| Module | Key Function | Description |
|--------|-------------|-------------|
| reservoir_optimize | `compute_storage()` | Month-by-month storage state equation |
| reservoir_optimize | `compute_total_revenue()` | Hydropower output (negative for minimizer) |
| reservoir_optimize | `optimize_max_revenue()` | SciPy SLSQP constrained optimizer |
| reservoir_optimize | `optimize_pareto()` | Multi-objective Pareto analysis |
| test_reservoir_optimize | `test_*()` | 10 pytest boundary and constraint tests |
| validate_reservoir | `validate_*()` | 13 physical feasibility checks |

## Physical Constraints Verified

| Constraint | Test Case | Result |
|-----------|----------|--------|
| Storage >= 100,000 m³ | All 7 days | V_min = 100,500 ✅ |
| Storage <= 1,000,000 m³ | Peak storage | V_max = 999,500 ✅ |
| Release >= 10 m³/s (ecological) | All days | Q_min = 10.00 ✅ |
| Release <= 100 m³/s | High price day | Q_max = 25.42 ✅ |
| Mass balance closure | Full 7-day horizon | Error < 1 m³ ✅ |
| Revenue > 0 | Maximum revenue | $54,910.69 ✅ |

## Screenshots
See [`screenshot/`](./screenshot/) for test results, validation output, and Pareto frontier plot.

## Prompt Log
See [`prompt_log.md`](./prompt_log.md) for full AI-assisted development documentation (8 prompts, error table, 5 design decisions, reflection).