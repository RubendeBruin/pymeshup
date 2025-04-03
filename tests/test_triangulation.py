from pymeshup.helpers.triangulate_non_convex import triangulate_poly


def test_triangulation():
    """Test the triangulation function with the given vertices."""
    vertices = [(-60, 0.0, 0.0),
                (-60, -2.5, 0.0),
                (-60, -2.5, 4.0),
                (-60, 0.0, 4.0),
                (-60, 2.5, 4.0),
                (-60, 2.5, 0.0),
                (-60, 0.0, 0.0)]

    verts, faces = triangulate_poly(vertices)

    print("Vertices:", verts)
    print("Faces:", faces)

    # Visualization (optional)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 8))

    # Plot the original polygon
    x = [v[1] for v in verts]
    y = [v[2] for v in verts]
    plt.plot(x + [x[0]], y + [y[0]], 'k-')

    # Plot the triangles
    for tri in faces:
        t = [verts[i] for i in tri]
        t.append(t[0])
        plt.plot([p[1] for p in t], [p[2] for p in t], 'r--')

    plt.axis('equal')
    plt.title("Triangulation Result")
    plt.xlabel("Y")
    plt.ylabel("Z")
    plt.grid(True)
    plt.show()


def test_triangulation2():
    """Test the triangulation function with the given vertices."""
    vertices = [(-60, 0.0, 0.0),
                (-60, -2.5, 0.0),
                (-61, -2.5, 4.0),
                (-60, 0.0, 4.0),
                (-60, 2.5, 4.0),
                (-60, 2.5, 0.0),
                (-60, 0.0, 0.0)]

    verts, faces = triangulate_poly(vertices)

    print("Vertices:", verts)
    print("Faces:", faces)

    # Visualization (optional)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 8))

    # Plot the original polygon
    x = [v[1] for v in verts]
    y = [v[2] for v in verts]
    plt.plot(x + [x[0]], y + [y[0]], 'k-')

    # Plot the triangles
    for tri in faces:
        t = [verts[i] for i in tri]
        t.append(t[0])
        plt.plot([p[1] for p in t], [p[2] for p in t], 'r--')

    plt.axis('equal')
    plt.title("Triangulation Result")
    plt.xlabel("Y")
    plt.ylabel("Z")
    plt.grid(True)
    plt.show()

def test_earclip_loop():
    vertices = [(-60.999989760000005, 0.0, 0.0), (-60.999989760000005, 2.50000008, 0.0),
     (-60.999989760000005, 2.50000008, 4.000012320000001), (-60.999989760000005, 0.0, 4.000012320000001),
     (-60.999989760000005, -2.50000008, 4.000012320000001), (-60.999989760000005, -2.50000008, 0.0),
     (-60.999989760000005, 0.0, 0.0)]

    verts, faces = triangulate_poly(vertices)


if __name__ == "__main__":
    test_earclip_loop()