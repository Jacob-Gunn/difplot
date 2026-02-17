# difplot

A lightweight plotting utility built on top of `matplotlib` for
visualizing differential equation solutions and structured scientific
data.\
The module provides:

-   A configurable plotting wrapper (`difplot`) for high-quality
    publication-style figures.
-   A behavior-preserving downsampling routine (`sample`) for large 2D
    datasets.

------------------------------------------------------------------------

## Installation

This module depends on:

-   numpy
-   matplotlib

Install dependencies via:

``` bash
pip install numpy matplotlib
```

Place `difplot.py` in your project directory and import:

``` python
from difplot import difplot, sample
```

------------------------------------------------------------------------

## difplot

### Purpose

`difplot` is a high-level wrapper around matplotlib designed for
scientific plotting of:

-   Multiple curves
-   Contour overlays
-   Filled regions
-   Log/linear scaling
-   Publication-style formatting

Figures are automatically exported as PDF.

------------------------------------------------------------------------

### Basic Usage

``` python
import numpy as np
from difplot_v2 import difplot

x = np.linspace(0, 10, 1000)
y1 = np.sin(x)
y2 = np.cos(x)

difplot(
    xlist=[x, x],
    ylist=[y1, y2],
    xlabel="x",
    ylabel=["f(x)", "sin(x)", "cos(x)"],
    name="example_plot"
)
```

This generates:

    example_plot.pdf

------------------------------------------------------------------------

### Core Parameters

Required:

-   `xlist`: list of x-arrays
-   `ylist`: list of y-arrays
-   `xlabel`: string
-   `ylabel`: string or list

Common optional controls:

-   `figx`, `figy`: figure size
-   `fontSize`: base font size
-   `DPI`: export resolution
-   `color`: list or `"random"`
-   `linestyle`: list of line styles
-   `xscale`, `yscale`: `"linear"` or `"log"`
-   `xspan`, `yspan`: axis limits
-   `vertical`: vertical reference lines
-   `text`: annotations
-   `fill`: shaded regions
-   `contours`: contour overlays
-   `usetex`: enable LaTeX rendering

Output:

The figure is saved as:

    <path><name>.pdf

------------------------------------------------------------------------

## Contour Overlays

Contours can be added using:

``` python
difplot(
    xlist=X,
    ylist=Y,
    zlist=Z,
    contours=(levels, colors, linestyles),
    label_contours=[True],
    zlabel="z"
)
```

Supports:

-   Multiple Z datasets
-   Per-level styling
-   Selective labeling

------------------------------------------------------------------------

## sample

### Purpose

`sample` reduces a dense 2D dataset `[x, y]` to `N` representative
points while:

-   Preserving steep gradients
-   Enforcing full x-range coverage
-   Respecting maximum spacing constraints

------------------------------------------------------------------------

### Usage

``` python
import numpy as np
from difplot_v2 import sample

data = np.column_stack((x, y))
reduced = sample(data, N=200)
```

------------------------------------------------------------------------

### Parameters

-   `data`: array shape (M, 2)
-   `N`: target number of points
-   `tol`: adaptive slope tolerance
-   `maxD`: maximum spacing in x
-   `max_iter`: iteration limit

Returns:

    np.ndarray of shape (N, 2)

------------------------------------------------------------------------

## Design Philosophy

-   Minimal global rc configuration
-   Publication-oriented defaults
-   Explicit control over styling
-   Flexible contour normalization
-   Deterministic PDF export

------------------------------------------------------------------------

## License

Use and modify freely within your research or applications.
