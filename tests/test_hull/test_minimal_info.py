"""This issue here is that that frames are not connected property.

This has to do with the autocomplete function in combination with the first vertex not being at x=0
"""

from pymeshup import Frame, Hull, Plot


def test_create_negative_startpoints():
    x1 = [1]
    y1 = [1]

    x2 = [0, 10, -10]
    y2 = [0, 1, 1]

    f1 = Frame.from_xy(x1, y1)
    f2 = Frame.from_xy(x2, y2)

    h = Hull(0,f1, 10,f2)

    _ = h.volume

