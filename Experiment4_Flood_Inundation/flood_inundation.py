"""
Experiment 4: Flood Inundation Analysis (DEM-based)
====================================================
Spatial flood inundation analysis using Digital Elevation Model data.
- DEM generation (synthetic terrain)
- Flood calculation (elevation < water_level)
- Flood extent visualization
- Dynamic water level simulation
- Flooded area percentage vs water level curve
"""

import numpy as np
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def generate_dem(size: int = 100, seed: int = 42) -> np.ndarray:
    """Generate synthetic DEM with realistic terrain features.

    Creates a 100x100 grid with elevations between 30-80m.
    Terrain includes: river valley, hills, and flat plains.
    """
    np.random.seed(seed)
    x = np.linspace(-3, 3, size)
    y = np.linspace(-3, 3, size)
    X, Y = np.meshgrid(x, y)

    # Base terrain: gentle slope + hills
    dem = 50 + 5 * X + 3 * Y  # gentle slope
    dem += 8 * np.sin(X * 2) * np.cos(Y * 1.5)  # hills
    dem += 6 * np.sin(X * 3 + Y * 2)  # terrain variation
    dem += np.random.randn(size, size) * 1.5  # micro-terrain

    # River valley (dip in the middle)
    river_valley = -12 * np.exp(-((Y - 0.3 * X) ** 2) / 0.8)
    dem += river_valley

    # Normalize to 30-80m range
    dem = 30 + (dem - dem.min()) / (dem.max() - dem.min()) * 50
    return dem.astype(np.float32)


def calculate_flood(dem: np.ndarray, water_level: float) -> dict:
    """Calculate flood inundation for a given water level.

    Args:
        dem: 2D elevation array in meters.
        water_level: Flood water level in meters.

    Returns:
        Dictionary with:
        - flooded_mask: Boolean array (True where flooded)
        - depth_array: Inundation depth (0 where not flooded)
        - percentage: Percentage of area flooded
        - max_depth: Maximum inundation depth
    """
    flooded_mask = dem < water_level
    depth_array = np.where(flooded_mask, water_level - dem, 0.0)
    percentage = flooded_mask.mean() * 100
    max_depth = depth_array.max()

    return {
        'flooded_mask': flooded_mask,
        'depth_array': depth_array,
        'percentage': float(percentage),
        'max_depth': float(max_depth)
    }


def visualize_flood(dem: np.ndarray, result: dict, water_level: float, filename: str):
    """Create flood extent visualization with terrain and water overlay."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: Original DEM
    im1 = axes[0].imshow(dem, cmap='terrain', origin='lower')
    axes[0].set_title(f'Original DEM\n({dem.shape[0]}x{dem.shape[1]})', fontsize=12, fontweight='bold')
    axes[0].set_xlabel('X (pixels)')
    axes[0].set_ylabel('Y (pixels)')
    plt.colorbar(im1, ax=axes[0], label='Elevation (m)')

    # Panel 2: Flooded mask overlay
    terrain_rgba = plt.cm.terrain(plt.Normalize()(dem))
    flood_overlay = np.zeros_like(terrain_rgba)
    flood_overlay[result['flooded_mask']] = [0.2, 0.4, 0.8, 0.7]  # Blue with transparency
    combined = np.where(result['flooded_mask'][:, :, None], flood_overlay, terrain_rgba)
    axes[1].imshow(combined, origin='lower')
    axes[1].set_title(f'Flood Extent at {water_level}m\nFlooded: {result["percentage"]:.1f}%', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('X (pixels)')
    axes[1].set_ylabel('Y (pixels)')

    # Panel 3: Inundation depth
    im3 = axes[2].imshow(result['depth_array'], cmap='Blues', origin='lower')
    axes[2].set_title(f'Inundation Depth\nMax Depth: {result["max_depth"]:.2f}m', fontsize=12, fontweight='bold')
    axes[2].set_xlabel('X (pixels)')
    axes[2].set_ylabel('Y (pixels)')
    plt.colorbar(im3, ax=axes[2], label='Depth (m)')

    fig.suptitle(f'Flood Inundation Analysis - Water Level: {water_level}m', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {filename}")


def simulate_rising_water(dem: np.ndarray, levels: np.ndarray) -> dict:
    """Simulate rising water levels and compute flooded percentage.

    Args:
        dem: 2D elevation array.
        levels: Array of water levels to simulate.

    Returns:
        Dictionary with levels and percentages arrays.
    """
    percentages = []
    max_depths = []
    for wl in levels:
        result = calculate_flood(dem, wl)
        percentages.append(result['percentage'])
        max_depths.append(result['max_depth'])

    return {
        'levels': levels,
        'percentages': np.array(percentages),
        'max_depths': np.array(max_depths)
    }


def plot_flood_curve(sim_results: dict, filename: str = 'flood_curve.png'):
    """Plot water level vs flooded percentage curve."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color1 = '#2563eb'
    ax1.plot(sim_results['levels'], sim_results['percentages'], 'o-', color=color1, linewidth=2, markersize=5)
    ax1.set_xlabel('Water Level (m)', fontsize=12)
    ax1.set_ylabel('Flooded Area (%)', color=color1, fontsize=12)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)
    ax1.set_title('Flood Inundation Curve\nWater Level vs. Flooded Percentage', fontsize=14, fontweight='bold')

    # Add annotations
    mid_idx = len(sim_results['levels']) // 2
    ax1.annotate(f'{sim_results["percentages"][mid_idx]:.1f}% at {sim_results["levels"][mid_idx]}m',
                xy=(sim_results['levels'][mid_idx], sim_results['percentages'][mid_idx]),
                xytext=(sim_results['levels'][mid_idx] + 2, sim_results['percentages'][mid_idx] - 5),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=10)

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {filename}")


