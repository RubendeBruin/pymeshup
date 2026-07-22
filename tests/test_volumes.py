import numpy as np
import pytest
from pathlib import Path
from pymeshup import Box, Cylinder, Plot, Load

HERE = Path(__file__).parent  # folder waarin dit testbestand staat


def test_crop():
    a = Box()
    a.crop(xmax=0)


def test_transform_translation():
    m = np.eye(4)
    m[:3, 3] = (1, 2, 3)

    a = Box().transform(m)

    assert a.bounds == pytest.approx((0.5, 1.5, 1.5, 2.5, 2.5, 3.5))


def test_transform_rotation():
    """90 degrees about the z-axis: x-extent and y-extent swap"""
    m = np.eye(4)
    m[:2, :2] = ((0, -1), (1, 0))

    a = Box(0, 2, 0, 1, 0, 1).transform(m)

    assert a.bounds == pytest.approx((-1, 0, 0, 2, 0, 1))


def test_transform_scaling():
    m = np.diag((2.0, 3.0, 4.0, 1.0))

    a = Box().transform(m)

    assert a.volume == pytest.approx(24)


def test_transform_accepts_nested_lists():
    a = Box().transform([[1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

    assert a.bounds == pytest.approx((0.5, 1.5, -0.5, 0.5, -0.5, 0.5))


def test_transform_is_non_destructive():
    a = Box()
    m = np.eye(4)
    m[:3, 3] = (1, 2, 3)

    a.transform(m)

    assert a.bounds == pytest.approx((-0.5, 0.5, -0.5, 0.5, -0.5, 0.5))


def test_transform_requires_4x4():
    with pytest.raises(ValueError):
        Box().transform(np.eye(3))


def test_transform_inverse_undoes_transform():
    """a.transform(M).transform_inverse(M) yields the original a"""
    m = np.array(
        [
            [0.0, -2.0, 0.0, 1.0],
            [3.0, 0.0, 0.0, 2.0],
            [0.0, 0.0, 4.0, 3.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )

    a = Box(0, 2, 0, 1, 0, 1)
    b = a.transform(m).transform_inverse(m)

    assert b.vertices == pytest.approx(a.vertices)
    assert b.bounds == pytest.approx(a.bounds)
    assert b.volume == pytest.approx(a.volume)


def test_transform_inverse_translation():
    m = np.eye(4)
    m[:3, 3] = (1, 2, 3)

    a = Box().transform_inverse(m)

    assert a.bounds == pytest.approx((-1.5, -0.5, -2.5, -1.5, -3.5, -2.5))


def test_transform_inverse_is_non_destructive():
    a = Box()
    m = np.eye(4)
    m[:3, 3] = (1, 2, 3)

    a.transform_inverse(m)

    assert a.bounds == pytest.approx((-0.5, 0.5, -0.5, 0.5, -0.5, 0.5))


def test_transform_inverse_requires_4x4():
    with pytest.raises(ValueError):
        Box().transform_inverse(np.eye(3))


def test_transform_inverse_of_singular_matrix():
    m = np.eye(4)
    m[1, 1] = 0  # flattens y, can not be undone

    with pytest.raises(ValueError):
        Box().transform_inverse(m)


@pytest.mark.interactive
def test_add():
    a = Box()
    c = Cylinder()

    p = a.add(c)

    Plot(p)


@pytest.mark.interactive
def test_load():
    a = Load(HERE / "cheetah.obj")
    Plot(a)
