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

frame0 = (0,1)

# two point frame
frame_2p = (-1,0,
              1,0)

frame_3p_line = (-1,0,
                 0,0,
                 1,0)

frameh = (0,-0.1,
          0.1, -0.1,
          0.1, 0.3)




def test_hull():
    f1 = Frame(*frame1).autocomplete()
    f2 = Frame(*frame2).autocomplete()
    fb = Frame(0,1) # bow

    h = Hull(0,f1,
             5,f2,
             15,f2,
             20,fb)

    Plot(h)

def test_hull00():
    f0 = Frame(*frame0).autocomplete()
    f2 = Frame(*frameh).autocomplete()

    h = Hull(0,f0,
             5,f2,
             15,f0)

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

def test_hull_2p_end():
    f1 = Frame(*frame1).autocomplete()
    fb = Frame(*frame_2p)  # bow

    h = Hull(0, f1,
             5, fb)
    # Plot(h)

def test_hull_flat_end():
    f1 = Frame(*frame1).autocomplete()
    fb = Frame(*frame_3p_line)  # bow

    h = Hull(0, f1,
             5, fb)
    # Plot(h)

def test_once_failed():
    frames = []
    for i in range(7):
        frames.append(Frame(0, 0))

    frames[0].xy = ((5.7579768, 0.2801112), (6.2941199999999995, 0.2801112), (5.7579768, 0.2801112))
    frames[1].xy = (
        (5.7171336, 0.0), (6.3349632, 0.0), (6.3349632, 0.3941064), (5.7171336, 0.3941064), (5.7171336, 0.0))
    frames[2].xy = ((5.670194400000001, 0.0), (6.3819023999999995, 0.0), (6.3819023999999995, 0.8330184),
                    (5.670194400000001, 0.8330184), (5.670194400000001, 0.0))
    frames[3].xy = ((5.5830216, 0.0), (6.469075200000001, 0.0), (6.469075200000001, 1.6669512000000002),
                    (5.5830216, 1.6669512000000002), (5.5830216, 0.0))
    frames[4].xy = (
        (5.5522368, 0.0), (6.533997600000001, 0.0), (6.533997600000001, 2.221992), (5.5522368, 2.221992),
        (5.5522368, 0.0))
    frames[5].xy = ((5.9960256, 0.12009120000000001), (6.0560712, 0.12009120000000001), (6.395923200000001, 1.1801856),
                    (6.4660272, 1.7397984000000002), (6.2109096, 2.4301704), (5.840882400000001, 2.4301704),
                    (5.586069600000001, 1.7397984000000002), (5.6558688, 1.1801856), (5.9960256, 0.12009120000000001))
    frames[6].xy = ((6.025896, 1.4999208000000002),)

    # frames = [*reversed(frames)]

    # h = Hull(-11.6659152,
    #          frames[0],
    #          -11.318138400000002,
    #          frames[1])
    #
    # Plot(h)
    #
    h = Hull(-11.6659152,
             frames[0],
             -11.318138400000002,
             frames[1],
             -9.9998784,
             frames[2],
             -7.499908800000001,
             frames[3],
             -5.833872,
             frames[4],
             -5.2090320000000006,
             frames[5],
             -3.9489888,
             frames[6], )