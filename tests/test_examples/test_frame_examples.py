"""
Tests for the Frame examples shown in README.md.
"""

import pytest
from numpy.testing import assert_allclose
from pymeshup import Frame


def test_frame_from_flat_coords():
    """Frame can be constructed from a flat coordinate list."""
    f = Frame(0, 0, 1, 0, 1, 1, 0, 1)
    assert f.n == 5  # 4 unique + auto-close


def test_frame_from_xy():
    """Frame.from_xy constructs the same frame as the flat-list form."""
    f_flat = Frame(0, 0, 1, 0, 1, 1, 0, 1)
    f_xy = Frame.from_xy([0, 1, 1, 0], [0, 0, 1, 1])
    assert f_flat.is_identical_to(f_xy)


def test_frame_single_point_tip():
    """A single-point frame (sharp tip) stores one pair."""
    tip = Frame(0, 1)
    assert tip.n == 1
    assert tip.xy == ((0, 1),)


def test_frame_autocomplete_readme_example():
    """autocomplete() mirrors a half-frame over x=0 correctly."""
    half = Frame(0, 0, 1, 0, 1.5, 0.5, 1.5, 2)
    full = half.autocomplete()

    expected = (
        (0, 0),
        (1, 0),
        (1.5, 0.5),
        (1.5, 2),
        (-1.5, 2),
        (-1.5, 0.5),
        (-1, 0),
        (0, 0),
    )
    assert_allclose(full.xy, expected)


def test_frame_scaled_returns_new_frame():
    """scaled() returns a new Frame, leaving the original unchanged."""
    f = Frame(0, 0, 1, 0, 1, 1, 0, 1)
    scaled = f.scaled(x=2, y=3)
    assert scaled is not f


def test_frame_copy_is_identical():
    """copy() produces a frame equal to the original."""
    f = Frame(0, 0, 1, 0, 1, 2, 0, 2)
    f2 = f.copy()
    assert f.is_identical_to(f2)
    assert f2 is not f


def test_frame_center():
    """center() returns the mean of all vertices including the closing duplicate."""
    f = Frame(0, 0, 2, 0, 2, 2, 0, 2)
    cx, cy = f.center()
    # Frame(0,0,2,0,2,2,0,2) → 5 points (auto-close appends (0,0))
    # mean x = (0+2+2+0+0)/5 = 0.8,  mean y = (0+0+2+2+0)/5 = 0.8
    assert abs(cx - 0.8) < 0.05
    assert abs(cy - 0.8) < 0.05


def test_frame_is_identical_to_true():
    """Two frames built from the same data are identical."""
    f1 = Frame(0, 0, 1, 0, 1, 1).autocomplete()
    f2 = Frame(0, 0, 1, 0, 1, 1).autocomplete()
    assert f1.is_identical_to(f2)


def test_frame_is_identical_to_false():
    """Two different frames are not identical."""
    f1 = Frame(0, 0, 1, 0, 1, 1)
    f2 = Frame(0, 0, 2, 0, 2, 1)
    assert not f1.is_identical_to(f2)


def test_frame_properties_x_y():
    """x and y properties return the correct coordinate lists."""
    f = Frame(0, 0, 3, 4)
    assert f.x == [0, 3, 0]
    assert f.y == [0, 4, 0]


