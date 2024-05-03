from pymeshup import *

def test_crop():
    a = Box()
    a.crop(xmax=0)

def test_add():
    a = Box()
    c = Cylinder()

    p = a.add(c)

    Plot(p)


def test_load():
    a = Load('cheetah.obj')
    Plot(a)
