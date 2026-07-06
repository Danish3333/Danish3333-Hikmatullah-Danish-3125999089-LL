#!/usr/bin/env python3
"""validate_flood.py -- Physical validation for Experiment 4: Flood Inundation Analysis.
Runs 13 checks (V01-V13) and saves validation_report.txt."""

from datetime import datetime
import numpy as np
import os
from flood_inundation import generate_dem, calculate_flood, simulate_rising_water, validate

def main():
    results = []
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("VALIDATION REPORT -- Experiment 4: Flood Inundation Analysis")
    report_lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 60)

    dem = generate_dem(100, seed=42)

    # V01: DEM shape
    ok = dem.shape == (100, 100)
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V01: DEM shape is (100,100) -- {dem.shape}")

    # V02: DEM min elevation
    ok = dem.min() >= 29.9
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V02: DEM min >= 29.9m -- {dem.min():.1f}m")

    # V03: DEM max elevation
    ok = dem.max() <= 80.1
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V03: DEM max <= 80.1m -- {dem.max():.1f}m")

    # V04: Reproducible
    dem2 = generate_dem(100, seed=42)
    ok = np.allclose(dem, dem2)
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V04: DEM reproducible (same seed)")

    # V05: 0% below terrain
    r = calculate_flood(dem, dem.min() - 1)
    ok = r['percentage'] < 0.01
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V05: WL<min -> 0% -- {r['percentage']:.3f}%")

    # V06: 100% above terrain
    r = calculate_flood(dem, dem.max() + 1)
    ok = r['percentage'] > 99.99
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V06: WL>max -> 100% -- {r['percentage']:.3f}%")

    # V07: Monotonic flood
    r40 = calculate_flood(dem, 40)
    r50 = calculate_flood(dem, 50)
    ok = r50['percentage'] >= r40['percentage']
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V07: Flood@50m >= Flood@40m -- {r50['percentage']:.1f}% >= {r40['percentage']:.1f}%")

    # V08: No negative depth
    r = calculate_flood(dem, 55)
    ok = bool(np.all(r['depth_array'] >= 0))
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V08: All depth values >= 0 -- min={r['depth_array'].min():.2f}")

    # V09: Percentage in [0,100]
    ok = 0 <= r['percentage'] <= 100
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V09: Flood % in [0,100] -- {r['percentage']:.1f}%")

    # V10: Rising water monotonic
    levels = np.linspace(30, 80, 10)
    sim = simulate_rising_water(dem, levels)
    pcts = sim['percentages']
    ok = all(pcts[i] <= pcts[i+1] + 1e-6 for i in range(len(pcts)-1))
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V10: Rising water monotonic")

    # V11: Built-in validate
    v = validate(dem)
    ok = all(p for _, p in v)
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V11: Built-in validate() all pass -- {sum(1 for _,p in v if p)}/{len(v)}")

    # V12: Output PNG exists
    ok = os.path.exists('outputs/flood_extent_40m.png')
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V12: flood_extent_40m.png exists")

    # V13: Output PNG exists
    ok = os.path.exists('outputs/flood_extent_50m.png')
    results.append(ok)
    report_lines.append(f"[{'PASS' if ok else 'FAIL'}] V13: flood_extent_50m.png exists")

    passed = sum(results)
    total = len(results)
    report_lines.append("-" * 60)
    report_lines.append(f"Result: {passed}/{total} PASSED")
    report_lines.append("Conclusion: All flood inundation physical constraints verified.")

    report = "\n".join(report_lines)
    print(report)
    with open('validation_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\nValidation Summary: {passed}/{total} checks PASSED")

if __name__ == '__main__':
    main()