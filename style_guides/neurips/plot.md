# NeurIPS Plot Style Guide

## 1. The "NeurIPS Look"

The prevailing aesthetic is defined by **precision, accessibility, and high contrast**. The "default" academic look has shifted away from bare-bones styling toward a more graphic, publication-ready presentation.

- **Vibe:** Professional, clean, and information-dense.
- **Backgrounds:** Heavy bias toward **stark white backgrounds** for maximum contrast in print and PDF reading. The "Seaborn-style" Light Grey (`#F0F0F0`) background remains an accepted variant.
- **Accessibility:** Strong emphasis on distinguishing data not just by color, but by texture (patterns) and shape (markers) to support black-and-white printing and colorblind readers.

---

## 2. Color Palettes

### Categorical Data

- **Soft Pastels:** Matte, low-saturation colors (salmon, sky blue, mint, lavender) to prevent visual fatigue.
- **Muted Earth Tones:** "Academic" palettes using olive, beige, slate grey, and navy.
- **High-Contrast Primaries:** Used sparingly when categories must be distinct (e.g., deep orange vs. vivid purple).
- **Accessibility Mode:** Combine color with **geometric patterns** (hatches, dots, stripes) to differentiate categories.

### Sequential & Heatmaps

- **Perceptually Uniform:** "Viridis" (blue-to-yellow) and "Magma/Plasma" (purple-to-orange) are the standard.
- **Diverging:** "Coolwarm" (blue-to-red) for positive/negative value splits.
- **Avoid:** The traditional "Jet/Rainbow" scale.

---

## 3. Axes & Grids

- **Grid lines:** Almost never solid. Use **fine dashed (`--`)** or **dotted (`:`)** lines in light gray.
- **Placement:** Grids rendered *behind* data elements (low Z-order).
- **Spines:**
  - **"Boxed" Look:** Full enclosure (black spines on all 4 sides) — very common.
  - **"Open" Look:** Remove top and right spines for minimalist appearance.
- **Ticks:** Subtle, facing inward, or removed entirely in favor of grid alignment.

---

## 4. Layout & Typography

- **Font Family:** Exclusively **Sans-Serif** (Helvetica, Arial, or DejaVu Sans). Serif fonts are rarely used for labels.
- **Label Rotation:** X-axis labels rotated **45 degrees** only when necessary; otherwise horizontal orientation preferred.
- **Legends:**
  - **Internal Placement:** Float inside the plot area (top-left or top-right) to maximize "data-ink ratio."
  - **Top Horizontal:** Single row above the plot title as alternative.
- **Annotations:** Direct labeling next to lines or on top of bars instead of forcing legend lookup.

---

## 5. Type-Specific Guidelines

### Bar Charts & Histograms

- **Borders:**
  - **High-Definition:** Black outlines around colored bars for high-contrast look.
  - **Borderless:** Solid color fills with no outline (often used with light grey backgrounds).
- **Grouping:** Bars grouped tightly, with significant whitespace between categorical groups.
- **Error Bars:** Consistently styled with **black, flat caps**.

### Line Charts

- **Markers:** Lines almost always include **geometric markers** (circles, squares, diamonds) at data points.
- **Line Styles:** Dashed lines (`--`) for theoretical limits, baselines, or secondary data. Solid lines for primary experimental data.
- **Uncertainty:** Semi-transparent **shaded bands** (confidence intervals) rather than simple vertical error bars.

### Pie / Donut Charts

- **Separators:** Thick **white borders** to separate slices or treemap blocks.
- **Structure:** Thick **Donut charts** preferred over traditional Pie charts.
- **Emphasis:** "Exploding" (detaching) a specific slice is a common technique to highlight a key statistic.

### Scatter Plots

- **Shape Coding:** Different marker shapes (circles vs. triangles) to encode a categorical dimension alongside color.
- **Fills:** Markers are typically solid and fully opaque.
- **3D Plots:** Depth emphasized by drawing "walls" with grids or using drop-lines to the "floor" of the plot.

### Heatmaps

- **Aspect Ratio:** Cells are almost strictly **square**.
- **Annotation:** Write the exact value (in white or black text) **inside the cell** rather than relying solely on a color bar.
- **Borders:** Cells often borderless (smooth gradient look) or separated by very thin white lines.

### Radar Charts

- **Fills:** Polygon area uses **translucent fills** (alpha ~0.2) to show grid lines underneath.
- **Perimeter:** Outer boundary marked by a solid, darker line.

### Dot / Lollipop Plots

- Used as a modern alternative to bar charts.
- Styled as "lollipops" (dots connected to the axis by a thin line).

---

## 6. Common Pitfalls

- **The "Excel Default" Look:** Avoid heavy 3D effects on bars, shadow drops, or serif fonts (Times New Roman) on axes.
- **The "Rainbow" Map:** Avoid Jet/Rainbow colormap — outdated and perceptually misleading.
- **Ambiguous Lines:** A line chart *without* markers can look ambiguous if data points are sparse; always add markers.
- **Over-reliance on Color:** Failing to use patterns or shapes to distinguish groups makes the plot inaccessible to colorblind readers.
- **Cluttered Grids:** Avoid solid black grid lines; they compete with the data. Always use light grey/dashed grids.
