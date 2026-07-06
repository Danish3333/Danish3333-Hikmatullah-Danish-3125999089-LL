# Prompt Log — Assignment 3: The Swiss Cheese Test Suite

## AI-Assisted Development Documentation
**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026, XJTU

---

## 1. Assignment Overview

This assignment required designing a multi-layer "Swiss Cheese" test suite for a flood inundation model. Each layer catches what the previous layer missed: unit tests verify basic execution, boundary tests check extreme values, physical tests validate scientific constraints, and regression tests ensure reproducibility. The goal was to identify AI "hallucinations" — places where AI-generated code violates physical reality.

---

## 2. Development Prompts

### Prompt 1: Test Strategy Design
**My Prompt to AI:** "Design a 4-layer test suite for a flood inundation function: Layer 1 Unit Tests, Layer 2 Boundary Tests, Layer 3 Physical Tests, Layer 4 Regression Tests. What should each layer test?"

**AI Response:** Proposed 4-layer model with specific test categories. Unit: return types, shapes. Boundary: min/max elevations. Physical: monotonicity, non-negative depth. Regression: seed reproducibility.

### Prompt 2: Unit Test Implementation
**My Prompt to AI:** "Write Layer 1 unit tests: Does the function return a dict? Are required keys present? Is the mask boolean? Are shapes correct?"

**AI Response:** Generated 6 unit tests checking dict structure, key presence, dtypes, and shape consistency.

### Prompt 3: Boundary Test Implementation
**My Prompt to AI:** "Write Layer 2 boundary tests: What happens at water level below minimum elevation? Above maximum? At exact min/max? With small increments?"

**AI Response:** Generated 5 boundary tests including edge cases at exact elevation boundaries.

### Prompt 4: Physical Test Implementation
**My Prompt to AI:** "Write Layer 3 physical tests: Is flooded area monotonically increasing? Are depths non-negative? Is max depth correct? Are mask and depth arrays consistent?"

**AI Response:** Generated 10 physical validation tests.

### Prompt 5: Regression Tests
**My Prompt to AI:** "Write Layer 4 regression tests: Same seed → same DEM? Different seed → different DEM? Deterministic flood calculation?"

**AI Response:** Generated 3 regression tests.

### Prompt 6: Hallucination Detection
**My Prompt to AI:** "What AI hallucinations could occur in flood inundation code? What specific tests would catch each one?"

**AI Response:** Identified 4 potential hallucinations: negative depths for non-flooded cells, integer division, <= vs < boundary, off-by-one indexing.

### Prompt 7: Standalone Execution
**My Prompt to AI:** "Make the test suite self-contained without importing from Experiment4. Embed the functions directly."

**AI Response:** Created standalone version with embedded generate_dem() and calculate_flood().

### Prompt 8: Unicode Fix
**My Prompt to AI:** "Replace all Unicode characters with ASCII to avoid Windows encoding errors in batch runs."

**AI Response:** Replaced ≥, →, ≈ with ASCII equivalents.

---

## 3. Errors & Debugging Log

| Error | Root Cause | Fix |
|-------|-----------|-----|
| ModuleNotFoundError for flood_inundation | Test tried to import from Experiment4 | Embedded functions directly in test file |
| UnicodeEncodeError on ≥ character | Windows CP1252 encoding limitation | Replaced with ASCII >= |
| Test failure: WL = max_elev expected 100% | <= vs < boundary — only strict inequality flags cells | Updated test expectation to acknowledge this is correct behavior |
| Subprocess capture issue in batch runner | UTF-8 box-drawing characters failed on Windows | Used ASCII '=' characters |

---

## 4. Design Decisions

**Decision 1: 4-layer model over flat test list**
Chosen: Structured 4-layer approach (Unit/Boundary/Physical/Regression)
Reason: Each layer catches a different class of error. Flat test lists don't reveal coverage gaps.

**Decision 2: Standalone over import-based**
Chosen: Self-contained test file with embedded functions
Reason: Avoids import path issues and makes the assignment independently runnable.

**Decision 3: 24 total test cases**
Chosen: Layer 1 (6) + Layer 2 (5) + Layer 3 (10) + Layer 4 (3) = 24 tests
Reason: Sufficient coverage for a 2-hour assignment without excessive redundancy.

---

## 5. Key Results

All 24/24 tests pass. No hallucinations detected in the current flood_inundation implementation — the code correctly uses np.where() for depth calculation, strict inequality for flood condition, and float64 for percentage calculation.

## 6. Reflection

The Swiss Cheese model proved effective at systematically covering blind spots that a flat test list would miss. Layer 3 physical tests caught the most interesting edge case: the difference between strict `<` and `<=` at exact boundary conditions. This isn't a bug but a design choice that needed documentation. The exercise confirmed that AI-generated scientific code needs multi-layer testing because each layer catches qualitatively different classes of errors.