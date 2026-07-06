# Experiment 4: Flood Inundation Analysis (DEM-based)

**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026 | **Xi'an Jiaotong University**

Spatial flood inundation analysis using Digital Elevation Model data. Simulates flooding on a synthetic 100×100 terrain grid, generates 3-panel visualizations, and validates 13 physical constraints including monotonicity, depth bounds, and edge cases.

---

## Directory Structure

| File | Purpose |
|------|---------|
| `flood_inundation.py` | Main flood analysis — DEM generation, flood calculation, visualization, validation |
| `test_flood_inundation.py` | pytest test suite — 10 tests for DEM, flood, and simulation |
| `validate_flood.py` | Physical validation — 13 automated checks |
| `validation_report.txt` | Auto-generated validation results (13/13 PASSED) |
| `prompt_log.md` | AI-assisted development documentation (~2000 words) |
| `requirements.txt` | Python dependencies with pinned versions |
| `outputs/` | Generated files (dem_data.npy, flood_extent_40m.png, flood_extent_50m.png, flood_curve.png) |
| `screenshot/` | Program screenshots |
| `chat_history/` | AI interaction history |

## DEM Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Grid size | 100 × 100 | 10,000 cells |
| Elevation range | 30 – 80 m | Synthetic terrain |
| River valley | Gaussian dip | Diagonal channel across terrain |
| Hills | Sinusoidal | 2-frequency terrain variation |
| Seed | 42 | Fixed for reproducibility |

## Flood Simulation Levels

| Water Level | Flooded Area | Max Depth |
|-------------|-------------|-----------|
| 40 m | 10.1% | 10.0 m |
| 50 m | 37.2% | 20.0 m |
| 55 m | 55.7% | 25.0 m |
| 30–80 m | 51 steps | Full curve |

## Quick Start

### Prerequisites
Python 3.10+

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Flood Analysis
```bash
python flood_inundation.py
```
**Expected output:** 4 files generated in `outputs/`, 5/5 internal validation PASS

### Run Tests
```bash
pytest test_flood_inundation.py -v
```
**Expected output:** 10/10 tests PASS

### Run Validation
```bash
python validate_flood.py
```
**Expected output:** 13/13 checks PASSED

## Expected Output

```
$ python flood_inundation.py
============================================================
FLOOD INUNDATION ANALYSIS (DEM-based)
============================================================

[1] DEM generated: (100, 100), range=[30.0, 80.0]m
Saved: outputs/flood_extent_40m.png

[2] WL=40m: Flooded=10.06%, Max Depth=10.00m
Saved: outputs/flood_extent_50m.png

[2] WL=50m: Flooded=37.20%, Max Depth=20.00m
Saved: outputs/flood_curve.png

[3] Dynamic simulation: 51 levels from 30.0m to 80.0m

[4] Validation Results:
----------------------------------------
  [PASS] WL < min elevation -> 0%
  [PASS] WL > max elevation -> 100%
  [PASS] Flooded area increases monotonically
  [PASS] Max depth = WL - min_elev
  [PASS] Percentage between 0-100
----------------------------------------
  Overall: ALL PASS
```

```
$ python validate_flood.py
[PASS] V01: DEM shape is (100,100) — (100, 100)
[PASS] V02: DEM min ≥ 29.9m — 30.0m
[PASS] V03: DEM max ≤ 80.1m — 80.0m
[PASS] V04: DEM reproducible (same seed)
[PASS] V05: WL<min → 0% — 0.000%
[PASS] V06: WL>max → 100% — 100.000%
[PASS] V07: Flood@50m ≥ Flood@40m — 37.2% ≥ 10.1%
...
─────────────────────────────
Validation Summary: 13/13 checks PASSED
```

## Physical Validation Checks (13 total)

| Check | Description | Result |
|-------|-------------|--------|
| V01 | DEM shape is (100, 100) | ✅ |
| V02 | DEM min elevation ≥ 29.9m | ✅ |
| V03 | DEM max elevation ≤ 80.1m | ✅ |
| V04 | DEM reproducible (same seed) | ✅ |
| V05 | WL below min → 0% flooded | ✅ |
| V06 | WL above max → 100% flooded | ✅ |
| V07 | Flood monotonic with WL | ✅ |
| V08 | All depth values ≥ 0 | ✅ |
| V09 | Flood % in [0, 100] | ✅ |
| V10 | Rising water monotonic | ✅ |
| V11 | Built-in validate() all pass | ✅ |
| V12 | flood_extent_40m.png exists | ✅ |
| V13 | flood_extent_50m.png exists | ✅ |

## Test Results
Run: `pytest test_flood_inundation.py -v`  
**10/10 tests passed.** See [`screenshot/`](./screenshot/).

## Validation Results
Run: `python validate_flood.py`  
**13/13 validation checks passed.** See [`validation_report.txt`](./validation_report.txt).

## System Architecture

| Module | Key Function | Description |
|--------|-------------|-------------|
| flood_inundation | `generate_dem()` | Synthetic DEM with Gaussian topography |
| flood_inundation | `calculate_flood()` | Flood mask and depth computation |
| flood_inundation | `simulate_rising_water()` | 51-step rising water simulation |
| flood_inundation | `visualize_flood()` | 3-panel terrain + flood overlay visualization |
| test_flood_inundation | `test_*()` | 10 pytest physical boundary tests |
| validate_flood | `validate_*()` | 13 automated physical feasibility checks |

## Physical Constraints Verified

| Constraint | Test Case | Result |
|-----------|----------|--------|
| Water depth >= 0 everywhere | Full DEM grid | min_depth = 0.0 ✅ |
| Flood only below water level | Hill cells | No uphill flooding ✅ |
| Extent increases with water level | +10m step | 37.2% > 10.1% ✅ |
| Zero flood at level below DEM min | level = 29 | Extent = 0 cells ✅ |
| Full flood at level above DEM max | level = 81 | Extent = 100% ✅ |
| Max depth = WL - min elevation | WL=60 | max_depth = 30.0 ✅ |

## Screenshots
See [`screenshot/`](./screenshot/) for test results, validation output, and flood extent plots.

## Prompt Log
See [`prompt_log.md`](./prompt_log.md) for full AI-assisted development documentation (8 prompts, error table, 5 design decisions, reflection).