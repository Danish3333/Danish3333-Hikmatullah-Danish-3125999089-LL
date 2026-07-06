# Prompt 1: Naive Request — SCS-CN Runoff Function

## Student's Prompt (Naive)
```
Write a Python function to calculate SCS-CN runoff.
```

## AI Response (Naive — with errors)

```python
def runoff(P, CN):
    S = 25400 / CN - 254
    Ia = 0.2 * S
    Q = (P - Ia)**2 / (P - Ia + S)
    return Q

# Test
print(runoff(50, 80))  # 13.8
print(runoff(0, 80))   # Error: division by zero?
```

## Errors Identified (Human Review)

| # | Error | Severity | Explanation |
|---|-------|----------|-------------|
| 1 | **Missing P ≤ Ia check** | CRITICAL | When P < Ia, runoff should be 0 (no runoff before initial abstraction is satisfied). The formula `(P-Ia)²/(P-Ia+S)` would produce incorrect negative/positive values |
| 2 | **No Q ≤ P constraint** | CRITICAL | Runoff physically cannot exceed rainfall. Without this check, Q could be > P for certain CN values |
| 3 | **No input validation** | HIGH | CN must be in (0, 100]. CN=0 causes division by zero. P cannot be negative |
| 4 | **No docstring or type hints** | MEDIUM | No documentation explaining what the function does, parameters, or return values |
| 5 | **No edge case for P=0** | MEDIUM | P=0 should return Q=0 immediately without computation |
| 6 | **Integer division risk** | LOW | Using `/` is fine in Python 3, but `25400/CN` should explicitly use float |

## Verdict
The naive prompt produced a function that **fails 3 critical physical constraints** — it would return incorrect results for P < Ia and could violate Q ≤ P.