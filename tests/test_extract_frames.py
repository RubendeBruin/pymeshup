# Read the following stl file.
# This is a typical example of a bad vessel hull shape mesh.
#
# Volume.reframe() re-slices the mesh into transverse frames, cleans each
# frame up (orders the points along the shortest path and removes redundant
# vertices in straight segments) and lofts the frames back into a clean,
# watertight hull Volume using the Hull class.
#
# This POC loads the bad mesh and rebuilds it with reframe(), then shows the
# result with matplotlib.

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from pymeshup import Load, Plot

if __name__ == '__main__':
    filename = r"C:\dev\pymeshup\tests\assets_for_tests\3dpea.com_kvlcc2.stl"

    bad_hull = Load(filename).rotate(x=-90).rotate(z=180)
    # Plot(bad_hull)
    # exit(0)

    # Re-slice the bad mesh into frames and loft them into a clean hull.
    hull = bad_hull.reframe(n_frames=100)

    print(f"Hull volume : {hull.volume:,.1f}")
    print(f"Hull bounds : {hull.bounds}")

    # Plot(hull)

    # --- Show the reconstructed hull from three angles ---------------------
    verts = hull.ms.current_mesh().vertex_matrix()
    faces = hull.ms.current_mesh().face_matrix()

    fig = plt.figure(figsize=(15, 5))
    for k, (title, (elev, azim)) in enumerate(
        [("iso", (20, -60)), ("top", (90, -90)), ("front", (0, -90))]
    ):
        ax = fig.add_subplot(1, 3, k + 1, projection='3d')
        ax.add_collection3d(Poly3DCollection(
            verts[faces], facecolor='lightsteelblue', edgecolor='k', linewidth=0.15
        ))
        ax.set_xlim(verts[:, 0].min(), verts[:, 0].max())
        ax.set_ylim(verts[:, 1].min(), verts[:, 1].max())
        ax.set_zlim(verts[:, 2].min(), verts[:, 2].max())
        ax.set_box_aspect((6, 2, 2))
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(title)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

    fig.suptitle(f"reframe() reconstructed hull  |  volume = {hull.volume:,.0f}")
    plt.tight_layout()
    plt.show()
