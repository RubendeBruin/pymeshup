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


def test_hull2():
    c = Cylinder()
    b = Box(xmin=0, zmax=3, ymin=-3, ymax=3)
    d = 23
    e = c.inside_of(b)

    f = Box()
    f2 = Box()
    f3 = Box()
    f4 = Box()
    f5 = f4.move(2, 2)

    frame2 = (0, 0,
              0.1, 0,
              0.9, 0,
              1.0, 0.1,
              1, 1)

    frame1 = (0, -0.1,
              0.1, -0.1,
              0.1, 0.3,
              1, 0.3,
              1, 1)

    f1 = Frame(*frame1).autocomplete()
    f2 = Frame(*frame2).autocomplete()
    fb = Frame(0, 1)  # bow

    h = Hull(0, f1,
             5, f2,
             15, f2,
             20, fb)

    h = h.remove(c)