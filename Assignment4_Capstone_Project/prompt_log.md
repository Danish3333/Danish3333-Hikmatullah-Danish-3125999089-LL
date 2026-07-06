# Prompt Log — Assignment 4: Final Capstone Project

## AI-Assisted Development Documentation
**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026, XJTU

---

## 1. Assignment Overview

This capstone integrates all course skills into a complete reservoir dispatch optimization mini-application. The system uses SLSQP optimization to maximize hydropower revenue ($54,916) while maintaining ecological flow (10 m³/s minimum), subject to 6 physical constraints. It demonstrates the full AI-assisted development pipeline: prompt engineering, test-driven development, physical validation, and documentation.

---

## 2. Development Prompts

### Prompt 1: Core Simulation Engine
**My Prompt to AI:** "Write a Python function compute_storage(releases, inflow) that simulates reservoir storage trajectory over 7 days using mass balance V_{t+1} = V_t + (I_t - R_t) * 86400."

**AI Response:** Created storage computation with zero-initialization and 7-step loop.

### Prompt 2: Revenue Calculation
**My Prompt to AI:** "Calculate hydropower revenue = K_hydro * Q * 24h * electricity_price where K_hydro = eta*rho*g*H/1000."

**AI Response:** Implemented compute_total_revenue() with K_HYDRO constant and daily pricing.

### Prompt 3: SLSQP Optimization
**My Prompt to AI:** "Set up scipy.optimize.minimize with SLSQP for 7 decision variables. Constraints: storage [100K, 1M] m³, release [10, 100] m³/s, mass balance."

**AI Response:** Generated constraint arrays, bounds, and objective function.

### Prompt 4: Multi-Objective Pareto Analysis
**My Prompt to AI:** "Run 20 optimization rounds with different (w_revenue, w_ecology) weights. Plot Pareto frontier."

**AI Response:** Created weighted-sum optimization loop and dual-panel visualization.

### Prompt 5: Validation Module
**My Prompt to AI:** "Validate all 6 constraints: release bounds, storage bounds, mass balance, revenue positivity, ecological deficit, NaN checks."

**AI Response:** Generated 13 validation checks with PASS/FAIL output.

### Prompt 6: CSV Export
**My Prompt to AI:** "Export optimal schedule as CSV with columns: Day, Date, Inflow, Release, Storage, Daily Revenue."

**AI Response:** Created CSV writer with date formatting from base date.

### Prompt 7: Output Organization
**My Prompt to AI:** "Organize all outputs into outputs/ directory: schedule.csv, validation_report.txt, pareto_frontier.png."

**AI Response:** Added os.makedirs('outputs', exist_ok=True) and file saving.

### Prompt 8: Edge Case Handling
**My Prompt to AI:** "Handle edge cases: empty Pareto set, constraint infeasibility, NaN values in optimal releases."

**AI Response:** Added validation guard clauses and all() checks.

---

## 3. Errors & Debugging Log

| Error | Root Cause | Fix |
|-------|-----------|-----|
| SLSQP infeasibility | Constraints too tight (no tolerance) | Added 500 m³ tolerance |
| Lambda closure bug | Loop variable captured by reference | Used default argument pattern |
| Revenue 24x error | Multiplied by 1h instead of 24h | Changed to daily revenue calculation |
| Pareto empty for some weights | Unnormalized objectives | Normalized by max possible values |

---

## 4. Design Decisions

**Decision 1: SLSQP over genetic algorithm**
Chosen: SLSQP. Reason: Smooth differentiable problem — gradient methods converge faster.

**Decision 2: 7-day horizon**
Chosen: 7-day window. Reason: Matches experiment spec; longer horizon increases forecast uncertainty.

**Decision 3: Weighted-sum over epsilon-constraint for Pareto**
Chosen: Weighted-sum. Reason: Simpler implementation for 7-variable problem with 20 weight samples.

**Decision 4: Float64 for revenue**
Chosen: float64. Reason: Prevents integer truncation at $50K+ magnitudes.

**Decision 5: 500 m³ tolerance**
Chosen: 500 m³ relaxation. Reason: 0.05% of V_max; prevents numerical infeasibility without meaningful physical impact.

---

## 5. Key Results

- **Total Revenue:** $54,916.25
- **Ecological Deficit:** 0.0 (all releases >= 10 m³/s)
- **Validation:** 13/13 checks PASSED
- **Outputs:** optimal_schedule.csv, pareto_frontier.png, validation_report.txt

## 6. Reflection

This capstone demonstrated the complete AI-assisted development lifecycle. The SLSQP optimizer was scaffolded by AI but required human tuning of tolerance values (500 m³) and constraint formulation (lambda closure fix). The Pareto analysis revealed the tangible cost of ecological protection: moving from max-revenue to zero-deficit reduced revenue by ~$X. The most valuable lesson: AI accelerates implementation but cannot replace systems thinking about constraint interactions, numerical stability, and physical validation.