def validate(dem: np.ndarray) -> list:
    """Validate physical correctness of flood calculations."""
    results = []
    min_elev = dem.min()
    max_elev = dem.max()

    # Test 1: Water below min elevation -> 0% flooded
    r = calculate_flood(dem, min_elev - 1)
    results.append(("WL < min elevation -> 0%", abs(r['percentage']) < 0.01))

    # Test 2: Water above max elevation -> 100% flooded
    r = calculate_flood(dem, max_elev + 1)
    results.append(("WL > max elevation -> 100%", abs(r['percentage'] - 100) < 0.01))

    # Test 3: Flooded area monotonic (increases with WL)
    wls = np.linspace(min_elev, max_elev, 10)
    pcts = [calculate_flood(dem, wl)['percentage'] for wl in wls]
    monotonic = all(pcts[i] <= pcts[i + 1] + 1e-9 for i in range(len(pcts) - 1))
    results.append(("Flooded area increases monotonically", monotonic))

    # Test 4: Max depth equals WL - min_elev
    r = calculate_flood(dem, max_elev)
    results.append(("Max depth = WL - min_elev", abs(r['max_depth'] - (max_elev - min_elev)) < 0.5))

    # Test 5: Percentage between 0-100
    r = calculate_flood(dem, (min_elev + max_elev) / 2)
    results.append(("Percentage between 0-100", 0 <= r['percentage'] <= 100))

    return results


# =============================================================================
# Main Execution
# =============================================================================
if __name__ == '__main__':
    print("=" * 60)
    print("FLOOD INUNDATION ANALYSIS (DEM-based)")
    print("=" * 60)

    # Generate DEM
    dem = generate_dem(100, seed=42)
    os.makedirs('outputs', exist_ok=True)
    np.save('outputs/dem_data.npy', dem)
    print(f"\n[1] DEM generated: {dem.shape}, range=[{dem.min():.1f}, {dem.max():.1f}]m")

    # Flood at specific levels
    for wl in [40, 50]:
        result = calculate_flood(dem, wl)
        visualize_flood(dem, result, wl, f'outputs/flood_extent_{wl}m.png')
        print(f"\n[2] WL={wl}m: Flooded={result['percentage']:.2f}%, Max Depth={result['max_depth']:.2f}m")

    # Dynamic simulation
    levels = np.linspace(30, 80, 51)
    sim = simulate_rising_water(dem, levels)
    plot_flood_curve(sim, 'outputs/flood_curve.png')
    print(f"\n[3] Dynamic simulation: {len(levels)} levels from {levels[0]}m to {levels[-1]}m")

    # Validation
    print("\n[4] Validation Results:")
    print("-" * 40)
    all_pass = True
    for name, passed in validate(dem):
        status = "PASS" if passed else "FAIL"
        if not passed: all_pass = False
        print(f"  [{status}] {name}")
    print("-" * 40)
    print(f"  Overall: {'ALL PASS' if all_pass else 'SOME FAILED'}")
    print("\n" + "=" * 60)
    print("Analysis complete. All outputs saved.")