from pymeshup.hull import build_triangles
import matplotlib.pyplot as plt

if __name__ == '__main__':
    v1 = [(0, 5.7579768, 0.2801112),
         (0, 6.2941199999999995, 0.2801112),
         (0, 5.7579768, 0.2801112)]

    v2 = [(5, 5.7171336, 0.0),
         (5, 6.3349632, 0.0),
         (5, 6.3349632, 0.3941064),
         (5, 5.7171336, 0.3941064),
         (5, 5.7171336, 0.0)]

    # # use matplotlib to plot the points in 3d space
    # fig = plt.figure()
    # ax = fig.add_subplot(111, projection='3d')
    # ax.scatter([v[1] for v in v1], [v[2] for v in v1], [v[0] for v in v1], c='r', marker='o')
    # ax.scatter([v[1] for v in v2], [v[2] for v in v2], [v[0] for v in v2], c='b', marker='o')
    #
    # # plot the indices as text
    # for i, txt in enumerate(v1):
    #     ax.text(txt[1], txt[2], txt[0], str(i))
    #
    # for i, txt in enumerate(v2):
    #     ax.text(txt[1], txt[2], txt[0], str(i))
    #
    # plt.show()

    verts, face_ids = build_triangles(v1,v2)



