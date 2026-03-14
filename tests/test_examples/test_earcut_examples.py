"""
Tests for the polygon-triangulation helpers documented in README.md.

Covers:
  - triangulate_poly          (auto VTK → earcut fallback)
  - triangulate_poly_py       (pure-Python ear-clipping)
  - is_clockwise
  - is_point_inside_triangle
  - find_plane
  - triangulate_ear_clipping_2d
"""

import pytest
import numpy as np
from numpy.testing import assert_allclose

from pymeshup.helpers.triangulate_non_convex import triangulate_poly
from pymeshup.helpers.earcut_2d import (
    is_clockwise,
    is_point_inside_triangle,
    find_plane,
    triangulate_ear_clipping_2d,
    triangulate_poly_py,
)


# ---------------------------------------------------------------------------
# triangulate_poly  (README example verbatim)
# ---------------------------------------------------------------------------

RECT_VERTS = [
    (-60,  0.0, 0.0),
    (-60, -2.5, 0.0),
    (-60, -2.5, 4.0),
    (-60,  0.0, 4.0),
    (-60,  2.5, 4.0),
    (-60,  2.5, 0.0),
    (-60,  0.0, 0.0),   # closing point
]


def test_triangulate_poly_returns_four_triangles():
    """README example: rectangular section produces 4 triangles."""
    verts, faces = triangulate_poly(RECT_VERTS)
    assert len(faces) == 4


def test_triangulate_poly_vertices_passthrough():
    """verts returned by triangulate_poly equals the input."""
    verts, faces = triangulate_poly(RECT_VERTS)
    assert_allclose(verts, RECT_VERTS)


def test_triangulate_poly_face_indices_in_range():
    """Every face index must reference a valid vertex."""
    verts, faces = triangulate_poly(RECT_VERTS)
    n = len(verts)
    for face in faces:
        for idx in face:
            assert 0 <= idx < n


def test_triangulate_poly_triangle_count_formula():
    """A simple polygon with N unique vertices produces N-2 triangles."""
    # hexagon (6 unique vertices, no closing duplicate)
    import math
    r = 1.0
    hex_verts = [(0, r * math.cos(2 * math.pi * i / 6),
                     r * math.sin(2 * math.pi * i / 6))
                 for i in range(6)]
    # Do NOT append a closing point; VTK counts each entry as a unique vertex.

    _verts, faces = triangulate_poly(hex_verts)
    assert len(faces) == 4   # 6 vertices → 6 - 2 = 4 triangles


# ---------------------------------------------------------------------------
# triangulate_poly_py  (pure-Python earcut, README example)
# ---------------------------------------------------------------------------

NON_PLANAR_VERTS = [
    (-60,  0.0, 0.0),
    (-60, -2.5, 0.0),
    (-60, -2.5, 4.0),
    (-60,  0.0, 4.0),
    (-61,  1.0, 5.0),   # off-plane vertex
    (-60,  2.5, 0.0),
    (-60,  0.0, 0.0),
]


def test_triangulate_poly_py_returns_tuples():
    """triangulate_poly_py returns (verts, faces)."""
    verts, faces = triangulate_poly_py(NON_PLANAR_VERTS)
    assert verts is not None
    assert faces is not None


def test_triangulate_poly_py_face_count():
    """A 7-point polygon (6 unique + close) produces 5 triangles."""
    verts, faces = triangulate_poly_py(NON_PLANAR_VERTS)
    n_unique = len(NON_PLANAR_VERTS) - 1   # closing duplicate removed inside
    assert len(faces) == n_unique - 2


def test_triangulate_poly_py_planar_input():
    """Pure-Python earcut works on a plain planar rectangle too."""
    planar = [
        (0, 0, 0),
        (0, 1, 0),
        (0, 1, 1),
        (0, 0, 1),
        (0, 0, 0),
    ]
    _verts, faces = triangulate_poly_py(planar)
    assert len(faces) == 2   # 4 unique vertices → 2 triangles


# ---------------------------------------------------------------------------
# is_clockwise
# ---------------------------------------------------------------------------

def test_is_clockwise_ccw_square():
    """Counter-clockwise square returns False."""
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    assert is_clockwise(square) is False


def test_is_clockwise_cw_square():
    """Clockwise square returns True."""
    square = [(0, 0), (0, 1), (1, 1), (1, 0)]
    assert is_clockwise(square) is True


def test_is_clockwise_triangle_ccw():
    triangle = [(0, 0), (1, 0), (0.5, 1)]
    assert is_clockwise(triangle) is False


# ---------------------------------------------------------------------------
# is_point_inside_triangle
# ---------------------------------------------------------------------------

def test_point_inside_triangle_true():
    """Centroid of a triangle is inside it."""
    a, b, c = (0, 0), (3, 0), (0, 3)
    centroid = (1, 1)
    assert is_point_inside_triangle(centroid, a, b, c) is True


def test_point_inside_triangle_false():
    """Point clearly outside is not inside."""
    a, b, c = (0, 0), (1, 0), (0, 1)
    outside = (5, 5)
    assert is_point_inside_triangle(outside, a, b, c) is False


def test_point_on_vertex_is_inside():
    """A vertex of the triangle is considered 'inside' (on boundary)."""
    a, b, c = (0, 0), (2, 0), (1, 2)
    assert is_point_inside_triangle(a, a, b, c) is True


# ---------------------------------------------------------------------------
# find_plane
# ---------------------------------------------------------------------------

def test_find_plane_returns_orthonormal_axes():
    """find_plane returns two orthonormal vectors that are perpendicular to each other."""
    verts = np.array([
        (-60, 0.0, 0.0),
        (-60, 2.5, 0.0),
        (-60, 2.5, 4.0),
        (-60, 0.0, 4.0),
    ], dtype=float)

    ux, uy = find_plane(verts)

    # Each axis should have unit length
    assert abs(np.linalg.norm(ux) - 1.0) < 1e-9
    assert abs(np.linalg.norm(uy) - 1.0) < 1e-9

    # They should be perpendicular
    assert abs(np.dot(ux, uy)) < 1e-9


def test_find_plane_xy_polygon():
    """Polygon in the XY plane gives ux/uy both in-plane."""
    verts = np.array([
        (0, 0, 0),
        (1, 0, 0),
        (1, 1, 0),
        (0, 1, 0),
    ], dtype=float)
    ux, uy = find_plane(verts)
    # z-component of both ux and uy must be zero (they lie in the XY plane)
    assert abs(ux[2]) < 1e-9
    assert abs(uy[2]) < 1e-9


# ---------------------------------------------------------------------------
# triangulate_ear_clipping_2d
# ---------------------------------------------------------------------------

def test_ear_clipping_square():
    """A counter-clockwise square is split into 2 triangles."""
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    faces = triangulate_ear_clipping_2d(square)
    assert len(faces) == 2
    # All indices in range
    for tri in faces:
        for idx in tri:
            assert 0 <= idx < len(square)


def test_ear_clipping_pentagon():
    """A pentagon produces 3 triangles."""
    import math
    pentagon = [(math.cos(2 * math.pi * i / 5),
                 math.sin(2 * math.pi * i / 5))
                for i in range(5)]
    faces = triangulate_ear_clipping_2d(pentagon)
    assert len(faces) == 3


def test_ear_clipping_readme_example():
    """README example: CCW square → triangles use indices in [0, 3]."""
    square = [(0, 0), (1, 0), (1, 1), (0, 1)]
    triangles = triangulate_ear_clipping_2d(square)
    all_indices = {idx for tri in triangles for idx in tri}
    assert all_indices <= {0, 1, 2, 3}

