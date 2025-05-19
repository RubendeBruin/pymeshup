from datetime import datetime

from pymeshup import *

"""test two skegs

This file 

- defines a single SHAPE with the name s2, this shape is off-center
- it then defines a 


TWOSKEGS
L:246.06
W:77.64
P:M
N:1
OT:Centerplane
OV:Baseline
*
s2                 <--- name of the shape
61                 <--- number of points
-24.6063,5
19.3077,0
...
20.7841,4.8885
19.3077,4.8885
19.3077,0         <--- first last point
0,0,0             <--- shell thickness
**                <--- start of component
SKEG1.C           <-- name
0                 <-- side,  If only half of the component is described by the shape data (the other half being described by reflecting the transverse coordinates about the shape's origin), the side factor is 0.
1                 <-- effectiveness
0,0,0             <-- offset
s2                <-- shape name
***
HULL
SEA WATER
1
1.025
0,0,0
1
SKEG1.C
****


"""

def test_skegs(assets_dir):

    filename_gf1 =assets_dir / "skegs_only.GF"
    a = GHSgeo(filename_gf1) # , circular_segments_step=1)

    # single shape s2
    shape : Volume = a.shapes_raw['s2']

    print(shape.center)
    print(shape.bounds)

    # component
    cmp = a.components['SKEG1.C']
    # The

    skeg_volume = a.parts['HULL']['volume']

    # Skeg is defined outside the centerline (clearly on one side)
    assert abs(skeg_volume.center[1]) < 0.1, "Skegs is not centered on the centerline"
    assert skeg_volume.volume > 1, "Skeg volume is too small"


