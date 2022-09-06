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