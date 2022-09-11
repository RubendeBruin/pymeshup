examples = dict()

examples['Creating tanks in loaded hull'] = """# Example of how to create tank in a given hull-shape

ch = Load('cheetah.stl')

ch_ps = ch.move(y=-1, z=1).crop(zmax=10.5)

ps1 = ch_ps.crop(xmin=1, xmax=15, ymin=1)
ps2 = ch_ps.crop(xmin=16, xmax=25, ymin=1)
ps3 = ch_ps.crop(xmin=26, xmax=35, ymin=1)
ps4 = ch_ps.crop(xmin=36, xmax=55, ymin=1)
ps5 = ch_ps.crop(xmin=36, xmax=55, ymin=1)
ps6 = ch_ps.crop(xmin=56, xmax=75, ymin=10)
ps7 = ch_ps.crop(xmin=76, xmax=120, ymin=10)
ps8 = ch_ps.crop(xmin=120, xmax=160, ymin=10, zmax=9)
ps9 = ch_ps.crop(xmin=161, xmax=180, ymin=10, zmax=9)
ps10 = ch_ps.crop(xmin=181, ymin=10, zmax=9)

# create a copy with a small offset to cut the tanks from
ch_sb = ch.move(y=1, z=1).crop(zmax=10.5)

sb1 = ch_sb.crop(xmin=1, xmax=15, ymax=-1)
sb2 = ch_sb.crop(xmin=16, xmax=25, ymax=-1)
sb3 = ch_sb.crop(xmin=26, xmax=35, ymax=-1)
sb4 = ch_sb.crop(xmin=36, xmax=55, ymax=-1)
sb5 = ch_sb.crop(xmin=36, xmax=55, ymax=-1)
sb6 = ch_sb.crop(xmin=56, xmax=75, ymax=-10)
sb7 = ch_sb.crop(xmin=76, xmax=120, ymax=-10)
sb8 = ch_sb.crop(xmin=120, xmax=160, ymax=-10, zmax=9)
sb9 = ch_sb.crop(xmin=161, xmax=180, ymax=-10, zmax=9)
sb10 = ch_sb.crop(xmin=181, ymax=-10, zmax=9)

ch_c = ch.move(z=1)

c7 = ch_c.crop(xmin=76, xmax=120, ymin=-9, ymax = 9)
c8 = ch_c.crop(xmin=121, xmax=160, ymin=-9, ymax = 9, zmax=9)
c9 = ch_c.crop(xmin=161, xmax=180, ymin=-9, ymax = 9, zmax=11)
c10 = ch_c.crop(xmin=181, ymin=-9, ymax = 9, zmax=11, xmax = 200)

# remove the temporary copies such that they are not
# displayed or exported
del ch_ps
del ch_sb
del ch_c
"""

examples['Make diffraction mesh'] = """# Example of generating a panel mesh from a predefined hullshape

ch = Load('cheetah.stl')

draft = 8
panel_size = 3 # as percentage

cheetah_panels = ch.crop(zmax=draft).move(z=-draft).regrid(pct=panel_size)
"""
