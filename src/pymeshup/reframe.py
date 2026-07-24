"""Reconstruct a clean hull Volume by lofting *waterlines* (horizontal slices).

Instead of slicing the hull into transverse frames and lofting them along X, we
slice it into horizontal XY waterlines and loft them along Z. A bulbous bow (or a
stern bulb) is simply the forward/aft part of the low waterlines -- continuous
with the hull in every waterline -- so it comes out as one smooth surface with no
special handling, which a frame loft could never manage.

Each waterline is stitched from the (possibly broken) mesh, resampled to a common
number of points, and the rings are lofted and mirrored into a watertight,
port/starboard-symmetric hull. The flat of bottom and the flat of deck are capped
across the beam; the raked stem and stern faces are closed off afterwards.
Symmetry is assumed: only y >= 0 is sliced and the result is mirrored.
"""

import numpy as np

# Use the specific VTK submodules (as done elsewhere in pymeshup) to avoid
# loading optional DLLs that may not be present.
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray, vtkPlane
from vtkmodules.vtkFiltersCore import vtkCutter
from vtkmodules.util.numpy_support import (
    vtk_to_numpy,
    numpy_to_vtk,
    numpy_to_vtkIdTypeArray,
)

# transverse distance below which a section point is treated as being on the
# centerline (y = 0).
CENTERLINE_TOL = 1e-3


def _polydata_from_volume(volume) -> vtkPolyData:
    """Build a vtkPolyData straight from the Volume's internal mesh data."""
    mesh = volume.ms.current_mesh()
    verts = np.asarray(mesh.vertex_matrix(), dtype=np.float64)
    faces = np.asarray(mesh.face_matrix(), dtype=np.int64)

    points = vtkPoints()
    points.SetData(numpy_to_vtk(verts, deep=True))

    # VTK legacy connectivity layout: [3, i, j, k, 3, i, j, k, ...]
    conn = np.empty((len(faces), 4), dtype=np.int64)
    conn[:, 0] = 3
    conn[:, 1:] = faces
    cells = vtkCellArray()
    cells.SetCells(len(faces), numpy_to_vtkIdTypeArray(conn.ravel(), deep=True))

    pd = vtkPolyData()
    pd.SetPoints(points)
    pd.SetPolys(cells)
    return pd


def _slice_z(polydata, z):
    """Cut the mesh with a horizontal plane at height `z`; return the (x, y)
    line segments of the waterline as an (N, 2, 2) array."""
    plane = vtkPlane()
    plane.SetOrigin(0.0, 0.0, z)
    plane.SetNormal(0.0, 0.0, 1.0)
    cutter = vtkCutter()
    cutter.SetCutFunction(plane)
    cutter.SetInputData(polydata)
    cutter.Update()
    cut = cutter.GetOutput()
    if cut.GetNumberOfPoints() == 0:
        return np.empty((0, 2, 2))

    points = vtk_to_numpy(cut.GetPoints().GetData())[:, :2]  # keep (x, y)
    cells = cut.GetLines()
    offsets = vtk_to_numpy(cells.GetOffsetsArray())
    conn = vtk_to_numpy(cells.GetConnectivityArray())
    segments = []
    for start, end in zip(offsets[:-1], offsets[1:]):
        ids = conn[start:end]
        for a, b in zip(ids[:-1], ids[1:]):
            segments.append([points[a], points[b]])
    return np.array(segments)


def _fragments(segments, weld_tol=1e-6):
    """Weld the loose segments and return the waterline's polyline fragments."""
    if len(segments) == 0:
        return []
    pts = segments.reshape(-1, 2)
    quant = np.round(pts / weld_tol).astype(np.int64)
    _, inv = np.unique(quant, axis=0, return_inverse=True)
    unique_pts = np.zeros((inv.max() + 1, 2))
    unique_pts[inv] = pts

    adj = {}
    for a, b in inv.reshape(-1, 2):
        a, b = int(a), int(b)
        if a != b:
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)

    visited = set()
    fragments = []

    def walk(a, b):
        chain = [a, b]
        visited.add(frozenset((a, b)))
        cur = b
        while True:
            nxts = [n for n in adj[cur] if frozenset((cur, n)) not in visited]
            if not nxts:
                break
            nxt = nxts[0]
            visited.add(frozenset((cur, nxt)))
            chain.append(nxt)
            cur = nxt
            if cur == a:
                break
        return chain

    for v in adj:
        if len(adj[v]) == 1:
            for n in adj[v]:
                if frozenset((v, n)) not in visited:
                    fragments.append(walk(v, n))
    for v in adj:
        for n in adj[v]:
            if frozenset((v, n)) not in visited:
                fragments.append(walk(v, n))

    return [np.array([unique_pts[i] for i in c]) for c in fragments if len(c) > 1]


