from numpy.testing import assert_allclose
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCellArray
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator

from pymeshup import *
from pytest import raises

from pymeshup.helpers.triangulate_non_convex import triangulate_poly


def test_create():
    f = Frame(1,2,3,4)

def test_scaled():
    f = Frame(1, 2, 3, 4)
    f2 = f.scaled(2, 3)


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

def test_mesh_frame():
    import numpy as np

    points = np.array([
        [0, 0], [1, 0], [1, 1], [2, 1],[2,0],[4,0],[4,2],[3,1.7],[0,2],[0,0]
    ])

    f = Frame(*points.flatten())

    points, faces = f.to_plane_at(0)

    import matplotlib.pyplot as plt

    for tri in faces:

        # get vertices
        t = [points[i] for i in tri]
        t.append(t[0])


        plt.plot([p[1] for p in t], [p[2] for p in t], 'r-')

    plt.show()

def test_frame_to_plane4():
    f = Frame(0,0,
              1,0,
              1,1,
              0,1)

    vertices, faces = f.to_plane_at(0)

def test_frame_to_plane3():
    f = Frame(0, 0,
              1, 0,
              1, 1)

    vertices, faces = f.to_plane_at(0)

    #
    #
    # # make a vtk polydata object from these points
    # vtkPts = vtkPoints()
    # for p in points:
    #     vtkPts.InsertNextPoint(p[0], p[1], 0)
    #
    #  # add the polygon to the polydata
    # cellArray = vtkCellArray()
    #
    # # use vtkContourTriangulator to triangulate the polygon
    # idList = vtkIdList()
    # for i in range(len(points)):
    #     idList.InsertNextId(i)
    #
    # triangulator = vtkContourTriangulator.TriangulatePolygon(idList, vtkPts,cellArray)
    #
    # import matplotlib.pyplot as plt
    #
    # # extract the vertices from cellArray
    # cellArray.InitTraversal()
    # while True:
    #     idList = vtk.vtkIdList()
    #     if cellArray.GetNextCell(idList):
    #         print("Triangle")
    #
    #         corners = []
    #
    #         for i in range(idList.GetNumberOfIds()):
    #
    #             print(vtkPts.GetPoint(idList.GetId(i)))
    #
    #             corners.append(vtkPts.GetPoint(idList.GetId(i)))
    #
    #         corners.append(corners[0])
    #
    #         plt.plot([c[0] for c in corners], [c[1] for c in corners],'r-', lw=4)
    #
    #     else:
    #         break
    #
    # plt.plot([p[0] for p in points], [p[1] for p in points], 'b-')
    #
    # plt.show()

