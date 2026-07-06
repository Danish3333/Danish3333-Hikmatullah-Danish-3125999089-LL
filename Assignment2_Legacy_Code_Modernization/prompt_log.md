# Prompt Log - Assignment 2: Legacy Code Modernization

## Session Date: 2026-06-26

---

## Prompt 1: Legacy Code Analysis

**Prompt:**
```
Here is a legacy rainfall monitoring script written in Python 2 (circa 2018).
Analyze it and identify all issues:
[Pasted legacy code with urllib2, no types, no error handling, buggy alert logic]
```

**AI Response:** Identified 14 issues:
1. urllib2 removed in Python 3 → must replace with requests
2. No error handling → crashes on API failure
3. Magic numbers 10, 20 in alert logic → should be named constants
4. Alert threshold logic reversed (rain > 10 → yellow, > 20 → red should be < 10 green, 10-20 yellow, >= 20 red)
5. Hardcoded 3-city list → should be configurable
6. File open without context manager → leak risk
7. No type hints
8. No docstrings
9. Uses undefined variable `city` in `process()`
10. String concatenation for URL → no encoding
11. No timeout on HTTP request
12. No unit tests
13. Returns ambiguous tuple
14. No input validation

---

## Prompt 2: Modernization Strategy

**Prompt:**
```
Now modernize this legacy code for Python 3.12. Requirements:
- Replace urllib2 with requests (add timeout)
- Use dataclass instead of raw tuple returns
- Add type hints throughout
- Fix the alert logic bug
- Use context manager for file I/O
- Add proper error handling
- Add docstrings
- Make city list configurable
```

**AI Response:** Designed modernization with:
- `requests.get()` with timeout and error handling
- `@dataclass WeatherData` for structured returns
- Full type annotations (float, str, Tuple, Optional)
- Corrected alert thresholds with `check_alert()` function
- `with open() as f` context manager for logging
- All functions documented
- 5-city default with CITIES constant

---

## Prompt 3: Code Map Generation

**Prompt:**
```
Generate an AI-created code map explaining the modernized architecture. Show layers, data flow, and migration changes.
```

**AI Response:** Created layered architecture map with 5 layers (Data/API/Business/Domain/Persistence/Orchestration), data flow diagram, and migration comparison table.

---

## Errors Encountered and Corrections

| Error | Correction |
|-------|------------|
| Legacy uses Python 2 `urllib2` | Replaced with `requests` library |
| Alert bug: thresholds reversed | Corrected to CMA standard (<10 Green, 10-20 Yellow, >=20 Red) |
| Legacy uses `city` variable out of scope | Passed as explicit function parameter |