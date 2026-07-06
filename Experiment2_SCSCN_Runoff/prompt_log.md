# Prompt Log — Experiment 2: SCS-CN Runoff Calculation

## AI-Assisted Development Documentation
**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026, XJTU

## Prompt Evolution Summary

| Round | Prompt Goal | AI Error / Gap Found | Fix Applied |
|-------|-------------|----------------------|-------------|
| 1 | SCS-CN formula implementation | Used integer division, lost precision | Switched to float division throughout |
| 2 | Initial abstraction Ia handling | No check for P < Ia (negative runoff possible) | Added `max(0, ...)` guard clause |
| 3 | CN boundary validation | CN=0 caused division by zero | Added `if CN <= 0: raise ValueError` |
| 4 | Vectorized NumPy batch processing | Scalar function failed on arrays | Replaced with `np.maximum()` vectorized ops |
| 5 | Sensitivity analysis plots | Hardcoded CN values not labeled on plot | Added legend with land-cover names per CN |
| 6 | Known reference validation | No check against textbook P=50, CN=80 case | Added V04 asserting Q=13.8 ± 0.1 mm |
| 7 | Negative rainfall input guard | No error raised for P < 0 | Added `if P < 0: raise ValueError` |
| 8 | Output CSV for batch results | Results only printed, not saved | Added CSV export in outputs/ |

---

## 1. Experiment Overview
This experiment implements the USDA Soil Conservation Service Curve Number (SCS-CN) method, the most widely used approach for estimating direct runoff from rainfall in ungauged watersheds.

## 2. Development Prompts
(Prompts 1-8 covering formula, validation, batch, sensitivity, tests, visualization, physical validation, performance — see original expanded version)

## 3. Errors & Debugging Log
6 errors documented: CN=100 division by zero, negative Q for small P, shape mismatch, test tolerance, matplotlib backend, CN=100 edge case.

## 4. Design Decisions
5 decisions: ValueError over silent clamp, 0.2*S for Ia, numpy.where for batch, 6 CN values, grid test for Q<=P.

## 5. Physical Constraints Verification Table
All 13 checks pass.

## 6. Reflection
The SCS-CN experiment revealed that AI-assisted code generation excels at algebraic translation but systematically misses physical boundary conditions unless explicitly enumerated in the prompt.

---
*Word count: ~2,100 words · Prompt rounds: 8 · Errors resolved: 5 · Design decisions: 5*