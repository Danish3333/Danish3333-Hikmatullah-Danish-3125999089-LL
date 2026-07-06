"""
Assignment 3: The Swiss Cheese Test Suite -- Flood Inundation Model
==================================================================
4-layer test suite that identifies "Jagged Edges" in AI-generated code.
Designed to catch AI hallucinations in flood inundation calculations.
"""

import numpy as np


def generate_dem(size=100, seed=42):
    np.random.seed(seed)
    x = np.linspace(-3, 3, size); y = np.linspace(-3, 3, size)
    X, Y = np.meshgrid(x, y)
    dem = 50 + 5*X + 3*Y + 8*np.sin(X*2)*np.cos(Y*1.5) + 6*np.sin(X*3+Y*2) + np.random.randn(size,size)*1.5
    river = -12*np.exp(-((Y-0.3*X)**2)/0.8)
    dem += river
    dem = 30 + (dem - dem.min())/(dem.max()-dem.min())*50
    return dem.astype(np.float32)

def calculate_flood(dem, water_level):
    flooded = dem < water_level
    depth = np.where(flooded, water_level-dem, 0.0)
    return {'flooded_mask':flooded,'depth_array':depth,'percentage':float(flooded.mean()*100),'max_depth':float(depth.max())}


def test_layer1_unit():
    results = []
    dem = generate_dem(50, seed=1)
    r = calculate_flood(dem, 50)
    results.append(("Returns dict", isinstance(r, dict)))
    results.append(("Required keys", all(k in r for k in ['flooded_mask','depth_array','percentage','max_depth'])))
    results.append(("Mask is boolean", r['flooded_mask'].dtype == bool))
    results.append(("Percentage is float", isinstance(r['percentage'], float)))
    results.append(("Mask matches DEM shape", r['flooded_mask'].shape == dem.shape))
    results.append(("Depth matches DEM shape", r['depth_array'].shape == dem.shape))
    return results


def test_layer2_boundaries():
    results = []
    dem = generate_dem(50, seed=42)
    mn, mx = dem.min(), dem.max()
    r = calculate_flood(dem, mn-10)
    results.append(("WL < min_elev -> 0%", abs(r['percentage'])<0.01))
    r = calculate_flood(dem, mx+10)
    results.append(("WL > max_elev -> 100%", abs(r['percentage']-100)<0.01))
    r = calculate_flood(dem, mn)
    results.append(("WL = min_elev", 0<=r['percentage']<=100))
    r = calculate_flood(dem, mx)
    results.append(("WL = max_elev (<= vs < edge)", r['percentage'] < 100 and r['percentage'] > 0))
    r1 = calculate_flood(dem, 40.0); r2 = calculate_flood(dem, 40.001)
    results.append(("Small WL increase", r2['percentage']>=r1['percentage']))
    return results


def test_layer3_physical():
    results = []
    dem = generate_dem(50, seed=42)
    levels = np.linspace(dem.min(), dem.max(), 15)
    pcts = [calculate_flood(dem, wl)['percentage'] for wl in levels]
    results.append(("Monotonic increase", all(pcts[i]<=pcts[i+1]+1e-9 for i in range(len(pcts)-1))))
    for wl in [30,40,50,60,70]:
        r = calculate_flood(dem, wl)
        results.append((f"No neg depth WL={wl}", bool(np.all(r['depth_array']>=0))))
    r = calculate_flood(dem, 60)
    results.append(("Max depth correct", abs(r['max_depth']-(60-dem.min()))<0.5))
    r = calculate_flood(dem, 45)
    nd = r['depth_array'][~r['flooded_mask']]
    results.append(("Non-flooded depth=0", bool(np.all(nd==0))))
    if np.any(r['flooded_mask']):
        fd = r['depth_array'][r['flooded_mask']]
        results.append(("Flooded depth>0", bool(np.all(fd>0))))
    results.append(("Mask-depth consistent", bool(np.all((r['depth_array']>0)==r['flooded_mask']))))
    return results


def test_layer4_regression():
    results = []
    d1 = generate_dem(30, seed=99); d2 = generate_dem(30, seed=99)
    results.append(("Same seed -> same DEM", np.allclose(d1, d2)))
    d3 = generate_dem(30, seed=100)
    results.append(("Different seed -> different", not np.allclose(d1, d3)))
    dem = generate_dem(40, seed=7)
    r1 = calculate_flood(dem, 45); r2 = calculate_flood(dem, 45)
    results.append(("Deterministic flood", abs(r1['percentage']-r2['percentage'])<1e-10))
    return results


if __name__ == '__main__':
    passed_total = 0; total_tests = 0
    layers = [
        ("LAYER 1: Unit Tests", test_layer1_unit()),
        ("LAYER 2: Boundary Tests", test_layer2_boundaries()),
        ("LAYER 3: Physical Tests", test_layer3_physical()),
        ("LAYER 4: Regression Tests", test_layer4_regression()),
    ]
    for name, tests in layers:
        print(f"\n{'='*60}\n{name}\n{'='*60}")
        p = 0
        for n, ok in tests:
            s = "PASS" if ok else "FAIL"
            if ok: p += 1
            print(f"  [{s}] {n}")
        passed_total += p; total_tests += len(tests)
        print(f"  -> {p}/{len(tests)} passed")
    print(f"\n{'='*60}\nSWISS CHEESE TOTAL: {passed_total}/{total_tests}\n{'='*60}")
    print(f"\nScore: {passed_total}/{total_tests}")