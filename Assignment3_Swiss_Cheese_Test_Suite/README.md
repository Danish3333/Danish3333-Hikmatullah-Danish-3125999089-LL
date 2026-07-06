# Assignment 3: The Swiss Cheese Test Suite
**Weight: 20% | Domain: Flood Inundation Mapping**

## Objective
Use AI to generate a flood inundation model, then build a Swiss Cheese test suite that identifies the "Jagged Edges" — places where AI-generated code is wrong, incomplete, or physically invalid. Catch at least one AI hallucination.

## The Swiss Cheese Model
```
Layer 1: Unit Tests     → "Does it run without crashing?"
Layer 2: Boundary Tests → "Does it handle extremes?"
Layer 3: Physical Tests → "Does it obey physics?"
Layer 4: Regression     → "Are results reproducible?"
```

## Known AI Weaknesses to Exploit

| AI Weakness | How to Test |
|-------------|-------------|
| Off-by-one in array indexing | Test min/max elevation cells |
| Forgets NaN/None handling | Inject bad data |
| Physical impossibility | Cross-check depth vs water level |
| Floating-point instability | Test extreme values |
| Boundary at exactly water level | Test elevation == water_level |

## Deliverables

| File | Description |
|------|-------------|
| `test_suite/test_flood_logic.py` | Unit tests |
| `test_suite/test_boundaries.py` | Boundary condition tests |
| `test_suite/test_physical.py` | Physical constraint tests |
| `test_suite/test_regression.py` | Regression tests |
| `hallucination_report/detected_hallucinations.md` | Caught AI errors |
| `prompt_log.md` | AI interaction documentation |

## Grading Criteria

| Criterion | Weight |
|-----------|--------|
| Test Suite Completeness | 35% |
| Hallucination Detection | 30% |
| Layer Design | 20% |
| Documentation | 15% |