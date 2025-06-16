import numpy as np
import csv

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

    segments = list()

    while True:

        # current points on frame1 and frame2
        p1 = f1[i1]
        p2 = f2[i2]

        if i1==n1-1:
            i2+=1
        elif i2==n2-1:
            i1+=1
                # finish the halfs simultaneously
        else:

            # possible next points on 1 and 2
            a1 = f1[i1+1]  # advance
            a2 = f2[i2+1]

            # are we crossing the center-line on either of them?
            crossed1 = (a1[1] * p1[1] <= 0 and i1 > 0) or crossed1
            crossed2 = (a2[1] * p2[1] <= 0 and i2 > 0) or crossed2

            if crossed1 and not crossed2:
                i2 += 1
            elif crossed2 and not crossed1:
                i1 += 1
            else:

                # if one of the lines has only three vertices, and both frames are still at index 0,
                # the advance on the one with the most vertices

                if i1==0 and i2==0 and (n1==3 or n2==3):
                    if n1 > n2:
                        i1 += 1
                    else:
                        i2 += 1

                else:

                    # should we advance on 1 or on 2?
                    #
                    # advance in frame 1 --> a1, p2
                    # advance on frame 2 --> p1, a2
                    # select the new line based on the shortest distance

                    l1 = np.linalg.norm(np.array(a1) - p2)  # advance on 1, stay on 2
                    l2 = np.linalg.norm(np.array(a2) - p1)  # keep point on 1, advance on 2

                    if l1==l2:
                        # print('equal')
                        # advance the one with the lowest relative index
                        if (i1/n1 < i2/n2):
                            i1 += 1
                        else:
                            i2 += 1


                    elif l1 > l2:
                        i2 += 1
                    else:
                        i1 += 1

        # print('connecting {} and {}'.format(i1,i2))

        segments.append((f1[i1], f2[i2]))

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
    while i < len(frames)-2:
        # frame i is redundant it is identical to frame i-1 and i+1

        if frames[i].is_identical_to(frames[i-1]) and frames[i].is_identical_to(frames[i+1]):
            frames.pop(i)
            x.pop(i)
        else:
            i += 1


    # print("---------------")

    # mesh (frame0)

    verts, face_ids = frames[0].to_plane_at(x[0])
    vertices.extend(verts)
    faces.extend(face_ids)

    for i in range(len(frames)-1):

        f1 = frames[i]
        f2 = frames[i+1]

        vertices1 = f1.as_vertices_at(x[i])
        vertices2 = f2.as_vertices_at(x[i+1])

        # print(f"Building triangles between {len(vertices1)} and {len(vertices2)} vertices")
        verts, face_ids = build_triangles(vertices1,vertices2)

        # correct face_ids for t
        nva = len(vertices)
        faces_corrected = [(a[0]+nva, a[1]+nva, a[2]+nva) for a in face_ids]

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

    try:
        volume = v.volume
    except ValueError:

        print("Volume not available, we do have the following mesh data")
        #
        # from pymeshup import Plot
        # Plot(v)
        return v

    if v.volume < 0:
        v = v.invert_normals()

    return v

def hull_from_file(filename) -> Volume:
    """Reads a hull from a file:

    framex   frame_data_y
    <empty>  frame_data_z
    """


    with open(filename, 'r') as f:
        first_line = f.readline()
        if '\t' in first_line:
            delimiter = '\t'
        else:
            delimiter = ','
        f.seek(0)

        reader = csv.reader(f, delimiter=delimiter)
        data = [row for row in reader]

    # print(data)

    # remove empties
    new_data = []
    for row in data:
        new_row = [item for item in row if item != '']
        new_data.append(new_row)

    # print(new_data)

    # Construct frames

    frames = []
    positions = []

    while new_data:
        row1 = new_data.pop(0)
        row2 = new_data.pop(0)

        assert len(row1) == len(row2) + 1, f"Row {row1} has {len(row1)} elements, row {row2} has {len(row2)} elements"

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

