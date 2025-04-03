import warnings

from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator

from pymeshup.helpers.earcut_2d import triangulate_poly_py

def triangulate_poly(vertices):
    try:
        return triangulate_poly_vtk(vertices)
    except ValueError:
        return triangulate_poly_py(vertices)


def triangulate_poly_vtk(vertices):
    """Triangulates a polygon defined by vertices. Polygons can be concave

    Returns

    """
    out_faces = []

    out_points = list(vertices)

       # make a vtk polydata object from these points
    vtkPts = vtkPoints()
    for p in out_points:
        vtkPts.InsertNextPoint(*p)

     # add the polygon to the polydata
    cellArray = vtkCellArray()

    # use vtkContourTriangulator to triangulate the polygon
    idList = vtkIdList()
    for i in range(len(vertices)):
        idList.InsertNextId(i)

    result = vtkContourTriangulator.TriangulatePolygon(idList, vtkPts,cellArray)

    if result != 1:
        raise ValueError("Triangulation failed")


    # extract the vertices from cellArray
    cellArray.InitTraversal()

    while True:
        idList = vtkIdList()
        if cellArray.GetNextCell(idList):
            corners = []

            for i in range(idList.GetNumberOfIds()):
                # corners.append(vtkPts.GetPoint(idList.GetId(i)))
                corners.append(idList.GetId(i))

            out_faces.append(corners)
        else:
            break

    return out_points, out_faces


if __name__ == '__main__':
    verts = [(0, 0, 0), (0, 0.1, 0), (0, 0.1, 0), (0, 1, 0), (0, 1, 0), (0, -1, 0), (0, -1, 0), (0, -0.1, 0), (0, -0.1, 0),
     (0, 0, 0)]

    verts, faces = triangulate_poly(verts)

    import matplotlib.pyplot as plt

    for tri in faces:
        # get vertices
        t = [verts[i] for i in tri]
        t.append(t[0])

        plt.plot([p[0] for p in t], [p[1] for p in t], 'r-')

    plt.show()
