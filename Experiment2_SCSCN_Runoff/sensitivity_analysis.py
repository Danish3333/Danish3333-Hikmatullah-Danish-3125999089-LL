"""SCS-CN Sensitivity Analysis - Visualizations."""
from scscn_runoff import calculate_runoff
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ---- Part 1: CN vs Runoff for fixed P=50mm ----
P_fixed = 50
CN_values = [60, 70, 80, 90, 95, 100]
Q_values = [calculate_runoff(P_fixed, cn) for cn in CN_values]

fig1, ax1 = plt.subplots(figsize=(8, 5))
ax1.plot(CN_values, Q_values, 'b-o', linewidth=2, markersize=8)
ax1.set_xlabel('Curve Number (CN)', fontsize=12)
ax1.set_ylabel('Runoff Q (mm)', fontsize=12)
ax1.set_title(f'SCS-CN Sensitivity Analysis\nRunoff vs CN for P={P_fixed} mm', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
for cn, q in zip(CN_values, Q_values):
    ax1.annotate(f'{q:.1f}', (cn, q), textcoords='offset points', xytext=(0, 12), ha='center', fontsize=9)
fig1.tight_layout()
fig1.savefig('outputs/SCS-CN Sensitivity Analysis.png', dpi=150)
print("Saved: outputs/SCS-CN Sensitivity Analysis.png")

# ---- Part 2: Rainfall vs Runoff for different CN ----
P_range = np.linspace(0, 200, 100)
CN_compare = [60, 70, 80, 90, 95]

fig2, ax2 = plt.subplots(figsize=(10, 6))
for cn in CN_compare:
    Q_range = [calculate_runoff(p, cn) for p in P_range]
    ax2.plot(P_range, Q_range, linewidth=2, label=f'CN={cn}')

ax2.plot(P_range, P_range, 'k--', linewidth=1, alpha=0.5, label='Q=P (100% runoff)')
ax2.set_xlabel('Rainfall P (mm)', fontsize=12)
ax2.set_ylabel('Runoff Q (mm)', fontsize=12)
ax2.set_title('Rainfall-Runoff Relationship for Different CN Values', fontsize=14, fontweight='bold')
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 200)
ax2.set_ylim(0, 200)
fig2.tight_layout()
fig2.savefig('outputs/Rainfall-Runoff Relationship for Different CN Values.png', dpi=150)
print("Saved: outputs/Rainfall-Runoff Relationship for Different CN Values.png")

print("\nAnalysis complete. Key observations:")
print(f"  - At P={P_fixed}mm, CN=60: Q={calculate_runoff(50,60):.1f}mm, CN=100: Q={calculate_runoff(50,100):.1f}mm")
print(f"  - Higher CN always produces more runoff (less infiltration)")
print(f"  - Runoff is non-linear: threshold at Ia before runoff begins")