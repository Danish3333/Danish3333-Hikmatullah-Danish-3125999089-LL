# Experiment 2: SCS-CN Runoff Calculation

**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026 | **Xi'an Jiaotong University**

Implements the USDA Soil Conservation Service Curve Number (SCS-CN) method for estimating direct runoff from rainfall. Includes vectorized NumPy implementation, physical boundary condition handling, sensitivity analysis across 6 land-cover types, and comprehensive validation.

---

## Directory Structure

| File | Purpose |
|------|---------|
| `scscn_runoff.py` | Core SCS-CN implementation — calculate_runoff(), calculate_S(), calculate_Ia(), batch_calculate_runoff() |
| `sensitivity_analysis.py` | Sensitivity analysis — generates CN vs Q and Rainfall vs Runoff plots |
| `test_scscn_runoff.py` | pytest test suite — 8 boundary condition tests |
| `validate_scscn_runoff.py` | Physical validation — 13 automated checks |
| `validation_report.txt` | Auto-generated validation results (13/13 PASSED) |
| `prompt_log.md` | AI-assisted development documentation (~2100 words) |
| `requirements.txt` | Python dependencies with pinned versions |
| `outputs/` | Generated plots (2 PNG files) |
| `screenshot/` | Program screenshots |
| `chat_history/` | AI interaction history |

## SCS-CN Formula Reference

| Symbol | Name | Formula | Unit |
|--------|------|---------|------|
| P | Rainfall depth | Input | mm |
| CN | Curve Number | Input (1–100) | — |
| S | Max retention | (25400/CN) − 254 | mm |
| Ia | Initial abstraction | 0.2 × S | mm |
| Q | Runoff depth | (P−Ia)² / (P−Ia+S) | mm |

## Land-Cover CN Reference

| Land Cover | CN Value | Runoff at P=50mm |
|-----------|----------|------------------|
| Forest (good) | 60 | 1.4 mm |
| Pasture | 70 | 5.8 mm |
| Cultivated | 80 | 13.8 mm |
| Urban (residential) | 90 | 27.1 mm |
| Urban (dense) | 95 | 37.8 mm |
| Impervious | 100 | 50.0 mm |

## Quick Start

### Prerequisites
Python 3.10+

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Core Calculation
```bash
python scscn_runoff.py
# Verifies known example: P=50mm, CN=80 → Q=13.8mm
```

### Run Sensitivity Analysis
```bash
python sensitivity_analysis.py
# Generates 2 PNG plots in outputs/
```

### Run Tests
```bash
python test_scscn_runoff.py
```
**Expected output:** 8/8 tests passed

### Run Validation
```bash
python validate_scscn_runoff.py
```
**Expected output:** 13/13 checks PASSED

## Expected Output

```
$ python test_scscn_runoff.py
Running SCS-CN Test Suite...
--------------------------------------------------
  [PASS] P=0, Q=0
  [PASS] P < Ia, Q=0
  [PASS] P=Ia, Q=0
  [PASS] P=50, CN=80 -> Q=13.8
  [PASS] CN=100 max runoff
  [PASS] Q <= P for all cases
  [PASS] CN=0 raises error
  [PASS] P<0 raises error
--------------------------------------------------
Results: 8/8 tests passed
```

```
$ python validate_scscn_runoff.py
[PASS] V01: Zero rainfall → zero runoff — Q=0.0
[PASS] V02: Runoff non-negative — Q=13.80
[PASS] V03: Q ≤ P — Q=13.80 ≤ 50
[PASS] V04: CN=90 > CN=70 runoff — 27.11 > 5.81
[PASS] V05: P=100 > P=50 runoff — 50.54 > 13.80
...
─────────────────────────────
Validation Summary: 13/13 checks PASSED
```

## Physical Constraints Verified

| Constraint | Test | Result |
|-----------|------|--------|
| Zero rain → zero runoff | P=0, CN=80 | Q=0.0 ✅ |
| Runoff ≥ 0 | P=50, CN=80 | 13.8 ≥ 0 ✅ |
| Q ≤ P | P=50, CN=80 | 13.8 ≤ 50 ✅ |
| Higher CN → more runoff | CN=90 vs CN=70 | 27.1 > 5.8 ✅ |
| More rain → more runoff | P=100 vs P=50 | 50.5 > 13.8 ✅ |
| Below Ia → zero runoff | P=5, CN=70 | Q=0.0 ✅ |

## Screenshots
See [`screenshot/`](./screenshot/) for test results, validation output, and sensitivity analysis plots.

## Prompt Log
See [`prompt_log.md`](./prompt_log.md) for full AI-assisted development documentation (8 prompts, error table, 5 design decisions, reflection).