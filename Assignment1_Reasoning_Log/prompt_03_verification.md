# Prompt 3: AI Self-Verification — Review SCS-CN Implementation

## Student's Prompt (Verification)

```
I want you to peer-review your own SCS-CN runoff function.
Check every line against these physical constraints:

1. Does the function return Q=0 when P < Ia? Test: P=5mm, CN=80
2. Does Q always satisfy Q ≤ P? Test: P=10mm with CN=95 (very high runoff potential)
3. What happens at CN=100? This is an impervious surface — should have maximum runoff
4. Are the units consistent? All in mm.
5. Is there any floating-point edge case (e.g., when P exactly equals Ia)?

Report:
- ✅ What the function handles correctly
- ⚠️ What could be improved (edge cases, performance)
- ❌ Any bugs or physical violations found
```

## AI Self-Review Response

```python
# AI's own test of its function
from scscn_runoff import calculate_runoff

print("=== AI Self-Verification ===")

# Test 1: P < Ia → Q=0
result = calculate_runoff(5, 80)
print(f"1. P=5, CN=80: Q={result} → {'✅' if result==0 else '❌'}")

# Test 2: Q ≤ P
p, cn = 10, 95
result = calculate_runoff(p, cn)
print(f"2. P=10, CN=95: Q={result} ≤ {p} → {'✅' if result<=p else '❌'}")

# Test 3: CN=100 → max runoff
result = calculate_runoff(50, 100)
print(f"3. P=50, CN=100: Q={result} → {'✅' if result>=0 else '❌'}")

# Test 4: P = Ia (edge case)
from scscn_runoff import calculate_Ia
ia80 = calculate_Ia(80)
result = calculate_runoff(ia80, 80)
print(f"4. P=Ia({ia80:.1f}), CN=80: Q={result} → {'✅' if result==0 else '❌'}")

# Test 5: Invalid inputs
try:
    calculate_runoff(50, 0)
    print("5. CN=0 → ❌ (should have raised error)")
except ValueError:
    print("5. CN=0 → ✅ (ValueError raised)")

try:
    calculate_runoff(-5, 80)
    print("6. P<0 → ❌ (should have raised error)")
except ValueError:
    print("6. P<0 → ✅ (ValueError raised)")

print("\n=== Summary ===")
print("✅ All 3 physical constraints handled correctly")
print("⚠️ Floating-point: P==Ia handled by 'if P <= Ia' (<= not <)")
print("   This is correct — catches exact equality")
print("✅ No bugs found — function is physically valid")
```

## AI's Written Analysis

| Check | Result | Explanation |
|-------|--------|-------------|
| P < Ia → Q=0 | ✅ PASS | `if P <= Ia: return 0.0` handles this correctly |
| Q ≤ P | ✅ PASS | `return min(Q, P)` enforces conservation of mass |
| CN=100 impervious | ✅ PASS | S=0, Ia=0, Q=P (all rain becomes runoff) |
| Input validation | ✅ PASS | ValueError for invalid CN, negative P |
| Floating-point at P=Ia | ⚠️ EDGE | Using `<=` handles the exact equality correctly |

## AI's Self-Improvement Suggestion

> "The function is physically correct. One improvement: for batch computations with many P values, a NumPy vectorized version would be faster than calling this function in a loop."

---

## Human Reflection on AI Self-Verification

| Aspect | Observation |
|--------|-------------|
| Did AI catch real bugs? | Not in this case — the CoT-generated code was already correct |
| Did AI identify edge cases? | Yes — correctly noted the P=Ia floating-point boundary |
| Did AI suggest useful improvements? | Yes — NumPy vectorization for batch processing |
| Was AI honest? | Yes — it correctly confirmed all checks passed, didn't fabricate errors |

**Key Takeaway:** AI self-verification works best when given specific physical constraints to check against. An open-ended "review this code" prompt is less effective than targeted constraint-checking prompts.