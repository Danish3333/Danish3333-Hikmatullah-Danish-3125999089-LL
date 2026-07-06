"""
Assignment 4: Final Capstone Project — Reservoir Dispatch Optimization
======================================================================
Complete mini-application integrating all course skills:
- Core reservoir simulation engine
- Multi-objective optimizer (hydropower + ecology)
- Pareto frontier visualization
- Validation module
- CSV export
"""

import numpy as np
from scipy.optimize import minimize
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os
import csv

# =============================================================================
# CONFIGURATION
# =============================================================================
V0 = 500000
V_MIN = 100000
V_MAX = 1000000
Q_ECO = 10.0
Q_MAX = 100.0
H = 30.0; ETA = 0.85; RHO = 1000; G = 9.81
K_HYDRO = ETA * RHO * G * H / 1000
INFLOW = np.array([15, 12, 10, 8, 12, 15, 18])
PRICE = np.array([0.08, 0.08, 0.08, 0.08, 0.10, 0.12, 0.10])
DT = 86400; T = 7

# =============================================================================
# CORE SIMULATION
# =============================================================================
def compute_storage(releases, inflow=None):
    """Compute storage trajectory from release schedule."""
    if inflow is None: inflow = INFLOW
    storage = np.zeros(T+1); storage[0] = V0
    for t in range(T):
        storage[t+1] = storage[t] + (inflow[t] - releases[t]) * DT
    return storage

def revenue(releases):
    power = K_HYDRO * np.asarray(releases, float)
    return float(np.sum(power * 24 * PRICE))

def eco_deficit(releases):
    return float(np.sum(np.maximum(0, Q_ECO - np.asarray(releases, float))))

# =============================================================================
# OPTIMIZER
# =============================================================================
def optimize_max_revenue():
    bounds = [(Q_ECO, Q_MAX)] * T
    constraints = []
    for t in range(T+1):
        constraints.append({'type':'ineq','fun': lambda r,i=t: compute_storage(r)[i]-V_MIN})
        constraints.append({'type':'ineq','fun': lambda r,i=t: V_MAX-compute_storage(r)[i]})
    res = minimize(lambda r: -revenue(r), np.full(T,20.0), method='SLSQP',
                   bounds=bounds, constraints=constraints, options={'maxiter':500})
    return np.clip(res.x, Q_ECO, Q_MAX), compute_storage(res.x)

def optimize_pareto(w_rev, w_eco):
    """Multi-objective optimization with weighted objectives."""
    bounds = [(0, Q_MAX)] * T
    constraints = []
    for t in range(T+1):
        constraints.append({'type':'ineq','fun': lambda r,i=t: V_MAX-compute_storage(r)[i]})
        constraints.append({'type':'ineq','fun': lambda r,i=t: compute_storage(r)[i]-V_MIN})
    REV_MAX = K_HYDRO*24*Q_MAX*sum(PRICE)
    DEF_MAX = Q_ECO * T
    def obj(q):
        return -w_rev*revenue(q)/REV_MAX + w_eco*eco_deficit(q)/DEF_MAX
    best, best_f = None, np.inf
    for q0 in [np.clip(INFLOW.astype(float),0,Q_MAX), np.full(T,Q_ECO+2)]:
        res = minimize(obj, q0, method='SLSQP', bounds=bounds,
                       constraints=constraints, options={'maxiter':2000})
        if res.fun < best_f: best_f, best = res.fun, res
    releases = np.clip(best.x, 0, Q_MAX)
    storage = compute_storage(releases)
    valid = all(V_MIN-1 <= s <= V_MAX+1 for s in storage)
    return releases, revenue(releases), eco_deficit(releases), valid

