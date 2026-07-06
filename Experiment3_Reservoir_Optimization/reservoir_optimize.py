"""
Experiment 3: Water Resources Optimization - Reservoir Dispatch
==============================================================
Multi-objective optimization for 7-day reservoir release scheduling.
- Maximize hydropower revenue
- Minimize ecological deficit
- Pareto frontier analysis
- Monte Carlo uncertainty analysis
"""

import numpy as np
import os
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import time

# Reservoir parameters
V0 = 500000       # Initial storage (m3)
V_min = 100000    # Min storage (m3)
V_max = 1000000   # Max storage (m3)
Q_eco = 10.0      # Min ecological release (m3/s)
Q_max = 100.0     # Max release (m3/s)
H = 30.0          # Hydraulic head (m)
eta = 0.85        # Turbine efficiency
rho = 1000        # Water density (kg/m3)
g = 9.81          # Gravity (m/s2)
K_HYDRO = eta * rho * g * H / 1000  # kW/(m3/s)

# 7-day forecast
inflow = np.array([15, 12, 10, 8, 12, 15, 18])  # m3/s
price = np.array([0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10])  # $/kWh
dt = 86400  # seconds per day
T = 7
TOL = 500


def compute_storage(releases):
    """Compute storage trajectory from release schedule."""
    storage = np.zeros(T + 1)
    storage[0] = V0
    for t in range(T):
        storage[t + 1] = storage[t] + (inflow[t] - releases[t]) * dt
    return storage


def compute_total_revenue(releases):
    """Compute total hydropower revenue."""
    power_kw = K_HYDRO * np.asarray(releases, dtype=float)
    return float(np.sum(power_kw * 24 * price))


def compute_eco_deficit(releases):
    """Compute ecological flow deficit."""
    return float(np.sum(np.maximum(0.0, Q_eco - np.asarray(releases, dtype=float))))


# ---- Optimization ----
bounds = [(Q_eco, Q_max) for _ in range(T)]
x0 = np.full(T, 20.0)

constraints = []
for t in range(T + 1):
    constraints.append({'type': 'ineq', 'fun': lambda r, i=t: compute_storage(r)[i] - V_min - TOL})
    constraints.append({'type': 'ineq', 'fun': lambda r, i=t: V_max - compute_storage(r)[i] - TOL})

def objective_max_revenue(releases):
    return -compute_total_revenue(releases)

result = minimize(objective_max_revenue, x0, method='SLSQP', bounds=bounds, constraints=constraints)

optimal_releases = np.clip(result.x, Q_eco, Q_max)
optimal_storage = compute_storage(optimal_releases)
total_revenue = compute_total_revenue(optimal_releases)
eco_deficit = compute_eco_deficit(optimal_releases)

# Save schedule
start_date = datetime(2024, 1, 1)
dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(T)]

header = "Day,Date,Inflow_m3s,Release_m3s,Storage_m3,Price_per_kWh,Daily_Revenue_USD"
rows = []
for i in range(T):
    daily_rev = K_HYDRO * optimal_releases[i] * 24 * price[i]
    rows.append(f"{i+1},{dates[i]},{inflow[i]:.1f},{optimal_releases[i]:.4f},{optimal_storage[i+1]:.0f},{price[i]:.2f},{daily_rev:.2f}")

os.makedirs('outputs', exist_ok=True)
with open('outputs/optimal_schedule.csv', 'w') as f:
    f.write(header + "\n" + "\n".join(rows) + "\n")

# ---- Trade-off Analysis (Pareto) ----
_REV_UPPER = K_HYDRO * 24.0 * Q_max * sum(price)
_DEF_UPPER = Q_eco * T

def optimize_multi_objective(w_revenue, w_ecology):
    def objective(q):
        rev = compute_total_revenue(q)
        deficit = compute_eco_deficit(q)
        return -w_revenue * rev / _REV_UPPER + w_ecology * deficit / _DEF_UPPER
    bounds_mo = [(0.0, Q_max)] * T
    constraints_mo = []
    for t in range(T + 1):
        constraints_mo.append({'type': 'ineq', 'fun': lambda r, i=t: V_max - compute_storage(r)[i]})
        constraints_mo.append({'type': 'ineq', 'fun': lambda r, i=t: compute_storage(r)[i] - V_min})
    initial_guesses = [
        np.clip(np.asarray(inflow, dtype=float), 0.0, Q_max),
        np.full(T, Q_eco + 2.0),
    ]
    best_res = None
    best_obj = np.inf
    for q0 in initial_guesses:
        res = minimize(objective, q0, method="SLSQP", bounds=bounds_mo, constraints=constraints_mo, options={"ftol": 1e-9, "maxiter": 2000})
        if res.fun < best_obj:
            best_obj = res.fun
            best_res = res
        if res.success:
            break
    rel = best_res.x
    stor = compute_storage(rel)
    ok = all(V_min - 1.0 <= s <= V_max + 1.0 for s in stor)
    return {"releases": rel, "revenue": compute_total_revenue(rel), "ecological_deficit": compute_eco_deficit(rel), "success": ok}

