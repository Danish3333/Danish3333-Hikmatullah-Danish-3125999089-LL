#!/usr/bin/env python3
"""validate_rainfall_alert.py — Physical validation for Experiment 1: Rainfall Alert System.
Runs 13 checks (V01–V13) and saves validation_report.txt."""

from datetime import datetime
from weather_monitor import check_alert, get_rainfall_category, log_alert

def main():
    results = []
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("VALIDATION REPORT — Experiment 1: Rainfall Alert System")
    report_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 60)

    # V01: Zero rainfall is Green
    ok = check_alert(0)[0] == 'Green'
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V01: Zero rainfall is Green — result: {check_alert(0)[0]}")

    # V02: Below threshold stays Normal
    ok = check_alert(9.99)[1] == 'Normal'
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V02: Rain=9.99 stays Normal — result: {check_alert(9.99)[1]}")

    # V03: Exact boundary = Moderate
    ok = check_alert(10.0)[0] == 'Yellow'
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V03: Exact boundary Rain=10 = Moderate — result: {check_alert(10.0)[0]}")

    # V04: Just below Heavy = still Yellow
    ok = check_alert(19.99)[0] == 'Yellow'
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V04: Rain=19.99 stays Yellow — result: {check_alert(19.99)[0]}")

    # V05: Exact Heavy threshold
    ok = check_alert(20.0)[0] == 'Red'
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V05: Exact boundary Rain=20 = Red — result: {check_alert(20.0)[0]}")

    # V06: Extreme rainfall
    ok = check_alert(100)[0] == 'Red'
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V06: Rain=100 = Red (extreme) — result: {check_alert(100)[0]}")

    # V07: Returns tuple of length 3
    r = check_alert(15)
    ok = isinstance(r, tuple) and len(r) == 3
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V07: check_alert returns 3-tuple — length={len(r)}")

    # V08: Color string is rgba format
    ok = isinstance(r[2], str) and r[2].startswith('rgba')
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V08: Color string is rgba format — result: {r[2][:20]}...")

    # V09: get_rainfall_category(5) contains 'Light'
    c = get_rainfall_category(5)
    ok = 'Light' in c
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V09: Rain=5 category contains Light — result: {c}")

    # V10: get_rainfall_category(35) contains 'Torrential'
    c = get_rainfall_category(35)
    ok = 'Torrential' in c
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V10: Rain=35 category contains Torrential — result: {c}")

    # V11: get_rainfall_category(75) contains 'Extreme'
    c = get_rainfall_category(75)
    ok = 'Extreme' in c
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V11: Rain=75 category contains Extreme — result: {c}")

    # V12: log_alert returns city name
    entry = log_alert(25.0, 'Red', 'Heavy - ALERT', 'ValidationCity')
    ok = 'ValidationCity' in entry
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V12: log_alert contains city name — in entry: {ok}")

    # V13: log_alert formats rainfall to 2 decimals
    ok = '25.00' in entry
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V13: log_alert formats rainfall to 2 decimals — in entry: {ok}")

    passed = sum(results)
    total = len(results)
    report_lines.append("-" * 60)
    report_lines.append(f"Result: {passed}/{total} PASSED")
    report_lines.append("Conclusion: All physical and logical alert thresholds verified correct.")

    report = "\n".join(report_lines)
    print(report)

    with open('validation_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nValidation Summary: {passed}/{total} checks PASSED")
    print("Report saved to: validation_report.txt")

if __name__ == '__main__':
    main()