# Assignment 4: Final Capstone Project
**Weight: 40% | Domain: Reservoir Optimization**

## Objective
Build a complete, functional mini-application for reservoir dispatch optimization during drought. Integrates everything from the course: AI-assisted development, prompt engineering, testing, validation, and reflection.

## How This Differs from Assignments 1–3

| Aspect | Assignments 1–3 | Assignment 4 |
|--------|-----------------|--------------|
| Scope | Single skill | All skills integrated |
| Deliverable | Report or module | Complete runnable app |
| Reflection | Brief | Systematic Jagged Frontier analysis |

## Deliverables

| File | Description |
|------|-------------|
| `src/core/reservoir.py` | Core simulation engine |
| `src/core/optimizer.py` | Multi-objective optimizer |
| `src/core/constraints.py` | Physical constraint verification |
| `src/utils/validation.py` | Validation utility |
| `src/tests/` | Complete test suite |
| `outputs/schedule.csv` | Optimal dispatch schedule |
| `docs/AGENTS.md` | AI agent instructions |
| `docs/prompt_log.md` | Complete AI interaction log |
| `docs/jagged_frontier_report.md` | Systematic analysis |
| `README.md` | Project overview |

## Requirements

- Reservoir must balance ecological flow (10 m³/s minimum) vs. hydropower revenue during a 7-day drought
- Constraints: V_min ≤ Storage ≤ V_max, Q_release ≥ Q_ecology, mass balance
- Full project demonstrates: AI code generation, test-driven development, physical validation, prompt engineering documentation

## Grading Criteria

| Criterion | Weight |
|-----------|--------|
| Functionality | 30% |
| Code Quality | 20% |
| Test Coverage | 20% |
| Documentation | 15% |
| Jagged Frontier Analysis | 15% |