# Prompt 2: Chain-of-Thought (CoT) — SCS-CN Runoff Function

## Student's Prompt (CoT)

```
You are a hydrology expert. I need to implement the SCS-CN runoff formula in Python.

Think step by step:
1. First, recall the SCS-CN formula:
   - S = (25400 / CN) - 254  (potential maximum retention in mm)
   - Ia = 0.2 × S  (initial abstraction)
   - Q = (P - Ia)² / (P - Ia + S)  when P > Ia, otherwise Q = 0

2. What are the physical boundary conditions?
   - If P = 0: Q must be 0 (no rainfall = no runoff)
   - If P ≤ Ia: Q must be 0 (rainfall hasn't overcome initial abstraction)
   - Q must never exceed P (conservation of mass)
   - CN must be in range (0, 100]
   - P must be non-negative

3. Verify with known example: P=50mm, CN=80
   S = 25400/80 - 254 = 317.5 - 254 = 63.5 mm
   Ia = 0.2 × 63.5 = 12.7 mm
   Q = (50 - 12.7)² / (50 - 12.7 + 63.5) = 1391.29 / 100.8 ≈ 13.8 mm
   Check: 13.8 ≤ 50 ✓

4. Write the function with:
   - Type hints (float inputs and return)
   - Full docstring explaining formula, parameters, return value
   - Input validation with clear error messages
   - All boundary conditions handled
```

## AI Response (CoT — Correct)

```python
def calculate_runoff(P: float, CN: float) -> float:
    """
    Calculate runoff depth using the SCS-CN method.

    Args:
        P:  Rainfall depth in mm
        CN: Curve Number (0-100)

    Returns:
        Runoff depth in mm

    Raises:
        ValueError: If CN <= 0 or CN > 100 or P < 0
    """
    if CN <= 0 or CN > 100:
        raise ValueError(f"CN must be in range (0, 100], got {CN}")
    if P < 0:
        raise ValueError(f"P must be non-negative, got {P}")

    if P == 0:
        return 0.0

    S = (25400.0 / CN) - 254.0
    Ia = 0.2 * S

    if P <= Ia:
        return 0.0

    Q = (P - Ia) ** 2 / (P - Ia + S)

    return min(Q, P)  # Q never exceeds P
```

## Comparison: Naive vs CoT

| Criterion | Naive Prompt | CoT Prompt |
|-----------|-------------|------------|
| Boundary conditions handled | ❌ 0/3 | ✅ 3/3 |
| Input validation | ❌ None | ✅ CN range, P≥0 |
| Type hints | ❌ None | ✅ float annotations |
| Docstring | ❌ None | ✅ Full docstring |
| Verified with example | ❌ Not mentioned | ✅ Step-by-step calculation |
| Production-ready | ❌ No | ✅ Yes |

## Verdict
**CoT prompting increased code quality from ~40% to 100%.** The AI followed the step-by-step reasoning template and produced a complete, validated function with all physical constraints satisfied.