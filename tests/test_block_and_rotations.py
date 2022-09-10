from numpy.testing import assert_allclose

from pymeshup import *

def test_create_default_cube():
    c = Box()

def test_create_nondefault_cube():
    c = Box(-1, 1, -2, 2, -3, 3)

def test_move():
    c = Box()
    c2 = c.move(1,2,3)

    expected = [[0.5, 1.5, 2.5],
       [1.5, 1.5, 2.5],
       [0.5, 2.5, 2.5],
       [1.5, 2.5, 2.5],
       [0.5, 1.5, 3.5],
       [1.5, 1.5, 3.5],
       [0.5, 2.5, 3.5],
       [1.5, 2.5, 3.5]]
    assert_allclose(expected, c2.vertices)


def test_rotated_cube():
    c = Box()
    c = c.rotate(x = 45)

def test_copy():
    c = Box()
    c2 = Volume(c)

def test_cylinder():
    c = Cylinder()
    Plot(c)

def test_cylinder_volume7():
    """Verifies that the volume of the meshed cylinder matches the volume of a perfect cylinder"""
    c = Cylinder(radius=1, height=1, resolution=7)
    pi = 3.141592654
    expected = pi
    assert_allclose(c.volume, expected)

def test_cylinder_volume3():
    """Verifies that the volume of the meshed cylinder matches the volume of a perfect cylinder"""
    c = Cylinder(radius=1, height=1, resolution=3)
    pi = 3.141592654
    expected = pi
    assert_allclose(c.volume, expected)

def test_cylinder_volume300():
    """Verifies that the volume of the meshed cylinder matches the volume of a perfect cylinder"""
    c = Cylinder(radius=2, height=10, resolution=300)
    pi = 3.141592654
    expected = 4*pi*10
    assert_allclose(c.volume, expected)

def test_plot_multiple():
    c = Cylinder()
    b = Box()
    Plot([c,b])

def test_volume_from_verts_and_faces():
    v = Volume()
    p = [(1,0,0),(0,1,0),(1,1,0),(0,0,1)]
    fid = [(0,1,2),(0,1,3),(1,2,3),(2,0,3)]
    v.set_vertices_and_faces(p,fid)
    Plot(v)