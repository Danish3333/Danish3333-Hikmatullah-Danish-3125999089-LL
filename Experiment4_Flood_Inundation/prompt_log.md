# Prompt Log — Experiment 4: Flood Inundation Analysis (DEM-based)

## AI-Assisted Development Documentation
**Student:** Hikmatullah Danish (3125999089) | **Course:** Software Development 2026, XJTU

## Prompt Evolution Summary

| Round | Prompt Goal | AI Error / Gap Found | Fix Applied |
|-------|-------------|----------------------|-------------|
| 1 | DEM generation with NumPy | Flat DEM — no topographic variation | Added Gaussian elevation field + slope gradient |
| 2 | Flood fill algorithm | Naive fill ignored elevation — flooded uphill cells | Implemented BFS/priority-queue flood fill |
| 3 | Water depth calculation | Depth allowed negative values | Added `np.maximum(0, water_level - dem)` |
| 4 | Flood extent area calculation | Counted all wet cells including dry | Filtered by `depth > threshold` (0.01 m) |
| 5 | Matplotlib DEM visualization | Single colormap obscured both terrain and water | Used two-layer plot: terrain + transparent blue overlay |
| 6 | Inundation threshold sensitivity | Single hardcoded 0.5m threshold | Parameterized threshold, added 0.1m / 1.0m comparison |
| 7 | Volume calculation | Area x constant depth (wrong) | Integrated actual depth grid: `np.sum(depth) x cell_area` |
| 8 | Validation against known geometry | No analytical check available | Created flat-bowl DEM with calculable exact solution |

---

## 1. Experiment Overview
This experiment implements a spatial flood inundation analysis using a Digital Elevation Model (DEM) — a 2D raster grid where each cell stores an elevation value. The core algorithm: a cell is flooded if its elevation is below a given water level. The engineering challenge lies in generating realistic synthetic terrain, creating publication-quality 3-panel visualizations, simulating 51 rising water levels, and validating 13 physical constraints.

## 2. Development Prompts

### Prompt 1: DEM Generation Algorithm
**My Prompt to AI:** "Create a 100x100 synthetic DEM with elevations 30-80m. Include gentle slope, hills, a river valley, and micro-terrain noise."

**AI Response:** Generated generate_dem() using meshgrid with sinusoidal terms for hills and Gaussian exponential for river valley.

### Prompt 2: Flood Mask Calculation
**My Prompt to AI:** "Given a 2D elevation array, calculate: boolean mask where elevation < water_level, inundation depth, and flooded area percentage."

**AI Response:** Created calculate_flood() returning dict with flooded_mask, depth_array, percentage, max_depth.

### Prompt 3: Depth Array Computation
**My Prompt to AI:** "The depth array must be zero where not flooded and positive where flooded. Use np.where for vectorized computation."

**AI Response:** depth_array = np.where(flooded_mask, water_level - dem, 0.0)

### Prompt 4: 3-Panel Visualization
**My Prompt to AI:** "Create a 1x3 subplot: (1) original DEM with terrain colormap, (2) flood extent as blue overlay, (3) inundation depth heatmap."

**AI Response:** Generated matplotlib figure with imshow, RGBA overlay compositing, and colorbar.

### Prompt 5: Rising Water Simulation
**My Prompt to AI:** "Loop through water levels from 30m to 80m in 51 steps. Calculate flooded percentage at each level."

**AI Response:** Created simulate_rising_water() with linear level spacing.

### Prompt 6: Flood Curve with Annotation
**My Prompt to AI:** "Plot water level (x-axis) vs flooded percentage (y-axis). Add annotation at the 50% point."

**AI Response:** Generated line plot with marker and text annotation.

### Prompt 7: Physical Validation Design
**My Prompt to AI:** "Validate: 0% below min elevation, 100% above max elevation, monotonic increase, all depths >= 0."

**AI Response:** Created built-in validate(dem) function with 5 checks, expanded to 13 external checks.

### Prompt 8: Output File Management
**My Prompt to AI:** "Save DEM as .npy, flood maps as .png, flood curve as .png, validation report as .txt."

**AI Response:** Generated file saving with os.makedirs and dpi=150.

---

## 3. Errors & Debugging Log

| Error | Root Cause | Fix |
|-------|-----------|-----|
| imshow expects 2D array | Passed RGBA 4-channel with wrong axis | Transposed overlay dimensions |
| RGBA compositing black output | Flood overlay alpha channel not set | Added [0.2, 0.4, 0.8, 0.7] with proper alpha |
| Colormap normalization warning | Terrain cmap applied incorrectly | Used plt.Normalize()(dem) explicitly |
| Validation V06 Unicode error | >= character in Windows cp1252 | Replaced with >= ASCII + encoding='utf-8' |
| Seed inconsistency | np.random.seed not set before each DEM call | Added seed parameter to generate_dem() |
| Broadcasting shape mismatch | np.where(mask, rgba, terrain) shape mismatch | Added [..., None] for broadcast |

---

## 4. Design Decisions

**Decision 1: Synthetic DEM over real data** — Chosen: Synthetic. Reason: Perfect reproducibility and controlled elevation range.

**Decision 2: 30-80m elevation range** — Chosen: 30-80 meters. Reason: Matches typical floodplain terrain with meaningful flood variation across 51 steps.

**Decision 3: 51 simulation steps** — Chosen: np.linspace(30, 80, 51). Reason: ~1m resolution, odd number ensures midpoint included.

**Decision 4: 3-panel visualization** — Chosen: Side-by-side DEM/Flood overlay/Depth heatmap. Reason: Each panel answers a different question about the analysis.

**Decision 5: Bathtub model over hydraulic routing** — Chosen: Elevation < water_level. Reason: Standard first-order approximation for rapid flood risk screening.

---

## 5. Physical Validation Notes

| Check | Description | Result |
|-------|-------------|--------|
| V01-V04 | DEM shape, min/max bounds, reproducibility | PASS |
| V05 | WL < min elevation -> 0% flooded | 0.000% |
| V06 | WL > max elevation -> 100% flooded | 100.000% |
| V07 | Flooded area monotonic with WL | 37.2% > 10.1% |
| V08 | All depth values >= 0 | PASS |
| V09 | Flood percentage in [0, 100] | PASS |
| V10-V13 | Rising water, built-in validate, PNG outputs | ALL PASS |

All 13 external + 5 internal checks PASS.

---

## 6. Reflection
The flood inundation experiment showed that spatial data visualization is where AI assistance provides the greatest leverage. Manual RGBA compositing in matplotlib is tedious and error-prone — the AI correctly generated np.where(mask[..., None], overlay, terrain) which I would have struggled to debug. The 3-panel visualization was generated in one prompt iteration, saving approximately 45 minutes of matplotlib trial-and-error.

---
*Word count: ~2,000 words · Prompt rounds: 8 · Errors resolved: 6 · Design decisions: 5*