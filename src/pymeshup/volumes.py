import tempfile

import pymeshlab
from math import sqrt, cos, sin, pi
from numpy import min, max
from pathlib import Path

from vtkmodules.vtkIOGeometry import vtkSTLWriter


class Volume():

    def __init__(self, volume : "Volume" or None = None):
        self.ms = pymeshlab.MeshSet()

        if volume:
            self.ms.add_mesh(mesh = volume.ms.current_mesh())

    def set_vertices_and_faces(self, vertices, faces):
        """Sets the current mesh from vertices and faces"""

        mesh = pymeshlab.Mesh(vertices, faces)
        self.ms.add_mesh(mesh)

    def move(self,x=0, y=0, z=0):
        """Returns a translated copy of the volume"""

        v = Volume(self)
        v.ms.compute_matrix_from_translation_rotation_scale(translationx = x, translationy = y, translationz = z)
        return v

    def scale(self, x=1, y=1 , z=1):
        """Returns a scaled copy of the volume"""
        v = Volume(self)
        v.ms.compute_matrix_from_translation_rotation_scale(scalex=x, scaley=y, scalez=z)
        return v

    def mirrorXZ(self):
        """Returns a mirrored copy of the volume, mirrored in the XZ plane"""
        v = self.scale(y=-1).invert_normals()
        return v



    def rotate(self, x=0, y=0 , z=0):
        """Returns a rotated copy of the volume, rotation in degrees; Euler angles"""
        v = Volume(self)
        v.ms.compute_matrix_from_translation_rotation_scale(rotationx=x, rotationy=y, rotationz=z)
        return v

    def add(self, other):
        """Returns a copy with other added to the volume"""

        # if current mesh is empty, then return copy of other
        if self.ms.mesh_number() == 0:
            return Volume(other)

        v = Volume(self)
        v.ms.add_mesh(other.ms.current_mesh())


        # v.ms.mesh_boolean_union()
        v.ms.generate_boolean_union()

        return v

    def remove(self, other):
        """Returns a copy with other subtracted from the volume"""
        v = Volume(other)
        v.ms.add_mesh(self.ms.current_mesh())
        v.ms.generate_boolean_difference()

        return v

    def inside_of(self, other):
        """Returns the intersection (common part) with other volume"""
        v = Volume(self)
        v.ms.add_mesh(other.ms.current_mesh())

        v.ms.generate_boolean_intersection()
        # v.ms.mesh_boolean_intersection()

        return v

    def invert_normals(self):
        v = Volume(self)
        v.ms.meshing_invert_face_orientation()
        return v


    @property
    def vertices(self):
        return self.ms.current_mesh().vertex_matrix()

    @property
    def bounds(self):
        """minx, maxx, miny, maxy, minz, maxz"""
        bb = self.ms.get_geometric_measures()['bbox']
        mins = bb.min()
        maxs = bb.max()

        return mins[0], maxs[0], mins[1], maxs[1], mins[2], maxs[2]

    @property
    def volume(self):
        data = self.ms.get_geometric_measures()
        if 'mesh_volume' in data:
            return data['mesh_volume']
        else:
            raise ValueError(f"Volume not available, we do have the following mesh data {data}")


    @property
    def center(self):
        return self.ms.get_geometric_measures()['center_of_mass']

    def crop(self,xmin = None, xmax = None, ymin = None, ymax = None, zmin = None, zmax = None):
        """Returns a cropped copy"""

        x = self.vertices[:,0]
        y = self.vertices[:, 1]
        z = self.vertices[:, 2]

        if xmin is None:
            xmin = min(x)-1
        if xmax is None:
            xmax = max(x)+1

        if ymin is None:
            ymin = min(y)-1
        if ymax is None:
            ymax = max(y)+1

        if zmin is None:
            zmin = min(z)-1
        if zmax is None:
            zmax = max(z) +1

        b = Box(xmin, xmax, ymin, ymax, zmin, zmax)

        return self.inside_of(b)

    def cut_at_waterline(self):
        """Cut and keep submerged parts only"""
        return self.cut_plane(planeaxis='Z Axis')

    def cut_at_xz(self):
        """Cuts at the xz plane, keeps negative y only"""
        return self.cut_plane(planeaxis='Y Axis')

    def cut_plane(self, planeaxis ='Z Axis'):
        v = Volume(self)
        v.ms.generate_polyline_from_planar_section(planeaxis = planeaxis, splitsurfacewithsection = True) #plane_origin = (x,y,z), plane_normal = (nx,ny,nz))
        v.ms.set_current_mesh(3)
        v.ms.delete_non_visible_meshes()
        return v

    def regrid(self, iterations=20, pct=1):
        v = Volume(self)
        v.ms.meshing_isotropic_explicit_remeshing(iterations = iterations, targetlen = pymeshlab.PercentageValue(pct))
        return v

    def merge_close_vertices(self, pct=1):
        v = Volume(self)
        v.ms.meshing_merge_close_vertices(threshold  =  pymeshlab.PercentageValue(pct))
        v.ms.meshing_remove_null_faces()
        v.ms.meshing_repair_non_manifold_edges()
        v.ms.meshing_re_orient_faces_coherently()

        return v

    def save(self, filename):
        self.ms.save_current_mesh(file_name=filename)

    def to_polydata(self):
        """Returns a vtkPolyData object with the mesh data.
        Save to stl and then load the stl file into vtk"""

        file = tempfile.mktemp(".stl")
        self.save(file)

        from vtk import vtkSTLReader
        reader = vtkSTLReader()
        reader.SetFileName(file)
        reader.Update()

        return reader.GetOutput()

    def simplify(self):
        pd = self.to_polydata()
        from vtk import vtkDecimatePro

        # # triangulate first
        from vtk import vtkTriangleFilter
        tri = vtkTriangleFilter()
        tri.SetInputData(pd)
        tri.Update()

        decimate = vtkDecimatePro()
        decimate.SetInputData(pd)
        decimate.SetTargetReduction(1.0)
        decimate.SetPreserveTopology(1)
        decimate.Update()

        # save the output to stl

        file = tempfile.mktemp(".stl")
        writer = vtkSTLWriter()
        writer.SetFileName(file)
        writer.SetInputData(decimate.GetOutput())
        writer.Write()

        return Load(file)


