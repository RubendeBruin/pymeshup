from pymeshup import *

def test_crop():
    a = Box()
    a.crop(xmax=0)

def test_load():
    a = Load('cheetah.obj')
    Plot(a)
