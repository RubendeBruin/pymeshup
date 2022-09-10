from numpy.testing import assert_allclose

from pymeshup import *
from pytest import raises

def test_create():
    f = Frame(1,2,3,4)


def test_create_wrong1():
    with raises(ValueError):
        f = Frame(1, 2, 3, 4,5)


def test_create_wrong2():
    with raises(ValueError):
        f = Frame(1, 2, 'drie', 4)

def test_autoclose():

    f = Frame(1,2,3,4)
    expected = [(1,2),(3,4),(1,2)]

    assert_allclose(expected, f.xy)


def test_autocomplete():
    f = Frame(1, 2, 3, 4).autocomplete()
    expected = ((1,2),(3,4),(-3,4),(-1,2), (1,2))

    assert_allclose(expected, f.xy)

def test_zero_frame():
    with raises(ValueError):
        f = Frame()

def test_onepoint_frame():
    f = Frame(1,2)
    assert_allclose(f.xy, [(1,2)])
