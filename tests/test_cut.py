from pymeshup import *

def test_cut():
    a = Box()
    a = a.cut_at_xz()

    Plot(a)