def _waterline(polydata, z):
    """Return the ordered (x, y) waterline curve (aft -> forward) at height `z`,
    stitched from the mesh fragments, or None if the slice is empty."""
    fragments = _fragments(_slice_z(polydata, z))
    if not fragments:
        return None

    chain = [p for p in fragments.pop(0)]
    while fragments:
        head, tail = chain[0], chain[-1]
        best = None  # (distance, index, side, connecting end)
        for k, f in enumerate(fragments):
            for end, pt in ((0, f[0]), (1, f[-1])):
                dh = np.hypot(*(pt - head))
                if best is None or dh < best[0]:
                    best = (dh, k, "head", end)
                dt = np.hypot(*(pt - tail))
                if dt < best[0]:
                    best = (dt, k, "tail", end)
        _, k, side, end = best
        f = fragments.pop(k)
        if side == "tail":
            chain.extend(list(f if end == 0 else f[::-1]))
        else:
            chain = list(f[::-1] if end == 0 else f) + chain

    curve = np.array(chain)
    if curve[0, 0] > curve[-1, 0]:      # orient aft (min x) -> forward (max x)
        curve = curve[::-1]
    return curve


def _resample(curve, n):
    """Resample an open curve to `n` points equally spaced along arc length."""
    d = np.concatenate([[0.0], np.cumsum(np.hypot(np.diff(curve[:, 0]),
                                                  np.diff(curve[:, 1])))])
    if d[-1] == 0:
        return curve
    t = np.linspace(0.0, d[-1], n)
    return np.column_stack([np.interp(t, d, curve[:, 0]),
                            np.interp(t, d, curve[:, 1])])


def reframe(volume, n_waterlines=80, points_per_waterline=140, margin=0.01):
    """Rebuild `volume` as a clean, watertight, symmetric hull by lofting
    horizontal waterlines.

    Args:
        volume: the source Volume (its internal mesh is used as-is).
        n_waterlines: number of horizontal slices from bottom to deck.
        points_per_waterline: points each waterline is resampled to.
        margin: fraction of the height held back from the extremes when slicing
            (a cut exactly on the flat bottom / deck is coincident and empty).

    Returns:
        A new Volume reconstructed from the waterlines.
    """
    from .volumes import Volume  # local import keeps module import lightweight
    from pymeshlab import PercentageValue

    polydata = _polydata_from_volume(volume)
    xmin, xmax, ymin, ymax, zmin, zmax = polydata.GetBounds()
    zheight = zmax - zmin
    beam = max(abs(ymin), abs(ymax))
    snap = 0.005 * beam   # snap near-centerline waterline points onto y = 0
    eps = margin * zheight

    # Place rings across the whole depth (so the flat of bottom sits at the true
    # keel and the flat of deck at the true sheer) but slice a hair inside the
    # extremes to avoid the coincident-plane empty cut.
    rings = []
    for z in np.linspace(zmin, zmax, n_waterlines):
        curve = _waterline(polydata, min(max(z, zmin + eps), zmax - eps))
        if curve is None or len(curve) <= 1:
            continue
        ring = _resample(curve, points_per_waterline)
        ring[np.abs(ring[:, 1]) < snap, 1] = 0.0
        rings.append((z, ring))

    if len(rings) < 2:
        raise ValueError("Could not extract enough waterlines to build a hull")

    m = points_per_waterline
    vertices = [(x, y, z) for z, ring in rings for x, y in ring]
    n_star = len(vertices)
    vertices += [(x, -y, z) for z, ring in rings for x, y in ring]

    def star(k, i):
        return k * m + i

    def port(k, i):
        return n_star + k * m + i

    faces = []
    # side wall: loft consecutive waterlines (starboard + mirrored port)
    for k in range(len(rings) - 1):
        for i in range(m - 1):
            a, b, c, d = star(k, i), star(k, i + 1), star(k + 1, i + 1), star(k + 1, i)
            faces += [(a, b, c), (a, c, d)]
            a, b, c, d = port(k, i), port(k, i + 1), port(k + 1, i + 1), port(k + 1, i)
            faces += [(a, c, b), (a, d, c)]

    # flat of bottom and flat of deck: cap the lowest and highest rings across
    # the beam (the raked/flared ends are closed by meshing_close_holes below)
    for k, flip in ((0, False), (len(rings) - 1, True)):
        for i in range(m - 1):
            a, b = star(k, i), star(k, i + 1)
            c, d = port(k, i), port(k, i + 1)
            faces += [(a, b, d), (a, d, c)] if flip else [(a, d, b), (a, c, d)]

    out = Volume()
    out.set_vertices_and_faces(np.array(vertices, dtype=float),
                               np.array(faces, dtype=int))
    out.ms.meshing_remove_duplicate_vertices()
    out.ms.meshing_remove_null_faces()
    out.ms.meshing_merge_close_vertices(threshold=PercentageValue(0.1))
    for _ in range(3):  # close the raked stem / stern faces (iterate to finish)
        out.ms.meshing_close_holes(maxholesize=100000)
        if out.ms.get_topological_measures().get("boundary_edges") == 0:
            break
    out.ms.meshing_re_orient_faces_coherently()
    if out.volume < 0:
        out = out.invert_normals()
    return out
