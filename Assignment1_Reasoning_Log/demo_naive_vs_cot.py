"""
Assignment 1 Demonstration: Naive vs CoT Prompting — Run This!
==============================================================
This script demonstrates the value of Chain-of-Thought prompting by running
the NAIVE SCS-CN function (from prompt_01) and the CoT function (from prompt_02)
against the same test cases, showing which one fails.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Experiment2_SCSCN_Runoff'))
from scscn_runoff import calculate_runoff as cot_calculate_runoff

# ---- NAIVE FUNCTION (from prompt_01_naive.md — deliberately broken) ----
def naive_runoff(P, CN):
    """BUG: Missing P<=Ia check, no Q<=P, no input validation."""
    S = 25400 / CN - 254
    Ia = 0.2 * S
    Q = (P - Ia)**2 / (P - Ia + S)
    return Q

# ---- TEST CASES ----
tests = [
    ("P=50, CN=80 (known example)", 50, 80, 13.8),
    ("P=0, CN=80 (no rain)", 0, 80, 0.0),
    ("P=5, CN=80 (P < Ia)", 5, 80, 0.0),
    ("P=10, CN=95 (high runoff)", 10, 95, None),  # Just check Q≤P
]

print("=" * 70)
print("ASSIGNMENT 1: NAIVE vs CoT — LIVE DEMONSTRATION")
print("=" * 70)

naive_pass = 0
cot_pass = 0
total = len(tests)

for name, P, CN, expected in tests:
    print(f"\n{'─'*50}")
    print(f"Test: {name}")

    # Naive
    try:
        nq = naive_runoff(P, CN)
        if expected is not None:
            n_ok = abs(nq - expected) < 0.15
        else:
            n_ok = nq <= P
        status = "PASS" if n_ok else "FAIL"
        if n_ok: naive_pass += 1
        print(f"  NAIVE: Q={nq:.2f} [{status}]")
        if not n_ok:
            print(f"    → BUG: Expected ~{expected}, got {nq:.2f}")
    except Exception as e:
        print(f"  NAIVE: CRASHED — {e}")

    # CoT
    try:
        cq = cot_calculate_runoff(P, CN)
        if expected is not None:
            c_ok = abs(cq - expected) < 0.15
        else:
            c_ok = cq <= P
        status = "PASS" if c_ok else "FAIL"
        if c_ok: cot_pass += 1
        print(f"  CoT:   Q={cq:.2f} [{status}]")
    except Exception as e:
        print(f"  CoT:   CRASHED — {e}")

print(f"\n{'='*70}")
print(f"RESULTS: Naive={naive_pass}/{total}  |  CoT={cot_pass}/{total}")
print(f"{'='*70}")

if naive_pass < total:
    print(f"\n❌ Naive failed {total - naive_pass} test(s) — missing boundary conditions")
if cot_pass == total:
    print(f"✅ CoT passed all tests — all 3 physical constraints handled")

print(f"\nConclusion: CoT prompting improved code from ~{naive_pass/total*100:.0f}% to {cot_pass/total*100:.0f}% correct.")
print(f"This is why structured prompts with domain constraints matter.")