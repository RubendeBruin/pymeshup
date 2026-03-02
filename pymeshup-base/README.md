# pymeshup-base

Core meshing and volume functions from the [pymeshup](https://github.com/RubendeBruin/pymeshup) project.

This package provides the core functionality for meshing and volume operations without requiring a full GUI installation (no PySide6, no capytaine).

## Installation

```bash
pip install pymeshup-base
```

## Usage

```python
from pymeshup_base import Frame, Volume, Box, Cylinder, Hull

# Create a simple box
box = Box(-1, 1, -1, 1, -1, 1)

# Create a hull from frames
frame = Frame(0, 0, 1, 1, 0, 2)
hull = Hull(0, frame, 10, frame)
```

## What's included

- `Frame` – 2D cross-section slices
- `Volume`, `Box`, `Cylinder`, `Load`, `Plot` – 3D volume primitives and operations
- `Hull` – Hull construction from frames
- `GHSgeo` – GHS geometry file import
- `STEP` – STEP file import

## What's NOT included (use `pymeshup` for these)

- GUI / user interface (PySide6)
- Capytaine hydrodynamic analysis
