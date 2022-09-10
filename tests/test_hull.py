from pymeshup import *

#
frame2 = (0,0,
          0.1, 0,
          0.9,0,
          1.0,0.1,
          1,1)

frame1 = (0,-0.1,
          0.1, -0.1,
          0.1, 0.3,
          1,0.3,
          1,1)




def test_hull():
    f1 = Frame(*frame1).autocomplete()
    f2 = Frame(*frame2).autocomplete()
    fb = Frame(0,1) # bow

    h = Hull(0,f1,
             5,f2,
             15,f2,
             20,fb)

    Plot(h)