------------------------------------------------------------
DEPENDENCIES
------------------------------------------------------------

Required:
- Python 3.x
- numpy
- matplotlib

Optional / implicit:
- LaTeX installation (only required if usetex=True or LaTeX
  rendering is enabled in colplot)

No external or non-standard Python packages are required.


------------------------------------------------------------
MODULE OVERVIEW
------------------------------------------------------------

The module provides the following main groups of functionality:

1. Global matplotlib configuration
2. Line plotting helpers (single and subplots)
3. Contour and colour plotting helpers
4. File reading utilities for parameter scans
5. Adaptive data downsampling


------------------------------------------------------------
FUNCTIONS
------------------------------------------------------------

-------------------------
_configure_rcparams(...)
-------------------------
Internal helper to configure matplotlib rcParams in a consistent
way across all plotting functions.

Controls:
- Font size and family
- Axis border width
- Tick size, direction, and placement
- Optional LaTeX rendering

Users typically do not need to call this directly.


-------------------------
difplot(...)
-------------------------
Primary line-plotting function.

Designed for plotting one or more y(x) datasets with:
- Automatic styling
- Optional random or colormap-based colouring
- Log or linear axes
- Axis scaling factors
- Legends, vertical lines, annotations, and shaded regions

Typical use case:
Plotting solutions of differential equations or multiple
parameter curves on a single axis.

Output:
- Saves figure as PDF


-------------------------
difSubPlot(...)
-------------------------
Creates a two-panel vertical subplot with similar behaviour
to difplot, but with reduced feature set.

Useful for:
- Comparing two related datasets
- Showing different regimes or parameter ranges

Output:
- Saves figure as JPEG


-------------------------
contplot(...)
-------------------------
Contour-only plotting utility.

Supports:
- Multiple contour levels
- Overlaid contour sets
- Inline or legend-based labelling
- Optional return of contour vertices for post-processing

Typical use case:
Threshold curves, phase boundaries, or exclusion contours.

Output:
- Saves figure as PDF
- Optionally returns contour point arrays


-------------------------
colplot(...)
-------------------------
Colour (pcolor) plot with overlaid contours.

Supports:
- Linear or logarithmic colour normalisation
- Multiple overlaid contour families
- Legend handling for contours
- LaTeX-rendered labels

Typical use case:
Heatmaps, density plots, or 2D parameter scans.

Output:
- Saves figure as PDF
- Optionally returns contour point arrays


-------------------------
read(...)
-------------------------
Bulk file reader for multi-dimensional datasets.

Designed for directory structures where filenames encode a
parameter value (e.g. mass, field strength).

Features:
- Automatic filename parsing
- Optional reference checking
- NaN detection
- Sorting by parameter value

Returns:
- [parameter_values, data_arrays]


-------------------------
read1D(...)
-------------------------
Simplified reader for scalar or 1D data stored in multiple files.

Typical use case:
Reading single output values per parameter point.

Returns:
- [values, parameter_values]


-------------------------
sample(...)
-------------------------
Adaptive downsampling routine for 2D data [x, y].

Purpose:
Reduce the number of points while preserving:
- Overall behaviour
- Steep gradients
- Full x-range coverage
- Maximum allowed spacing

Useful for:
- Plotting very large datasets
- Reducing storage or rendering cost

Returns:
- Downsampled array of shape (N, 2)


------------------------------------------------------------
DESIGN NOTES
------------------------------------------------------------

- This module intentionally avoids object-oriented design.
- Functions are explicit and verbose by design for transparency.
- Several functions assume familiarity with matplotlib internals.
- Some optional features (e.g. Mline, top axis transforms) rely
  on external global variables and are intended for specialised
  workflows.


------------------------------------------------------------
OUTPUT FORMATS
------------------------------------------------------------

- Line plots: PDF
- Contour plots: PDF
- Colour plots: PDF
- Subplots: JPEG

All output paths and filenames are user-configurable.
