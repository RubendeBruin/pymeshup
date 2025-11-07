import numpy as np

def is_clockwise(polygon):
    """Determine if the polygon is ordered clockwise."""
    area = 0
    n = len(polygon)
    for i in range(n):
        x_i, y_i = polygon[i]
        x_j, y_j = polygon[(i + 1) % n]
        area += (x_i * y_j) - (x_j * y_i)
    return area < 0


def is_point_inside_triangle(p, a, b, c):
    """Check if point p is inside the triangle formed by a, b, c."""

    def same_side(p1, p2, a, b):
        cp1 = (b[0] - a[0]) * (p1[1] - a[1]) - (b[1] - a[1]) * (p1[0] - a[0])
        cp2 = (b[0] - a[0]) * (p2[1] - a[1]) - (b[1] - a[1]) * (p2[0] - a[0])
        return (cp1 * cp2) >= 0

    return (same_side(p, c, a, b) and
            same_side(p, a, b, c) and
            same_side(p, b, c, a))


def triangulate_ear_clipping_2d(polygon):
    """Triangulate a 2D polygon using the ear-clipping algorithm."""

     # make a copy to not modify the original
    polygon = [tuple(vertex) for vertex in polygon]  # Ensure vertices are tuples and not a copy

    indices = [i for i in range(len(polygon))]

    triangles = []
    i_triangles = []
    orientation = not is_clockwise(polygon)

    while len(polygon) > 3:
        ear_clipped = False
        for i in range(len(polygon)):
            prev_idx = (i - 1) % len(polygon)
            next_idx = (i + 1) % len(polygon)
            prev = polygon[prev_idx]
            current = polygon[i]
            next_vrtx = polygon[next_idx]

            # Calculate cross product to determine convexity
            vec_prev = (current[0] - prev[0], current[1] - prev[1])
            vec_next = (next_vrtx[0] - current[0], next_vrtx[1] - current[1])
            cross = vec_prev[0] * vec_next[1] - vec_prev[1] * vec_next[0]

            # Determine if the vertex is convex
            if (orientation and cross < 0) or (not orientation and cross > 0):
                continue  # Reflex vertex, skip

            # Check if current vertex is an ear
            is_ear = True
            triangle = [prev, current, next_vrtx]
            for v in polygon:
                if v in triangle:
                    continue
                if is_point_inside_triangle(v, prev, current, next_vrtx):
                    is_ear = False
                    break
            if is_ear:
                triangles.append(triangle)

                i_triangles.append((indices[prev_idx],
                                    indices[i],
                                    indices[next_idx]))

                del polygon[i]
                del indices[i]
                ear_clipped = True
                break  # Move to next iteration of the while loop
        if not ear_clipped:
            raise ValueError("No ear found. Ensure the polygon is simple and non-intersecting.")

    # Add the remaining triangle
    if len(polygon) == 3:
        triangles.append(polygon)
        i_triangles.append((indices[0], indices[1], indices[2]))

    return i_triangles

def find_plane(vertices : np.array):
    """Find a suitable normal to the shape defined by the vertices.

    Args:
        vertices (list): List of vertices defining the shape.

    Returns:
        tuple: Normal vector.
    """

    result = None
    best_normal_length = 0

    for i in range(len(vertices)-2):
        v1 = vertices[i+1] - vertices[i]
        v2 = vertices[i+2] - vertices[i]

        normal = np.cross(v1, v2)

        if np.linalg.norm(normal) > 1:
            result =  normal
            break

        if np.linalg.norm(normal) > best_normal_length:
            best_normal_length = np.linalg.norm(normal)
            result = normal

    # normalize the normal vector
    normal = result / np.linalg.norm(result)

    # construct ux and uy from normal
    # try to use the x-axis as ux
    ux0 = np.array([1, 0, 0])

    # check if ux0 is parallel to normal
    if np.linalg.norm(np.cross(normal, ux0) ) < 1e-6:
        # use y-axis as ux
        ux0 = np.array([0, 1, 0])

    ux = ux0 - np.dot(ux0, normal) * normal # make perpendicular to normal
    ux = ux / np.linalg.norm(ux)

    # construct uy from ux and normal
    uy = np.cross(normal, ux)

    return ux, uy

def triangulate_poly_py(vertices_in):
    """Triangulate a polygon defined by vertices. Polygons can be concave

    Returns
    """

    # check if the polygon is simple and non-intersecting
    if len(vertices_in) < 3:
        raise ValueError("Polygon must have at least 3 vertices")

    # make a copy of the vertices
    vertices = np.array(vertices_in)

    first_repeated = np.allclose(vertices[0], vertices[-1], atol=1e-6)

    if first_repeated:
        vertices = vertices[:-1]

    # find a suitable normal to the shape
    ux, uy = find_plane(vertices)

    # # project the vertices to the plane
    projected = []
    for v in vertices:
        # project the vertex to the plane defined by ux and uy
        projected.append((np.dot(v, ux), np.dot(v, uy)))

    i_triangles = triangulate_ear_clipping_2d(projected)

    return vertices_in, i_triangles



if __name__ == '__main__':

    vertices = [(-60, 0 , 0),
                (-60, -2.5, 0.0),
                (-60, -2.5, 4.0),
                (-60, 0.0, 4.0),
                (-61, 1, 5.0),
                (-60, 2.5, 0.0),
                (-60, 0.0, 0.0)]

    verts, faces = triangulate_poly_py(vertices)

    print("Vertices:", verts)
    print("Faces:", faces)

    # Visualization (optional) in 3d
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 8))

    # Plot the original polygon
    x = [v[0] for v in verts]
    y = [v[1] for v in verts]
    z = [v[2] for v in verts]

    ax = plt.axes(projection='3d')
    ax.plot(x + [x[0]], y + [y[0]], z + [z[0]], 'k-')

    # Plot the triangles
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    from matplotlib import cm

    for i,tri in enumerate(faces):
        t = [verts[i] for i in tri]
        t.append(t[0])
        ax.plot([p[0] for p in t], [p[1] for p in t], [p[2] for p in t], 'r--')

        # fill the 3d polygon with a color
        poly3d = [[verts[i] for i in tri]]

        ax.add_collection3d(Poly3DCollection(poly3d, alpha=0.5, color=cm.tab20(i)))


    plt.show()





