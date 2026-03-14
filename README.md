# PyMeshUp

PyMeshUp provides an easy way to create and modify volume meshes using Python.
It combines functionality from [pymeshlab](https://github.com/cnr-isti-vclab/PyMeshLab),
[VTK](https://vtk.org/) and [CadQuery](https://cadquery.readthedocs.io/).
Optional 3D visualization is available via [vedo](https://vedo.embl.es/).

---

## Installation

```bash
pip install pymeshup
```

For 3D visualization:

```bash
pip install vedo
```

---

## Quick-start example

```python
from pymeshup import Frame, Hull, Box, Cylinder, Plot

# Define cross-sections
midship = Frame(0, 0,  1, 0,  1, 2,  0, 2).autocomplete()   # rectangular half-frame, mirrored
bow     = Frame(0, 1)                                         # single point → sharp bow

# Build a hull
hull = Hull(0, midship, 10, midship, 15, bow)

# Combine with a box to keep only the above-waterline part
above_water = hull.crop(zmin=0)

Plot([hull, above_water])
```

---

## API Reference

### `Frame`

A **Frame** is a 2-D cross-section (slice).
Axes convention: **X → right**, **Y → up**.

#### Construction

```python
from pymeshup import Frame

# From flat coordinate list  x1,y1, x2,y2, ...
f = Frame(0, 0,  1, 0,  1, 1,  0, 1)

# From separate x and y lists
f = Frame.from_xy([0, 1, 1, 0], [0, 0, 1, 1])

# Single point (used as a sharp tip)
tip = Frame(0, 1)
```

The polygon is **automatically closed** (first point appended to the end if needed).

#### Methods

| Method | Description |
|---|---|
| `frame.autocomplete()` | Mirror the half-frame over the `x = 0` centre-line and return the full closed frame. |
| `frame.scaled(x=1, y=1)` | Return a scaled copy. |
| `frame.copy()` | Return an identical copy. |
| `frame.center()` | Return the `(x, y)` centroid. |
| `frame.is_identical_to(other)` | Return `True` if both frames share all the same points. |

#### Properties

| Property | Description |
|---|---|
| `frame.x` | List of x-coordinates. |
| `frame.y` | List of y-coordinates. |
| `frame.xy` | Tuple of `(x, y)` pairs. |
| `frame.n` | Number of points (including the closing duplicate). |

#### Example

```python
from pymeshup import Frame

# Half-frame: bottom-centre → bilge → side → deck
half = Frame(0, 0,  1, 0,  1.5, 0.5,  1.5, 2)

# Mirror to full frame
full = half.autocomplete()
print(full.xy)
# ((0,0),(1,0),(1.5,0.5),(1.5,2),(-1.5,2),(-1.5,0.5),(-1,0),(0,0))
```

---

### `Volume`

A **Volume** is a triangulated 3-D mesh.  All operations return a **new** Volume (non-destructive).

#### Boolean operations

```python
from pymeshup import Box, Cylinder

box = Box(xmin=-1, xmax=1, ymin=-1, ymax=1, zmin=0, zmax=2)
cyl = Cylinder(height=2, radius=0.4)

combined    = box.add(cyl)          # union
hollow      = box.remove(cyl)       # difference – cylinder removed from box
common_part = box.inside_of(cyl)    # intersection
```

#### Transformations

```python
vol = Box()

moved   = vol.move(x=1, y=0, z=0.5)          # translate
scaled  = vol.scale(x=2, y=1, z=1)            # non-uniform scale
rotated = vol.rotate(x=0, y=0, z=45)          # Euler angles in degrees
mirror  = vol.mirrorXZ()                       # mirror in the XZ plane (negate Y)
```

#### Cropping / cutting

```python
vol = Box(xmin=-2, xmax=2, ymin=-2, ymax=2, zmin=-2, zmax=2)

cropped       = vol.crop(zmin=0)               # keep z >= 0
submerged     = vol.cut_at_waterline()         # keep z <= 0
port_side     = vol.cut_at_xz()               # keep y <= 0
```

#### Mesh quality

```python
vol = Hull(0, frame_a, 10, frame_b)

remeshed = vol.regrid(iterations=20, pct=1)        # isotropic remeshing
cleaned  = vol.merge_close_vertices(pct=1)          # weld near-coincident vertices
simple   = vol.simplify()                           # decimate (reduce face count)
```

#### Persistence

```python
vol.save("my_mesh.stl")      # save to STL (or any format pymeshlab supports)
```

#### Properties

| Property | Description |
|---|---|
| `vol.vertices` | `numpy` array of vertex positions `(N, 3)`. |
| `vol.volume` | Signed volume (float). |
| `vol.center` | Centre of mass `[x, y, z]`. |
| `vol.bounds` | `(xmin, xmax, ymin, ymax, zmin, zmax)`. |

---

### `Box`

Creates a box-shaped volume.

```python
from pymeshup import Box

# Unit box centred at the origin
unit_box = Box()

# Custom box
tank = Box(xmin=0, xmax=5, ymin=-1, ymax=1, zmin=-2, zmax=0)
print(tank.volume)   # ≈ 20.0
```

**Signature:** `Box(xmin=-0.5, xmax=0.5, ymin=-0.5, ymax=0.5, zmin=-0.5, zmax=0.5)`

---

### `Cylinder`

Creates a vertical cylinder with its **base at the origin**.

```python
from pymeshup import Cylinder

cyl = Cylinder(height=3, radius=0.5, resolution=36)
print(cyl.bounds)   # (xmin, xmax, ymin, ymax, 0, 3)
```

**Signature:** `Cylinder(height=1, radius=1, resolution=36)`

The radius is adjusted so that the **discretised** cylinder has the exact target volume.

---

### `Hull`

Builds a hull mesh by lofting a sequence of `Frame` cross-sections along the X axis.

```python
from pymeshup import Frame, Hull

stern   = Frame(0, 0,  1, 0,  1, 1).autocomplete()
midship = Frame(0, 0,  2, 0,  2, 2).autocomplete()
bow     = Frame(0, 2)    # sharp tip

# Hull(x0, frame0, x1, frame1, ..., xn, framen)
vessel = Hull(0, stern,  5, midship,  15, midship,  20, bow)
print(vessel.volume)
```

**Load from CSV file:**

```python
vessel = Hull("my_hull_frames.csv")
```

CSV format (tab- or comma-separated):

```
x_pos, y1, y2, ...
      , z1, z2, ...
x_pos, y1, y2, ...
      , z1, z2, ...
```

---

### `Load`

Loads an existing mesh file (STL, OBJ, PLY, …).

```python
from pymeshup import Load

mesh = Load("path/to/model.stl")
print(mesh.volume)
```

---

### `Plot`

Visualises one or more volumes interactively (requires **vedo**).

```python
from pymeshup import Box, Cylinder, Plot

a = Box()
b = Cylinder().move(z=1)

Plot([a, b])    # pass a list for multiple volumes
Plot(a)         # or a single volume
```

Install vedo with `pip install vedo`.

---

### `STEP`

Loads a STEP file via [CadQuery](https://cadquery.readthedocs.io/) and converts it to a `Volume`.

```python
from pymeshup import STEP

stp = STEP("model.step", scale=0.001)   # scale: e.g. mm → m
vol = stp.to_volume(angular_tolerance=5, linear_tolerance=1)
print(vol.bounds)
```

**`STEP.to_volume` arguments:**

| Argument | Default | Description |
|---|---|---|
| `angular_tolerance` | `5` | Angular tolerance for tessellation (degrees). |
| `linear_tolerance` | `1` | Linear tolerance for tessellation. |
| `filename` | `None` | If provided, the intermediate STL is saved to this path. |

---

### `GHSgeo`

Reads a **GHS Geometry File** (`.GF`) and makes individual parts and shapes available as `Volume` objects.

```python
from pymeshup import GHSgeo

geo = GHSgeo("vessel.GF")

# Access a named part
hull_volume = geo["HULL"]          # equivalent to geo.get_volume("HULL")

# Access raw (un-autocompleted) shapes by name
raw_shape = geo.shapes_raw["s1"]
print(raw_shape.bounds)
```

| Attribute | Description |
|---|---|
| `geo.parts` | Dictionary of parsed parts, each containing a `"volume"` key. |
| `geo.shapes_raw` | Dictionary of shapes as read from the file. |
| `geo.warnings` | List of warning messages encountered during parsing. |

---

## Full worked example

```python
from pymeshup import Frame, Hull, Box, Cylinder, Plot

# --- 1. Build a simple hull ---
half_frame = Frame(0, 0,   3, 0,   3.5, 1,   3.5, 4)
midship    = half_frame.autocomplete()
bow        = Frame(0, 4)        # sharp bow at deck height

hull = Hull(0, midship,  8, midship,  12, bow)

# --- 2. Add a cylindrical funnel on top ---
funnel = Cylinder(height=2, radius=0.4).move(x=4, z=4)

# --- 3. Hollow out an engine-room box ---
engine_room = Box(xmin=1, xmax=5, ymin=-1.5, ymax=1.5, zmin=0, zmax=3)
hull_with_room = hull.remove(engine_room)

# --- 4. Combine ---
ship = hull_with_room.add(funnel)

print(f"Ship volume : {ship.volume:.1f} m³")
print(f"Bounding box: {ship.bounds}")

# Plot(ship)   # uncomment if vedo is installed
```
