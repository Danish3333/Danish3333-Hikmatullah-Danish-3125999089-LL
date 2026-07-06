# Assignment 1: The Reasoning Log — Final Comparison Report

## Naive vs Chain-of-Thought: SCS-CN Runoff Function

---

## Part 1: The Two Prompts

### Naive Prompt
```
Write a Python function to calculate SCS-CN runoff.
```

### CoT Prompt
```
You are a hydrology expert. I need to implement the SCS-CN runoff formula in Python.

Think step by step:
1. First, recall the SCS-CN formula: S = (25400/CN)-254, Ia = 0.2*S
2. What physical boundary conditions must be satisfied?
   - P=0 → Q=0, P≤Ia → Q=0, Q≤P always
3. Verify with known example: P=50mm, CN=80 → Q=13.8mm
4. Write the function with type hints, docstring, and all boundary conditions
```

---

## Part 2: Output Comparison

| Criterion | Naive Output | CoT Output |
|-----------|-------------|------------|
| **P ≤ Ia check** | ❌ Missing | ✅ `if P <= Ia: return 0.0` |
| **Q ≤ P enforcement** | ❌ Missing | ✅ `return min(Q, P)` |
| **Input validation** | ❌ None | ✅ CN in (0,100], P ≥ 0 |
| **Type hints** | ❌ None | ✅ `float → float` |
| **Docstring** | ❌ None | ✅ Full formula + params + returns |
| **Edge case P=0** | ❌ Division by zero risk | ✅ Returns 0.0 immediately |
| **Production-ready** | ❌ ~40% complete | ✅ 100% complete |

## Part 3: Code Comparison

### Naive (Broken)
```python
def runoff(P, CN):
    S = 25400 / CN - 254
    Ia = 0.2 * S
    Q = (P - Ia)**2 / (P - Ia + S)
    return Q  # Bug: returns negative Q when P < Ia!
```

### CoT (Correct)
```python
def calculate_runoff(P: float, CN: float) -> float:
    """Calculate runoff depth using SCS-CN method. Args: P (mm), CN (0-100). Returns: Q (mm)."""
    if CN <= 0 or CN > 100: raise ValueError(f"CN={CN} invalid")
    if P < 0: raise ValueError(f"P={P} invalid")
    if P == 0: return 0.0
    S = (25400.0 / CN) - 254.0
    Ia = 0.2 * S
    if P <= Ia: return 0.0
    Q = (P - Ia)**2 / (P - Ia + S)
    return min(Q, P)
```

---

## Part 4: Reflection

### Why CoT Works Better
1. **Role assignment** ("You are a hydrology expert") triggers domain-specific knowledge
2. **Step-by-step** forces the AI to think through boundary conditions before writing code
3. **Verification with known example** (P=50, CN=80 → Q=13.8) provides a self-check
4. **Explicit constraints** (Q≤P, P≤Ia→Q=0) prevent the AI from missing physical rules

### Lessons Learned
- Naive prompts produce **naive code** — missing 3 critical physical constraints
- CoT prompts produce **production-ready code** — all constraints satisfied
- AI self-verification works well with specific constraint checklists
- For engineering domains, **always include physical boundary conditions in the prompt**

### Score: 4.5/5