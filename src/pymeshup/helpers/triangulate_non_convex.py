import warnings

from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray
from vtkmodules.vtkFiltersGeneral import vtkContourTriangulator


def triangulate_poly(vertices):
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


        # import matplotlib.pyplot as plt
        #
        # # plot in 3d
        # fig = plt.figure()
        # ax = fig.add_subplot(111, projection='3d')
        #
        # for i,p in enumerate(out_points):
        #     ax.scatter(*p)
        #
        #     # add label with number
        #     ax.text(*p, s=str(i))
        #
        # plt.title("Triangulation of the following points failed")
        # plt.show()


        warnings.warn("Triangulation failed, trying to re-order the points - SOME GEOMETRY MAY BE MISSING")

        # re-order the points to make the triangulation work and try again
        # do this by making a convex hull of the points

        from scipy.spatial import ConvexHull
        import numpy as np

        # check all points have the same x-coordinate
        unique_x = set([p[0] for p in out_points])
        assert len(unique_x) == 1

        unique_x = unique_x.pop()

        # points 2d for convex hull
        points_2d = [(p[1], p[2]) for p in out_points]

        hull = ConvexHull(np.array(points_2d))

        # get the vertices of the convex hull
        hull_points = [out_points[i] for i in hull.vertices]

        # add the first point to the end to close the hull
        hull_points.append(hull_points[0])

        # try again
        return triangulate_poly(hull_points)



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
