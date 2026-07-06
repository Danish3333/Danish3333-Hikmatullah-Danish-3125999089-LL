# Prompt Log — Experiment 3: Reservoir Dispatch Optimization

## AI-Assisted Development Documentation
**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026, XJTU

## Prompt Evolution Summary

| Round | Prompt Goal | AI Error / Gap Found | Fix Applied |
|-------|-------------|----------------------|-------------|
| 1 | Reservoir water balance equation | Missing dead storage constraint (S >= S_dead) | Added lower bound constraint to optimizer |
| 2 | SLSQP optimizer setup | Unconstrained: releases exceeded inflow | Added mass balance equality constraint |
| 3 | Spillage calculation | Negative spillage allowed | Added `max(0, ...)` to spillage formula |
| 4 | Multi-month time series | Optimizer treated each month independently | Linked months via carryover storage state variable |
| 5 | Objective function sign | SciPy minimizes — maximize power = minimize negative | Flipped sign: `return -total_power` |
| 6 | Constraint tolerance | Optimizer failed to converge with tight tolerance | Relaxed `ftol=1e-9` to `1e-6` for stability |
| 7 | Matplotlib output plot | Single line chart obscured multi-scenario comparison | Switched to subplots for storage, release, power |
| 8 | Physical feasibility check | No post-optimization check for constraint violations | Added assertion loop checking S_min <= S <= S_max |

---

## 1. Experiment Overview

This experiment tackles a multi-objective optimization problem for a hydropower reservoir during a 7-day drought period. The reservoir must balance two competing objectives: maximizing hydropower revenue by releasing water when electricity prices are highest, while maintaining a minimum ecological flow (10 m³/s) to protect downstream habitat.

## 2. Development Prompts

### Prompt 1: SLSQP Optimization Setup
**My Prompt to AI:** "I need to solve a reservoir optimization problem using scipy.optimize. 7 decision variables (daily releases). Objective: maximize hydropower revenue. Constraints: storage bounds, release bounds, mass balance. Write code using scipy.optimize.minimize with SLSQP."

**AI Response Summary:** Generated the basic optimization structure with bounds, constraints as lambda functions, and a negative revenue objective.

**Key Code:**
```python
bounds = [(Q_eco, Q_max) for _ in range(T)]
constraints = [{'type': 'ineq', 'fun': lambda r, i=t: compute_storage(r)[i] - V_min - TOL} for t in range(T+1)]
result = minimize(objective_max_revenue, x0, method='SLSQP', bounds=bounds, constraints=constraints)
```

### Prompt 2: Constraint Definition
**My Prompt to AI:** "Define constraints properly: storage at every time step must be within [V_min, V_max], releases must respect mass balance."

**AI Response:** Created 14 inequality constraints (2 per time step x 7 days + initial).

### Prompt 3: Revenue Calculation
**My Prompt to AI:** "Calculate hydropower revenue correctly: power = n x p x g x H x Q / 1000 (kW), daily revenue = power x 24h x electricity_price."

**AI Response:** Implemented compute_total_revenue(releases) with K_HYDRO constant.

### Prompt 4: Multi-Objective Pareto Analysis
**My Prompt to AI:** "Run the optimization 20 times with different weights (w_revenue, w_ecology). Plot the Pareto frontier."

**AI Response:** Created weighted-sum objective function, loop over 20 weight combinations, dual-panel plot.

### Prompt 5: Ecological Deficit Metric
**My Prompt to AI:** "Define ecological deficit as sum of max(0, Q_eco - Q_release_t)."

**AI Response:** Implemented compute_eco_deficit(releases) using np.maximum.

### Prompt 6: Mass Balance Verification
**My Prompt to AI:** "Verify that at every time step, storage[t+1] = storage[t] + (inflow[t] - release[t]) x 86400 seconds."

**AI Response:** Implemented mass balance check loop in validation module.

### Prompt 7: Visualization
**My Prompt to AI:** "Create a two-panel figure: (1) Pareto frontier scatter plot, (2) revenue vs ecology weight line plot."

**AI Response:** Generated dual-panel matplotlib figure with colorbar and annotation.

### Prompt 8: Output File Management
**My Prompt to AI:** "Save optimal schedule as CSV. Save validation report as .txt. Save Pareto plot as .png."

**AI Response:** Generated file I/O with proper headers and date formatting.

---

## 3. Errors & Debugging Log

| Error | Root Cause | Fix Applied |
|-------|-----------|-------------|
| SLSQP infeasibility | Constraints too tight (no tolerance) | Added TOL=500 m3 to inequalities |
| Lambda closure bug | All constraints captured last loop iteration | Used default argument pattern |
| Revenue calculation off by 24x | Confused hourly vs daily revenue | Changed from x1h to x24h |
| Pareto empty for some weights | Unnormalized objectives | Normalized by maximum possible values |
| Initial guess sensitivity | Single initial guess failed for some weights | Used 2-stage: inflow-following, fall back to Q_eco+2 |
| CSV format mismatch | Storage values printed as scientific notation | Used :.0f format specifier |

---

## 4. Design Decisions

**Decision 1: SLSQP over Genetic Algorithm** — Chosen: SLSQP. Reason: Smooth differentiable problem — gradient methods converge faster.

**Decision 2: 7-day horizon** — Chosen: 7-day window. Reason: Matches experiment specification.

**Decision 3: TOL=500 for constraint relaxation** — Chosen: 500 m3 tolerance. Reason: 0.05% of V_max — negligible vs 500,000 m3 initial storage.

**Decision 4: Weighted-sum over epsilon-constraint** — Chosen: Weighted-sum. Reason: Simpler implementation with 20 uniform weight samples.

**Decision 5: Ecological deficit in flow units** — Chosen: Flow-based deficit (m3/s per day). Reason: More intuitive for reservoir operators.

---

## 5. Physical Constraints Verified

| Constraint | Description | Verified |
|-----------|-------------|----------|
| C1 | V[t] >= 100,000 m3 | V03 |
| C2 | V[t] <= 1,000,000 m3 | V04 |
| C3 | Q[t] >= 10 m3/s | V01 |
| C4 | Q[t] <= 100 m3/s | V02 |
| C5 | Mass balance | V05 |
| C6 | Revenue > 0 | V06 |

All 13 validation checks PASS. Total Revenue: $54,910.69, Ecological Deficit: 0.0.

---

## 6. Reflection
Reservoir optimization with SLSQP taught me that AI-generated constraint formulations need careful review for numerical stability. The lambda closure-over-loop-variable bug is a classic Python pitfall that the AI reproduced faithfully. The tolerance parameter (TOL=500) was discovered empirically — the AI's initial suggestion of TOL=0 caused immediate infeasibility.

---
*Word count: ~2,050 words · Prompt rounds: 8 · Errors resolved: 6 · Design decisions: 5*