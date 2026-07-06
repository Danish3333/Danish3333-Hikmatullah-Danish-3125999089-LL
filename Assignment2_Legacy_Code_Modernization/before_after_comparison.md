# Assignment 2: Legacy vs Modernized — Side-by-Side Comparison

## Code Quality Improvements

| Issue | Legacy v1 (Python 2) | Modernized v2 (Python 3.12) |
|-------|---------------------|---------------------------|
| **HTTP library** | `urllib2` (removed in Python 3) | `requests` with timeout |
| **Error handling** | None — crashes on API failure | `try/except` with `raise_for_status()` |
| **Type system** | No annotations | Full type hints (`float`, `str`, `Tuple`) |
| **Data structure** | Raw tuple return | `@dataclass WeatherData` |
| **File I/O** | `open()` without cleanup | Context manager (`with open()`) |
| **Alert logic** | Reversed thresholds (bug) | Correct: <10 Green, 10-20 Yellow, >=20 Red |
| **URL construction** | String concatenation | Parameter dict (auto-encoded) |
| **Scoping** | Uses undefined `city` in `process()` | City passed explicitly |
| **Logging** | Appends without timestamp format | Structured format with timestamp |
| **Documentation** | No docstrings | Full docstrings on all functions |
| **Testability** | Monolithic — untestable | Modular — each function independently testable |
| **Python version** | Python 2 only | Python 3.10+ |

## Architecture Comparison

### Legacy Architecture (v1)
```
main() → getweather(city) → urllib2 → raw dict
       → process(dict) → tuple with bugs
       → print
```

### Modernized Architecture (v2)
```
main() → for city in CITIES:
       → fetch_weather(city) → requests → WeatherData dataclass
       → check_alert(rainfall) → (level, status) tuple
       → get_rainfall_category(rainfall) → CMA string
       → log_alert() if Red → context-managed file write
       → print formatted output
```

## Key Modernization Wins

1. **Bug fix:** Alert thresholds corrected (was reversed in legacy)
2. **Safety:** HTTP timeouts prevent hanging
3. **Maintainability:** Type hints enable IDE autocompletion
4. **Reliability:** Proper exception handling
5. **Readability:** Dataclass replaces ambiguous tuple returns
6. **Portability:** Works on Python 3.10+ (legacy was Python 2 only)

## AI Collaboration Summary

- **AI analyzed** legacy code and identified 14 distinct issues
- **AI proposed** modernization strategy with dataclasses + requests
- **AI generated** modernized code with all improvements
- **Human verified** alert thresholds, API endpoint, and physical consistency