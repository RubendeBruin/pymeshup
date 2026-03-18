from pymeshup import Volume, GHSgeo


"""test two skegs

This file defines a single SHAPE with the name s2



"""

def test_ghs(assets_dir):
    filename_gf1 = assets_dir / "skegs_only.GF"
    # filename = r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE_SPUD.GF1"
    a = GHSgeo(filename_gf1)  # , circular_segments_step=1)

    # single shape s2
    shape: Volume = a.shapes_raw["s2"]

    print(shape.center)
    print(shape.bounds)

    print(shape)

    #
    # shapes = [_ for _ in a.shapes_raw.values()]
    # Plot(shapes)

    # # print(a.warnings)
    # #

    # a.rotate180()  # to align with positive x axis

    # skeg = a.parts['HULL']['volume']

    # Skeg is defined outside the centerline (clearly on one side)

    # Plot(skeg)
