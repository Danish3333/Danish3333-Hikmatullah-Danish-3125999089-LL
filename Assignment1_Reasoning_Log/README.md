# Assignment 1: The Reasoning Log
**Weight: 20% | Domain: SCS-CN Hydrological Modeling**

## Objective
Use Chain-of-Thought (CoT) prompting to solve the SCS-CN rainfall-runoff problem, then document the full reasoning trace and human verification steps.

## Deliverables

| File | Description |
|------|-------------|
| `prompt_01_naive.md` | Initial naive prompt + AI response |
| `prompt_02_cot.md` | Structured CoT prompt + AI response |
| `prompt_03_verification.md` | Verification prompt + AI self-review |
| `comparison_report.md` | Naive vs CoT comparison + reflection |
| `prompt_log.md` | Complete AI interaction documentation |

## Task Steps

1. **Initial Prompt (Naive):** Ask an AI to write the SCS-CN function without structure. Identify errors.
2. **CoT Prompt (Structured):** Chain-of-Thought prompt with role assignment, formula, edge cases, step-by-step reasoning.
3. **Verification Prompt:** Ask AI to review its own output for physical correctness.
4. **Final Report:** Reflection comparing naive vs. CoT output quality, AI self-verification vs. human verification.

## The SCS-CN Problem
```
Q = (P - Ia)^2 / (P - Ia + S)
S = (25400 / CN) - 254
Ia = 0.2 * S
```

## Grading Criteria

| Criterion | Weight |
|-----------|--------|
| CoT Prompt Quality | 30% |
| Error Identification | 30% |
| Verification Depth | 25% |
| Reflection Quality | 15% |