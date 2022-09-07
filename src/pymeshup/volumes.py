import pymeshlab
from math import sqrt, cos, sin, pi

class Volume():

    def __init__(self, volume : "Volume" or None = None):
        self.ms = pymeshlab.MeshSet()

        if volume:
            self.ms.add_mesh(mesh = volume.ms.current_mesh())

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


    def rotate(self, x=0, y=0 , z=0):
        """Returns a rotated copy of the volume, rotation in degrees; Euler angles"""
        v = Volume(self)
        v.ms.compute_matrix_from_translation_rotation_scale(rotationx=x, rotationy=y, rotationz=z)
        return v

    def add(self, other):
        """Returns a copy with other added to the volume"""
        v = Volume(self)
        v.ms.add_mesh(other.ms.current_mesh())
        v.ms.mesh_boolean_union()

        return v

    def remove(self, other):
        """Returns a copy with other subtracted from the volume"""
        v = Volume(other)
        v.ms.add_mesh(self.ms.current_mesh())
        v.ms.mesh_boolean_difference()

        return v

    def inside_of(self, other):
        """Returns the intersection (common part) with other volume"""
        v = Volume(self)
        v.ms.add_mesh(other.ms.current_mesh())
        v.ms.mesh_boolean_intersection()

        return v


    @property
    def vertices(self):
        return self.ms.current_mesh().vertex_matrix()

    @property
    def volume(self):
        return self.ms.get_geometric_measures()['mesh_volume']

    @property
    def center(self):
        return self.ms.get_geometric_measures()['center_of_mass']



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

def Plot(v : Volume or list[Volume]):
    import vedo
    p = vedo.Plotter()

    if isinstance(v, Volume):
        v = [v]

    for m in v:
        vertices = m.ms.current_mesh().vertex_matrix()
        faces = m.ms.current_mesh().face_matrix()
        m2 = vedo.Mesh([vertices, faces])
        p.add(m2)

    p.show(axes=1, viewup='z')