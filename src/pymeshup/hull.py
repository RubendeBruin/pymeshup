import numpy as np
import csv

from .frames import Frame
from .volumes import Volume

import logging
logger = logging.getLogger(__name__)


def build_triangles(f1, f2):
    """
    Builds triangles between two lists of points.

    There is some magic involved:
    - the fist edge is created between the first vertices
    -


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

    o1 = 0  # previous indices
    o2 = 0

    triangles = list()
    segments = list()

    while True:
        # current points on frame1 and frame2
        p1 = f1[i1]
        p2 = f2[i2]

        # frame2 needs to catch up in the following cases
        # 1. frame1 has reached the end
        # 2. frame1 have just crosses the y=0 line and frame1 is still on the other side

        catchup1 = False
        catchup2 = False

        frame1_crossed = i1>1 and p1[1] * f1[i1-1][1] < 0
        frame2_crossed = i2>1 and p2[1] * f2[i2-1][1] < 0
        on_same_side = p1[1] * p2[1] >= 0

        frame1_reached_end = i1 == n1 - 1
        frame2_reached_end = i2 == n2 - 1

        if frame1_reached_end:
            catchup2 = True
        elif frame1_crossed and not on_same_side:
            catchup2 = True

        if frame2_reached_end:
            catchup1 = True
        elif frame2_crossed and not on_same_side:
            catchup1 = True

        # can not catch-up if we have reached the end
        if frame1_reached_end:
            catchup1 = False
        if frame2_reached_end:
            catchup2 = False


        if catchup1 or catchup2:
            logger.debug(f"i1: {i1}, i2: {i1}")
            logger.debug(f"same side {on_same_side}")
            logger.debug(f"reached end : {frame1_reached_end}, {frame2_reached_end}")
            logger.debug(f"crossed : {frame1_crossed}, {frame2_crossed}")
            logger.debug(f"catchup : {catchup1}, catchup2 : {catchup2}")

        if catchup1:
            i1 += 1
        elif catchup2:
            i2 += 1
        else:

            # possible next points on 1 and 2
            a1 = f1[i1 + 1]  # advance
            a2 = f2[i2 + 1]

            # # if one of the lines has only three vertices, and both frames are still at index 0,
            # # the advance on the one with the most vertices
            #
            # if i1 == 0 and i2 == 0 and (n1 == 3 or n2 == 3):
            #     if n1 > n2:
            #         i1 += 1
            #     else:
            #         i2 += 1

            # else:
            # should we advance on 1 or on 2?
            #
            # advance in frame 1 --> a1, p2
            # advance on frame 2 --> p1, a2
            # select the new line based on the shortest distance

            l1 = np.linalg.norm(np.array(a1) - p2)  # advance on 1, stay on 2
            l2 = np.linalg.norm(
                np.array(a2) - p1
            )  # keep point on 1, advance on 2

            if l1 == l2:
                # print('equal')
                # advance the one with the lowest relative index
                if i1 / n1 < i2 / n2:
                    i1 += 1
                else:
                    i2 += 1

            elif l1 > l2:
                i2 += 1
            else:
                i1 += 1

        segments.append((f1[i1], f2[i2]))

        # we now have point i1 and i2
        if i1 == o1:
            # triangle between i1, i2 and o2
            triangles.append((i1, o2 + n1, i2 + n1))
        else:
            triangles.append((o1, i2 + n1, i1))

        o1 = i1
        o2 = i2

        if i1 == n1 - 1 and i2 == n2 - 1:
            break

    return [*f1, *f2], triangles


def Hull(*args):
    """Arguments: pos, Frame, pos, Frame, etc
    example: h = Hull(0,stern, 10, midship, 20, midship, 30, bow)

    OR a filename
    """

    if len(args) == 1:
        filename = args[0]
        return hull_from_file(filename)

    if len(args) % 2 != 0:
        raise ValueError("Number of arguments should be even")

    n = len(args) // 2

    last_x = -1e20
    x = []
    frames = []

    for i in range(n):
        xx = args[2 * i]

        if not isinstance(xx, (float, int)):
            raise ValueError(
                f"Only numeric entries are accepted for Frame positions, {xx} is not nummeric"
            )

        if xx < last_x:
            raise ValueError(
                f"Frame positions should be increasing, {xx} is not larger than {last_x}"
            )
        last_x = xx

        f = args[2 * i + 1]

        if not isinstance(f, Frame):
            raise ValueError(
                f"Only Frame entries are accepted for frames, {f} is not a Frame object"
            )

        frames.append(f)
        x.append(xx)

    # # add one-frames at start and end, if needed
    # # The frames are always closed
    # # n is the number of vertices, where the first is identical to the last
    # # so n=3 means two unique vertices --> a line
    # if frames[0].n > 3:
    #     stern = Frame(*frames[0].center())
    #     frames.insert(0,stern)
    #     x.insert(0, x[0])
    #
    # if frames[-1].n > 3:
    #     bow = Frame(*frames[-1].center())
    #     frames.append(bow)
    #     x.append(x[-1])

    vertices = []
    faces = []

    # remove redundant intermediate frames
    i = 1
    while i < len(frames) - 2:
        # frame i is redundant it is identical to frame i-1 and i+1

        if frames[i].is_identical_to(frames[i - 1]) and frames[i].is_identical_to(
            frames[i + 1]
        ):
            frames.pop(i)
            x.pop(i)
        else:
            i += 1

    # print("---------------")

    # mesh (frame0)

    verts, face_ids = frames[0].to_plane_at(x[0])
    vertices.extend(verts)
    faces.extend(face_ids)

    for i in range(len(frames) - 1):
        f1 = frames[i]
        f2 = frames[i + 1]

        vertices1 = f1.as_vertices_at(x[i])
        vertices2 = f2.as_vertices_at(x[i + 1])

        # print(f"Building triangles between {len(vertices1)} and {len(vertices2)} vertices")
        verts, face_ids = build_triangles(vertices1, vertices2)

        # correct face_ids for t
        nva = len(vertices)
        faces_corrected = [(a[0] + nva, a[1] + nva, a[2] + nva) for a in face_ids]

        vertices.extend(verts)
        faces.extend(faces_corrected)

    # mesh last frame
    verts, face_ids = frames[-1].to_plane_at(x[-1], invert_normal=True)

    nva = len(vertices)
    faces_corrected = [(a[0] + nva, a[1] + nva, a[2] + nva) for a in face_ids]
    faces.extend(faces_corrected)

    vertices.extend(verts)

    v = Volume()
    v.set_vertices_and_faces(vertices, faces)
    v.ms.meshing_remove_duplicate_vertices()

    # check if we can get the volume of this hull, if not then debug
    try:
        _volume = v.volume
    except ValueError:
        print("Volume not available, we do have the following mesh data")
        return v

    if v.volume < 0:
        v = v.invert_normals()

    return v


def hull_from_file(filename) -> Volume:
    """Reads a hull from a file:

    framex   frame_data_y
    <empty>  frame_data_z
    """

    with open(filename, "r") as f:
        first_line = f.readline()
        if "\t" in first_line:
            delimiter = "\t"
        else:
            delimiter = ","
        f.seek(0)

        reader = csv.reader(f, delimiter=delimiter)
        data = [row for row in reader]

    # print(data)

    # remove empties
    new_data = []
    for row in data:
        new_row = [item for item in row if item != ""]
        new_data.append(new_row)

    # print(new_data)

    # Construct frames

    frames = []
    positions = []

    while new_data:
        row1 = new_data.pop(0)
        row2 = new_data.pop(0)

        assert (
            len(row1) == len(row2) + 1
        ), f"Row {row1} has {len(row1)} elements, row {row2} has {len(row2)} elements"

        x = float(row1[0])
        y = [float(item) for item in row1[1:]]
        z = [float(item) for item in row2]

        positions.append(x)

        frame_data = []
        for yy, zz in zip(y, z):
            frame_data.extend([yy, zz])

        frames.append(Frame(*frame_data).autocomplete())

    hull_data = []
    for frame, position in zip(frames, positions):
        hull_data.extend([position, frame])

    return Hull(*hull_data)

def debug_plot_frame_connection(f1 : Frame, f2: Frame, dx=10):
    """Uses matplotlib to plot the faces created between two frames """
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    vertices1 = f1.as_vertices_at(0)
    vertices2 = f2.as_vertices_at(dx)

    verts, face_ids = build_triangles(vertices1, vertices2)

    # --- 3D plot ---
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Build triangle polygons for Poly3DCollection
    tris = [[verts[i] for i in face] for face in face_ids]
    poly = Poly3DCollection(tris, alpha=0.5, facecolor='steelblue', edgecolor='k', linewidth=0.3)
    ax.add_collection3d(poly)

    # Scatter the vertices
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    ax.scatter(xs, ys, zs, color='red', s=10, zorder=5)

    # Label each vertex with its index within its original frame
    n1 = len(vertices1)
    for idx, (x, y, z) in enumerate(verts):
        frame_idx = idx if idx < n1 else idx - n1
        label = f"{frame_idx}"
        ax.text(x, y, z, label, fontsize=8, color='navy' if idx < n1 else 'darkgreen')

    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ax.set_zlim(min(zs), max(zs))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Vertices and Faces')

    plt.tight_layout()
    plt.show()