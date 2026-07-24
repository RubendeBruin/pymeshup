# Read the following stl file.
# This is a typical example of a bad vessel hull shape mesh.
#
# Volume.reframe() rebuilds the hull by slicing it into horizontal waterlines
# and lofting them, giving a clean, watertight, port/starboard-symmetric hull
# Volume (a bulbous bow / stern bulb comes out as one smooth surface).

from pymeshup import Load

def test_extract_frames(assets_dir):
    filename = assets_dir / "lq_3dpea.com_kvlcc2.stl"

    bad_hull = Load(filename)

    # Rebuild a clean hull by lofting horizontal waterlines.
    hull = bad_hull.reframe(n_waterlines=100)
    hull2 = hull.reframe(n_waterlines=10)

    _ = hull2.volume
