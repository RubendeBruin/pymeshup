import pytest
from vtkmodules.vtkCommonDataModel import vtkPolyData

from pymeshup import Box, Cylinder, Plot


def test_to_polydata():
    b = Box()
    pd = b.to_polydata()

    assert isinstance(pd, vtkPolyData)


@pytest.mark.interactive
def test_simplify():
    b = Cylinder(resolution=100)
    s = b.simplify()

    Plot(s)
