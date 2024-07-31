from vtkmodules.vtkCommonDataModel import vtkPolyData

from pymeshup import *

def test_to_polydata():
    b = Box()
    pd = b.to_polydata()

    assert isinstance(pd, vtkPolyData)

def test_simplify():
    b = Cylinder(resolution=100)
    s = b.simplify()

    Plot(s)