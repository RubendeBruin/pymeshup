from datetime import datetime

from pymeshup import *

"""Trick to get volumes as variables:

for part in a.parts.keys():
	name = part.replace('.','_')
	exec(f'{name} = a.parts["{part}"]["volume"]')

"""
# def test_read_ghs_with_circular_segments_default():
#     a =GHSgeo(r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE.GF1", circular_segments_step=10)
#     shape = a.shapes_outside['HULL']
#
#     Plot(shape)


def test_read_ghs_with_circular_segments():
    a =GHSgeo(r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE.GF1", circular_segments_step=1)
    shape = a.shapes_outside['HULL']
    assert shape.volume == 2719.7268458294716

    Plot(shape)
#
#
if __name__ == '__main__':
    filename_gf1 = r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\tank.gf1"
    # filename = r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE_SPUD.GF1"
    a = GHSgeo(filename_gf1) # , circular_segments_step=1)

    # shapes = [_ for _ in a.shapes_raw.values()]
    # Plot(shapes)
    #
    # # print(a.warnings)
    # #

    a.rotate180()  # to align with positive x axis

    Plot(a.shapes_raw['s14'])

    parts = []

    for name, part in a.parts.items():
        vol : Volume = part['volume']

        parts.append(vol)

    #
    #
    #
    #
    Plot(parts)

