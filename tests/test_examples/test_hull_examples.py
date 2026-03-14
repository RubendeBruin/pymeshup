"""
Tests for Hull examples shown in README.md.
"""

import pytest
from pymeshup import Frame, Hull


def _make_frames():
    """Return commonly-used frames for hull tests."""
    stern = Frame(0, 0, 1, 0, 1, 1).autocomplete()
    midship = Frame(0, 0, 2, 0, 2, 2).autocomplete()
    bow = Frame(0, 2)  # single-point sharp bow
    return stern, midship, bow


def test_hull_basic_construction():
    """Hull can be built from alternating position/Frame arguments."""
    stern, midship, bow = _make_frames()
    h = Hull(0, stern, 5, midship, 15, midship, 20, bow)
    assert h is not None


def test_hull_has_positive_volume():
    """A valid Hull has a positive volume."""
    stern, midship, bow = _make_frames()
    h = Hull(0, stern, 5, midship, 15, midship, 20, bow)
    assert h.volume > 0


def test_hull_bounds_x():
    """Hull extends from x=0 to x=20 as specified."""
    stern, midship, bow = _make_frames()
    h = Hull(0, stern, 5, midship, 15, midship, 20, bow)
    xmin, xmax, *_ = h.bounds
    assert abs(xmin - 0) < 0.1
    assert abs(xmax - 20) < 0.1


def test_hull_from_readme_quickstart():
    """README quick-start hull example runs without error."""
    midship = Frame(0, 0, 1, 0, 1, 2, 0, 2).autocomplete()
    bow = Frame(0, 1)
    hull = Hull(0, midship, 10, midship, 15, bow)
    assert hull.volume > 0


def test_hull_crop_above_waterline():
    """Cropping at zmin=0 keeps only the part above z=0."""
    midship = Frame(0, 0, 1, 0, 1, 2, 0, 2).autocomplete()
    bow = Frame(0, 1)
    hull = Hull(0, midship, 10, midship, 15, bow)
    above = hull.crop(zmin=0)
    # all vertices should be at z >= 0 (with small tolerance)
    assert above.vertices[:, 2].min() >= -0.01


def test_hull_odd_args_raises():
    """Hull with an odd number of arguments raises ValueError."""
    stern, _, _ = _make_frames()
    with pytest.raises(ValueError):
        Hull(0, stern, 5)


def test_hull_decreasing_x_raises():
    """Hull with non-increasing x positions raises ValueError."""
    stern, midship, _ = _make_frames()
    with pytest.raises(ValueError):
        Hull(10, stern, 5, midship)


def test_hull_non_frame_raises():
    """Passing a non-Frame object as a frame raises ValueError."""
    with pytest.raises(ValueError):
        Hull(0, "not_a_frame", 5, "also_not_a_frame")


def test_hull_from_file(tmp_path):
    """Hull can be loaded from a CSV file with the expected format.

    Row format:
      x, y1, y2, ...    ← first cell is x position; remaining are half-breadths
      , z1, z2, ...     ← first cell is empty; remaining are vertical heights
    """
    # Frame at x=0 and x=10: half-breadth 0→1, height 0→2
    # hull_from_file calls Frame(0, 0, 1, 2).autocomplete() → triangular section
    csv_content = (
        "0, 0, 1\n"
        ", 0, 2\n"
        "10, 0, 1\n"
        ", 0, 2\n"
    )
    csv_file = tmp_path / "frames.csv"
    csv_file.write_text(csv_content)
    h = Hull(str(csv_file))
    assert h is not None
    assert h.volume > 0