pareto_points = []
for w_eco in np.linspace(0.0, 1.0, 20):
    r = optimize_multi_objective(1.0 - w_eco, w_eco)
    if r["success"]:
        pareto_points.append(r)

if pareto_points:
    revenues = np.array([p["revenue"] for p in pareto_points])
    deficits = np.array([p["ecological_deficit"] for p in pareto_points])
    w_ecos_arr = np.linspace(0, 1, len(revenues))

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sc = axes[0].scatter(deficits, revenues / 1000, c=w_ecos_arr, cmap="RdYlGn_r", s=90, zorder=5, edgecolors="k", linewidths=0.5)
    axes[0].plot(deficits, revenues / 1000, "k--", alpha=0.25, linewidth=1)
    plt.colorbar(sc, ax=axes[0], label="Ecology weight")
    axes[0].set_xlabel("Ecological Deficit (m3/s * day)", fontsize=12)
    axes[0].set_ylabel("Total Revenue (k$)", fontsize=12)
    axes[0].set_title("Pareto Frontier: Revenue vs Ecological Deficit", fontsize=12, fontweight="bold")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(w_ecos_arr, revenues / 1000, "b-o", markersize=6, label="Revenue")
    zero_def_mask = deficits < 0.01
    rev_eco = revenues[zero_def_mask].max() if zero_def_mask.any() else revenues[-1]
    cost = float(revenues.max() - rev_eco)
    axes[1].axhline(rev_eco / 1000, color="green", linestyle="--", linewidth=1.5, label=f"Revenue (eco protected): ${rev_eco/1000:.1f}k")
    axes[1].fill_between(w_ecos_arr, np.full_like(w_ecos_arr, rev_eco / 1000), revenues / 1000, where=(revenues > rev_eco), alpha=0.25, color="red", label=f"Cost of ecology = ${cost:.0f}")
    axes[1].set_xlabel("Ecology Weight", fontsize=12)
    axes[1].set_ylabel("Total Revenue (k$)", fontsize=12)
    axes[1].set_title("Revenue vs Ecology Weight", fontsize=12, fontweight="bold")
    axes[1].legend(fontsize=9, loc="lower left")
    axes[1].grid(True, alpha=0.3)

    fig.suptitle("Reservoir Dispatch - Multi-Objective Trade-off Analysis", fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("outputs/tradeoff_analysis.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

# ---- Validation Report ----
lines = []
lines.append("=" * 65)
lines.append("RESERVOIR DISPATCH OPTIMIZATION - VALIDATION REPORT")
lines.append("=" * 65)
lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
lines.append("")
lines.append("OPTIMAL RELEASE SCHEDULE")
lines.append("-" * 50)
lines.append(f"  {'Day':>4} {'Inflow':>8} {'Release':>10} {'Storage':>11} {'Price':>7} {'Revenue':>10}")
for i in range(T):
    daily_rev = K_HYDRO * optimal_releases[i] * 24 * price[i]
    lines.append(f"  {i+1:>4} {inflow[i]:>8.1f} {optimal_releases[i]:>10.4f} {optimal_storage[i+1]:>9,.0f} {price[i]:>7.2f} {daily_rev:>9,.2f}")
lines.append(f"\n  TOTAL REVENUE: ${total_revenue:,.2f}")
lines.append("")
lines.append("CONSTRAINT VERIFICATION")
lines.append("-" * 50)
release_ok = Q_eco <= min(optimal_releases) + 1e-6 and max(optimal_releases) <= Q_max + 1e-6
storage_ok = V_min <= min(optimal_storage) + 1e-6 and max(optimal_storage) <= V_max + 1e-6
mass_ok = all(abs(optimal_storage[t + 1] - (optimal_storage[t] + (inflow[t] - optimal_releases[t]) * dt)) < 1 for t in range(T))
eco_violations = int(sum(optimal_releases < Q_eco - 1e-6))
p = lambda ok: "PASS" if ok else "FAIL"
lines.append(f"  Release bounds  : {p(release_ok)}")
lines.append(f"  Storage bounds  : {p(storage_ok)}")
lines.append(f"  Mass balance    : {p(mass_ok)}")
lines.append(f"  Eco violations  : {eco_violations}")
lines.append(f"  Feasible        : {'YES' if (release_ok and storage_ok and mass_ok) else 'NO'}")

report = "\n".join(lines)
with open('outputs/validation_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print("All outputs generated successfully.")
print(f"  Total Revenue: ${total_revenue:,.2f}")
print(f"  Ecological Deficit: {eco_deficit:.2f}")