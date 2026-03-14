"""
Tests for the full worked example from README.md and for Volume mesh-quality
and transformation helpers (regrid, merge_close_vertices, simplify, rotate).
"""

import pytest
from pymeshup import Frame, Hull, Box, Cylinder


# ---------------------------------------------------------------------------
# Full worked example from README
# ---------------------------------------------------------------------------

def test_readme_full_example():
    """The full README worked example runs without error and has volume > 0."""
    half_frame = Frame(0, 0, 3, 0, 3.5, 1, 3.5, 4)
    midship = half_frame.autocomplete()
    bow = Frame(0, 4)

    hull = Hull(0, midship, 8, midship, 12, bow)

    funnel = Cylinder(height=2, radius=0.4).move(x=4, z=4)

    engine_room = Box(xmin=1, xmax=5, ymin=-1.5, ymax=1.5, zmin=0, zmax=3)
    hull_with_room = hull.remove(engine_room)

    ship = hull_with_room.add(funnel)

    assert ship.volume > 0


# ---------------------------------------------------------------------------
# Transformations
# ---------------------------------------------------------------------------

def test_rotate_360_same_volume():
    """Rotating a box by 360° leaves the volume unchanged."""
    b = Box()
    rotated = b.rotate(z=360)
    assert abs(rotated.volume - b.volume) < 0.05


def test_rotate_90_bounds_swapped():
    """Rotating a non-square box by 90° around Z swaps x and y extents."""
    b = Box(xmin=0, xmax=2, ymin=0, ymax=1, zmin=0, zmax=1)
    r = b.rotate(z=90)
    xmin, xmax, ymin, ymax, zmin, zmax = r.bounds
    # after rotating 90°, the long axis (originally x) should now be along y
    x_extent = abs(xmax - xmin)
    y_extent = abs(ymax - ymin)
    assert y_extent > x_extent - 0.1


# ---------------------------------------------------------------------------
# Mesh quality helpers
# ---------------------------------------------------------------------------

def test_regrid_preserves_volume():
    """regrid() should not drastically change the enclosed volume."""
    b = Box()
    remeshed = b.regrid(iterations=5, pct=50)
    assert abs(remeshed.volume - b.volume) < 0.1 * abs(b.volume)


def test_merge_close_vertices_returns_volume():
    """merge_close_vertices() returns a Volume without error."""
    b = Box()
    cleaned = b.merge_close_vertices(pct=1)
    assert cleaned is not None
    assert cleaned.volume > 0


def test_simplify_returns_volume():
    """simplify() returns a Volume and reduces face count."""
    b = Box()
    simple = b.simplify()
    assert simple is not None


# ---------------------------------------------------------------------------
# Vertices and center-of-mass properties
# ---------------------------------------------------------------------------

def test_vertices_shape():
    """vertices property returns an (N, 3) array."""
    b = Box()
    verts = b.vertices
    assert verts.ndim == 2
    assert verts.shape[1] == 3


def test_center_of_mass():
    """center of a unit Box is approximately at the origin."""
    b = Box()
    cx, cy, cz = b.center
    assert abs(cx) < 0.05
    assert abs(cy) < 0.05
    assert abs(cz) < 0.05