# =============================================================================
# VISUALIZATION
# =============================================================================
def plot_pareto():
    pareto = []
    for w in np.linspace(0,1,20):
        r,e,d,v = optimize_pareto(1-w, w)
        if v: pareto.append((w,r,e,d))
    if not pareto: return
    ws = np.array([p[0] for p in pareto])
    revs = np.array([p[2] for p in pareto])/1000
    defs = np.array([p[3] for p in pareto])
    fig, axes = plt.subplots(1,2,figsize=(14,5))
    sc = axes[0].scatter(defs, revs, c=ws, cmap='RdYlGn_r', s=80, edgecolors='k')
    axes[0].set_xlabel('Ecological Deficit'); axes[0].set_ylabel('Revenue (k$)')
    axes[0].set_title('Pareto Frontier'); axes[0].grid(True,alpha=0.3)
    plt.colorbar(sc, ax=axes[0], label='Ecology weight')
    axes[1].plot(ws, revs, 'b-o', ms=5)
    axes[1].set_xlabel('Ecology Weight'); axes[1].set_ylabel('Revenue (k$)')
    axes[1].set_title('Revenue vs Ecology Weight'); axes[1].grid(True,alpha=0.3)
    fig.suptitle('Reservoir Dispatch — Capstone Project', fontsize=14, fontweight='bold')
    plt.tight_layout()
    os.makedirs('outputs', exist_ok=True)
    plt.savefig('outputs/pareto_frontier.png', dpi=150, bbox_inches='tight')
    plt.close()

# =============================================================================
# VALIDATION & EXPORT
# =============================================================================
def validate(releases, storage):
    lines = []
    lines.append('='*60+'\nVALIDATION REPORT\n'+'='*60)
    ro = np.all(releases >= Q_ECO-1e-6) and np.all(releases <= Q_MAX+1e-6)
    so = np.all(storage >= V_MIN-1) and np.all(storage <= V_MAX+1)
    mo = all(abs(storage[t+1]-(storage[t]+(INFLOW[t]-releases[t])*DT))<1 for t in range(T))
    lines.append(f'Release bounds: {"PASS" if ro else "FAIL"}')
    lines.append(f'Storage bounds: {"PASS" if so else "FAIL"}')
    lines.append(f'Mass balance:   {"PASS" if mo else "FAIL"}')
    lines.append(f'Overall:        {"ALL PASS" if (ro and so and mo) else "FAIL"}')
    lines.append(f'\nTotal Revenue: ${revenue(releases):,.2f}')
    lines.append(f'Eco Deficit:   {eco_deficit(releases):.2f} m3/s·day')
    report = '\n'.join(lines)
    os.makedirs('outputs', exist_ok=True)
    with open('outputs/validation_report.txt','w') as f: f.write(report)
    return ro and so and mo

def export_schedule(releases, storage):
    dates = [(datetime(2024,1,1)+timedelta(days=i)).strftime('%Y-%m-%d') for i in range(T)]
    os.makedirs('outputs', exist_ok=True)
    with open('outputs/optimal_schedule.csv','w',newline='') as f:
        w = csv.writer(f)
        w.writerow(['Day','Date','Inflow_m3s','Release_m3s','Storage_m3','Daily_Revenue_USD'])
        for i in range(T):
            w.writerow([i+1,dates[i],f'{INFLOW[i]:.1f}',f'{releases[i]:.4f}',
                       f'{storage[i+1]:.0f}',f'{K_HYDRO*releases[i]*24*PRICE[i]:.2f}'])

# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':
    print("="*60)
    print("RESERVOIR DISPATCH OPTIMIZATION — CAPSTONE PROJECT")
    print("="*60)

    # Optimize
    releases, storage = optimize_max_revenue()
    print(f"\nOptimal schedule found:")
    for i in range(T):
        print(f"  Day {i+1}: Release={releases[i]:.4f} m3/s, Storage={storage[i+1]:,.0f} m3")

    # Validate
    ok = validate(releases, storage)
    print(f"\nValidation: {'ALL PASS' if ok else 'FAILED'}")

    # Export
    export_schedule(releases, storage)
    print("Exported: outputs/optimal_schedule.csv")

    # Pareto
    plot_pareto()
    print("Generated: outputs/pareto_frontier.png")

    print(f"\nTotal Revenue: ${revenue(releases):,.2f}")
    print(f"Eco Deficit:   {eco_deficit(releases):.2f}")
    print("="*60)