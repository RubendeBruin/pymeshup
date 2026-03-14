"""
Tests for Box and Cylinder examples shown in README.md.
"""

import pytest
from pymeshup import Box, Cylinder


# ---------------------------------------------------------------------------
# Box
# ---------------------------------------------------------------------------

def test_box_unit_box_volume():
    """Default unit Box has a volume of exactly 1."""
    b = Box()
    assert abs(b.volume - 1.0) < 0.01


def test_box_custom_volume():
    """Box(0,5,-1,1,-2,0) should have volume ≈ 20."""
    tank = Box(xmin=0, xmax=5, ymin=-1, ymax=1, zmin=-2, zmax=0)
    assert abs(tank.volume - 20.0) < 0.1


def test_box_bounds():
    """Bounds of a custom Box match its construction arguments."""
    b = Box(xmin=1, xmax=3, ymin=-1, ymax=1, zmin=0, zmax=2)
    xmin, xmax, ymin, ymax, zmin, zmax = b.bounds
    assert abs(xmin - 1) < 0.01
    assert abs(xmax - 3) < 0.01
    assert abs(ymin - (-1)) < 0.01
    assert abs(ymax - 1) < 0.01
    assert abs(zmin - 0) < 0.01
    assert abs(zmax - 2) < 0.01


def test_box_move():
    """move() shifts the bounding box by the given offset."""
    b = Box(xmin=0, xmax=1, ymin=0, ymax=1, zmin=0, zmax=1)
    moved = b.move(x=10, y=0, z=0)
    xmin, xmax, *_ = moved.bounds
    assert abs(xmin - 10) < 0.05
    assert abs(xmax - 11) < 0.05


def test_box_scale():
    """scale() doubles the volume when one axis is doubled."""
    b = Box()
    scaled = b.scale(x=2)
    assert abs(scaled.volume - b.volume * 2) < 0.05


def test_box_mirrorXZ():
    """mirrorXZ() keeps volume equal to the original."""
    b = Box(xmin=0, xmax=1, ymin=0, ymax=1, zmin=0, zmax=1)
    mirrored = b.mirrorXZ()
    assert abs(mirrored.volume - b.volume) < 0.05


def test_box_crop():
    """crop(zmin=0) halves a vertically centred Box."""
    b = Box(xmin=-1, xmax=1, ymin=-1, ymax=1, zmin=-1, zmax=1)
    top_half = b.crop(zmin=0)
    # volume of the cropped box should be ≈ half the original
    assert abs(top_half.volume - b.volume / 2) < 0.1


def test_box_add():
    """add() produces a volume at least as large as either operand."""
    a = Box(xmin=0, xmax=1, ymin=0, ymax=1, zmin=0, zmax=1)
    b = Box(xmin=2, xmax=3, ymin=0, ymax=1, zmin=0, zmax=1)
    combined = a.add(b)
    assert combined.volume >= a.volume - 0.05


def test_box_remove():
    """remove() reduces the volume."""
    outer = Box(xmin=-2, xmax=2, ymin=-2, ymax=2, zmin=0, zmax=4)
    inner = Box(xmin=-1, xmax=1, ymin=-1, ymax=1, zmin=0, zmax=4)
    hollow = outer.remove(inner)
    assert hollow.volume < outer.volume


def test_box_inside_of():
    """inside_of() returns only the intersection part."""
    a = Box(xmin=0, xmax=2, ymin=0, ymax=1, zmin=0, zmax=1)
    b = Box(xmin=1, xmax=3, ymin=0, ymax=1, zmin=0, zmax=1)
    common = a.inside_of(b)
    assert common.volume < a.volume
    assert common.volume < b.volume


def test_box_cut_at_waterline():
    """cut_at_waterline() keeps only the submerged (z≤0) part."""
    b = Box(xmin=-1, xmax=1, ymin=-1, ymax=1, zmin=-2, zmax=2)
    sub = b.cut_at_waterline()
    # all vertices should have z ≤ 0 (plus a tiny tolerance)
    assert sub.vertices[:, 2].max() < 0.01


def test_box_cut_at_xz():
    """cut_at_xz() keeps only the y≤0 half."""
    b = Box(xmin=-1, xmax=1, ymin=-2, ymax=2, zmin=0, zmax=1)
    port = b.cut_at_xz()
    assert port.vertices[:, 1].max() < 0.01


def test_box_save_load(tmp_path):
    """Saved volume can be reloaded and has a comparable volume."""
    from pymeshup import Load
    b = Box()
    stl_path = str(tmp_path / "box.stl")
    b.save(stl_path)
    loaded = Load(stl_path)
    assert abs(loaded.volume - b.volume) < 0.01


# ---------------------------------------------------------------------------
# Cylinder
# ---------------------------------------------------------------------------

def test_cylinder_volume():
    """Cylinder volume ≈ π r² h."""
    from math import pi
    h, r = 4.0, 1.0
    cyl = Cylinder(height=h, radius=r)
    expected = pi * r ** 2 * h
    assert abs(cyl.volume - expected) < 0.05 * expected  # within 5 %


def test_cylinder_bounds_z():
    """Cylinder base starts at z=0 and extends to z=height."""
    cyl = Cylinder(height=3, radius=0.5)
    _, _, _, _, zmin, zmax = cyl.bounds
    assert abs(zmin) < 0.05
    assert abs(zmax - 3) < 0.05


def test_cylinder_move():
    """After move, the cylinder base is at the new z position."""
    cyl = Cylinder(height=2, radius=1).move(z=5)
    _, _, _, _, zmin, zmax = cyl.bounds
    assert abs(zmin - 5) < 0.05
    assert abs(zmax - 7) < 0.05