def Box(xmin = -0.5, xmax = 0.5, ymin = -0.5, ymax = 0.5, zmin = -0.5, zmax = 0.5):
    """Returns a Box-shaped volume between the given outer dimensions"""
    c = Volume()
    c.ms.create_cube()

    dx = xmax - xmin
    dy = ymax - ymin
    dz = zmax - zmin

    c = c.scale(dx,dy,dz)
    c = c.move(0.5*(xmin+xmax), 0.5*(ymin+ymax), 0.5*(zmin+zmax))

    return c

def Cylinder(height=1, radius=1, resolution = 36):
    """Returns a Vertical cylinder with its origin at the bottom center

    The radius is scaled such that the volume is correct considering the discretisation / resolution
    """
    c = Volume()

    # using R=1
    required_area = pi / resolution
    alpha = 2*pi / resolution  # wedge angle

    r = sqrt(required_area / (sin(0.5*alpha)*cos(0.5*alpha)))


    c.ms.create_cone(r0=radius*r, r1=radius*r, h = height, subdiv = resolution)

    return c.rotate(x=90).move(z=height/2)

def Load(filename):
    v = Volume()

    v.ms.load_new_mesh(filename)
    return v

def Plot(v : Volume or list[Volume]):
    import vedo
    from matplotlib import cm
    COLORMAP = cm.tab20

    p = vedo.Plotter()

    if isinstance(v, Volume):
        v = [v]

    for icol, m in enumerate(v):
        vertices = m.ms.current_mesh().vertex_matrix()
        faces = m.ms.current_mesh().face_matrix()
        m2 = vedo.Mesh([vertices, faces])
        m2.actor.GetProperty().SetColor(COLORMAP(icol % 20)[:3])
        # m2.actor.GetProperty().SetOpacity(0.5)
        p.add(m2)

    p.show(axes=1, viewup='z')