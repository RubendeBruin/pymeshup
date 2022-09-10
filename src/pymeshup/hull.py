import numpy as np

from .frames import Frame
from .volumes import Volume


def build_triangles(f1,f2):
    """
    Builds triangles between two lists of points

    Args:
        f1: list of [x,y,z]
        f2: lift of [x,y,z]

    Returns:
        points : list of [x,y,z] containing vertices
        triangles : list of [i,j,k] with the indices

    """

    # i = counter
    # n = amount
    # p1 = point on list 1
    # p2 = point on list 2

    i1 = 0
    i2 = 0
    # p1 = f1[i1]
    # p2 = f2[i2]

    n1 = len(f1)
    n2 = len(f2)

    o1 = 0   # previous indices
    o2 = 0

    crossed1 = False
    crossed2 = False


    triangles = list()

    while True:

        if i1==3:
            print('wait')

        p1 = f1[i1]
        p2 = f2[i2]

        if i1==n1-1:
            i2+=1
        elif i2==n2-1:
            i1+=1
                # finish the halfs simultaneously
        else:

            a1 = f1[i1+1]  # advance
            a2 = f2[i2+1]

            # are we crossing the center-line on either of them?
            crossed1 = a1[1] * p1[1] <= 0 or crossed1
            crossed2 = a2[1] * p2[1] <= 0 or crossed2

            if crossed1 and not crossed2:
                i2 += 1
            elif crossed2 and not crossed1:
                i1 += 1
            else:

                l1 = np.linalg.norm(np.array(a1) - p2)  # Line to next point on frame 1
                l2 = np.linalg.norm(np.array(a2) - p1)

                if l1 > l2:
                    i2 += 1
                else:
                    i1 += 1

        # we now have point i1 and i2
        if i1==o1:
            # triangle between i1, i2 and o2
            triangles.append((i1,o2+n1, i2+n1))
        else:
            triangles.append((o1, i2+n1, i1))

        o1 = i1
        o2 = i2

        if i1==n1-1 and i2==n2-1:
            break

    return [*f1,*f2], triangles


def Hull(*args):
    """Arguments: pos, Frame, pos, Frame, etc
    example: h = Hull(0,stern, 10, midship, 20, midship, 30, bow)"""

    if len(args) % 2 != 0:
        raise ValueError("Number of arguments should be even")

    n = len(args) // 2

    last_x = -1e20
    x = []
    frames = []

    for i in range(n):
        xx = args[2*i]

        if not isinstance(xx, (float, int)):
            raise ValueError(f"Only numeric entries are accepted for Frame positions, {xx} is not nummeric")

        if xx < last_x:
            raise ValueError(f"Frame positions should be increasing, {xx} is not larger than {last_x}")
        last_x = xx

        f = args[2*i+1]

        if not isinstance(f, Frame):
            raise ValueError(f"Only Frame entries are accepted for frames, {f} is not a Frame object")

        frames.append(f)
        x.append(xx)

    # add one-frames at start and end, if needed
    if frames[0].n > 1:
        stern = Frame(*frames[0].center())
        frames.insert(0,stern)
        x.insert(0, x[0])

    if frames[-1].n > 1:
        bow = Frame(*frames[-1].center())
        frames.append(bow)
        x.append(x[-1])

    vertices = []
    faces = []


    for i in range(len(frames)-1):

        f1 = frames[i]
        f2 = frames[i+1]

        vertices1 = f1.as_vertices_at(x[i])
        vertices2 = f2.as_vertices_at(x[i+1])

        verts, face_ids = build_triangles(vertices1,vertices2)

        # correct face_ids for t
        nva = len(vertices)
        faces_corrected = [(a[0]+nva, a[1]+nva, a[2]+nva) for a in face_ids]

        vertices.extend(verts)
        faces.extend(faces_corrected)

    v = Volume()
    v.set_vertices_and_faces(vertices, faces)

    return v


