"""Test suite for SCS-CN Runoff Calculation."""
import sys
sys.path.insert(0, '.')
from scscn_runoff import calculate_runoff, calculate_S, calculate_Ia


def test_boundary_conditions():
    """Test all boundary conditions."""
    results = []

    # Test P=0 -> Q=0
    q = calculate_runoff(0, 80)
    assert q == 0.0, f"P=0 should give Q=0, got {q}"
    results.append(("P=0, Q=0", "PASS"))

    # Test P < Ia -> Q=0
    q = calculate_runoff(5, 80)  # Ia=12.7 for CN=80
    assert q == 0.0, f"P < Ia should give Q=0, got {q}"
    results.append(("P < Ia, Q=0", "PASS"))

    # Test P = Ia -> Q=0
    ia = calculate_Ia(80)
    q = calculate_runoff(ia, 80)
    assert q == 0.0, f"P=Ia should give Q=0, got {q}"
    results.append(("P=Ia, Q=0", "PASS"))

    # Test known case: P=50, CN=80 -> Q=13.8
    q = calculate_runoff(50, 80)
    assert abs(q - 13.8) < 0.1, f"Expected Q=13.8, got {q}"
    results.append(("P=50, CN=80 -> Q=13.8", "PASS"))

    # Test CN=100 -> max runoff
    q = calculate_runoff(50, 100)
    assert q >= 0, f"CN=100 should give positive runoff"
    results.append(("CN=100 max runoff", "PASS"))

    # Test Q <= P always
    for p in [10, 25, 50, 100, 200]:
        for cn in [60, 70, 80, 90, 95]:
            q = calculate_runoff(p, cn)
            assert q <= p, f"Q({q}) > P({p}) for P={p}, CN={cn}"
    results.append(("Q <= P for all cases", "PASS"))

    # Test invalid inputs
    try:
        calculate_runoff(50, 0)
        assert False, "Should have raised ValueError"
    except ValueError:
        results.append(("CN=0 raises error", "PASS"))

    try:
        calculate_runoff(-5, 80)
        assert False, "Should have raised ValueError"
    except ValueError:
        results.append(("P<0 raises error", "PASS"))

    return results


if __name__ == '__main__':
    print("Running SCS-CN Test Suite...")
    print("-" * 50)
    results = test_boundary_conditions()
    passed = 0
    for name, status in results:
        print(f"  [{status}] {name}")
        if status == "PASS":
            passed += 1
    print("-" * 50)
    print(f"Results: {passed}/{len(results)} tests passed")