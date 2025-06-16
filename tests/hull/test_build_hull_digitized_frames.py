"""This issue here is that that frames are not connected property.

This has to do with the autocomplete function in combination with the first vertex not being at x=0
"""

from pymeshup import *

if __name__ == '__main__':

    f4 = Frame(0.003, 0.258,
               0.570, 0.291,
               1.018, 0.296,
               2.572, 0.430,
               5.898, 0.655,
               8.818, 0.909,
               9.812, 1.199,
               10.371, 1.513,
               10.793, 1.963,
               10.957, 3.264,
               10.982, 4.395,
               10.963, 7.746,
               ).autocomplete()


    f5 = Frame(0, 0.055,
               0.589, 0.072,
               2.668, 0.043,
               4.987, 0.059,
               7.417, 0.064,
               9.619, 0.064,
               10.017, 0.135,
               10.380, 0.365,
               10.775, 0.730,
               10.947, 1.187,
               10.982, 4.395,
               10.963, 7.746,
               ).autocomplete()

    print(f4.xy)
    print(f5.xy)
    #
    h = Hull(
             # 40, f3,
             50, f4,
             60, f5)
    #
    Plot(h)