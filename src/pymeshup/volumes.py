import pymeshlab

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
        v.ms.compute_matrix_from_translation_rotation_scale(scalex=x, scaley=y, scalez=z)
        return v

    @property
    def vertices(self):
        return self.ms.current_mesh().vertex_matrix()

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