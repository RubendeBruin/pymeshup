from datetime import datetime
from pathlib import Path

"""
This file contains a function to convert a GHS (GF1 or GF2) file to a DAVE vessel file

The GHSgeo class is still under development so this function should be considered experimental

"""



def GHS_to_DAVE(
    filename_gf1,
    vessel_name,
    outdir = None,
    circular_segments_step=10,
    output: list = None,
    resource_prefix = None
):
    """Converts a GHS file to a DAVE vessel file

    Output may be given as a list, in that case the output is added to that object (can be handy when no
    data is returned in case of exception)

    """

    if not vessel_name:
        raise ValueError("No vessel name given, please provide a name")


    if outdir == '':
        outdir = None

    if outdir is None:
        outdir = Path(filename_gf1).parent

    if resource_prefix is None:
        resource_prefix = f"res: {vessel_name}/geometry/"

    if output is None:
        output = []

    from pymeshup import GHSgeo, Volume

    output.append("reading GHS file:" + filename_gf1)

    # make sure that the output directory exists
    outdir = Path(outdir)
    outdir = outdir.resolve()

    outdir = outdir / vessel_name

    if not outdir.exists():
        outdir.mkdir(parents=True, exist_ok=True)

    # make sure that the geometry directory exists
    geometry_dir = outdir / "geometry"
    if not geometry_dir.exists():
        geometry_dir.mkdir(parents=True, exist_ok=True)

    # let the user know where we are writing to
    output.append("saving to vessel to " + str(outdir))
    output.append("saving geometry to " + str(geometry_dir))


    output.append("Reading GHS file, may take a while...")
    a = GHSgeo(filename_gf1, circular_segments_step=circular_segments_step)
    output.extend(a.warnings)

    Path(outdir).mkdir(exist_ok=True)
    output.append("saving to " + str(outdir))

    a.rotate180()  # to align with positive x axis

    # Construct a DAVE vessel csv file

    for name, part in a.parts.items():
        if "volume" not in part:
            output.append(
                f"WARNING: Failed to write .stl file for {name}, volume does not exist"
            )
            continue

        vol: Volume = part["volume"]

        filename = f"{outdir}/geometry/{name}.stl"

        vol.save(filename)

    # generate a DAVE vessel file

    # hull: Volume = a.parts["HULL"]["volume"]

    # get the hull for the parts lists
    # this is the part with part_type 1 (int) with the largest volume

    hull = None
    hull_volume = 0
    for name, part in a.parts.items():
        if part["part_type"] == 1:
            if part["volume"].volume > hull_volume:
                hull = part["volume"]
                hull_volume = part["volume"].volume
    if hull is None:
        output.append("WARNING: No hull found in GHS file")
        return output

    # get deck elevation
    general = dict()

    deck_elevation = hull.bounds[5]  # max-z
    keel_elevation = hull.bounds[4]  # min-z

    general["deck_elevation"] = deck_elevation
    general["keel_elevation"] = keel_elevation

    general["tank_cut_elevation"] = deck_elevation * 0.9
    general["barge_cut_elevations"] = (
        0.5 * keel_elevation + 0.5 * deck_elevation,
        deck_elevation * 0.9,
    )

    general["width"] = hull.bounds[3] - hull.bounds[2]
    general["length"] = hull.bounds[1] - hull.bounds[0]

    general["Cd_air_long"] = 1.2
    general["Cd_water_long"] = 1.2
    general["Cd_air_trans"] = 1.2
    general["Cd_water_trans"] = 1.2

    # Ballast tanks
    ballast_tanks = dict()

    for name, part in a.parts.items():
        if (
            part["part_type"] == 4
        ):  #  4 - Containment part  (e.g. a tank or compartment):
            # Name, resource, permeability,density,Fill-pct, off-x, off-y, off-z, rot-x, rot-y, rot-z, scale-x, scale-y, scale-z, invert-normals

            try:
                volume = part["volume"].volume
            except Exception as e:
                output.append(
                    f"WARNING: {name} has an error in the volume calculation, skipping it."
                )
                continue

            if volume < 0:
                invert_normals = True
            else:
                invert_normals = False

            data = (
                name,
                resource_prefix + name + ".stl",
                1,  # permeability
                -1,  # density. set -1 for outside water
                0,  # fill-pct
                0,  # off-x
                0,  # off-y
                0,  # off-z
                0,  # rot-x
                0,  # rot-y
                0,  # rot-z
                1,  # scale-x
                1,  # scale-y
                1,  # scale-z
                invert_normals,
            )  # invert-normals
            ballast_tanks[name] = data

    # Buoyancy parts

    buoyancy = dict()
    for name, part in a.parts.items():
        if (
            part["part_type"] == 1
        ):  #  1 - Displacement part (e.g. HULL including appendages)
            # Name, resource, off-x, off-y, off-z, rot-x, rot-y, rot-z, scale-x, scale-y, scale-z,invert-normals,,
            data = (
                name,
                resource_prefix + name + ".stl",
                0,  # off-x
                0,  # off-y
                0,  # off-z
                0,  # rot-x
                0,  # rot-y
                0,  # rot-z
                1,  # scale-x
                1,  # scale-y
                1,  # scale-z
                False,
            )
            buoyancy[name] = data

    # draft measurement points
    draft_measurement_points = dict()
    draft_measurement_points["AFT"] = (0, 0, 0)
    draft_measurement_points["BOW"] = (hull.bounds[1], 0, 0)
    draft_measurement_points["PS"] = (hull.bounds[1] / 2, hull.bounds[2], 0)
    draft_measurement_points["SB"] = (hull.bounds[1] / 2, hull.bounds[3], 0)

    header = """
#    THIS FILE IS AUTOMATICALLY EXPORTED FROM THE GHS (GF1) GEO FILE.
#    [ ] MAKE A COPY OF THIS FILE AND EDIT THE COPY.
#    
#    IN THE COPY:
#    [ ] ADD A HEADER WITH A DESCRIPTION OF THE VESSEL AND THE SOURCE OF THE DATA
#    [ ] ADD LIGHTSHIP WEIGHT
#    
#    OPTIONALLY
#    [ ] TWEAK THE GENERAL SETTINGS FOR VISUALS (CUT ELEVATIONS) AND LENGTH AND WIDTH
#    [ ] CHANGE THE VISUAL, IT IS INITIALLY SET TO THE HULL BUOYANCY PARTS (WHICH IS OK) BUT YOU PROBABLY WANT SOMETHING ELSE
#    [ ] ADD ADDITIONAL (NON BALLAST) TANKS IF ANY
#    [ ] ADD INERTIA IF YOU WANT TO DO DYNAMICS, AS GUIDANCE:
#        rxx = 0.3..0.4 * WIDTH
#        ryy = rzz = 0.22 ... 0.28 * LENGTH
#    [ ] ADD BOLLARDS IF ANY
#    [ ] ADJUST THE DRAFT MEASUREMENT POINTS IF NEEDED
#      
# REVISION HISTORY
# rev   |   date        |   description"""

    header += (
        "\n# 0\t| "
        + datetime.now().strftime("%Y-%m-%d %H:%M")
        + "\t|\tauto-generated from: "
        + filename_gf1
        + "\n#\n"
    )

    additional = """
#
#  EXAMPLE OF ADDITIONAL DATA TO BE ENTERED
#    
# *LightWeight													
#
# This defined the weight and inertia of the barge. Inertia is only used when doing dynamics.
#
#					Footprint					Dynamics			
# Name	mass [mT]	Cog-x	Cog-y	Cog-z	Fp-elevation	aft	front	sb	ps	rxx	ryy	rzz	
#	mT	m	m	m	m	m	m	m	m	m	m	m	
# front	10000	180	0	2.5	2	160	210	-22.5	22.5	20	25	25	
# main	20000	105	0	2.5	2	20	160	-22.5	22.5	20	100	100	
# stern	5000	3	0	2.5	2	0	20	-22.5	22.5	20	16	18	
# *Bollards													
#													
# name	Pos-x	Pos-y	Pos-z	capacity	capcity-x	 capcity-y								
# *OtherTanks													
#
# Other tanks are tanks that are not included in the ballast system.
# The total volume of the tank is derived from the geometry. Use permeability to tune the capacity.
#													
# Name	 resource	 permeability	density	Fill-pct	 off-x	 off-y	 off-z	 rot-x	 rot-y	 rot-z	 scale-x	 scale-y	 scale-z	 invert-normals
#													
"""

    # write to file
    outfile = f"{outdir}/{vessel_name}.vessel.csv"
    with open(outfile, "w") as f:
        f.write(header)
        f.write("# General\n")
        for key, value in general.items():
            try:
                values = "\t".join(map(str, value))
            except:
                values = str(value)
            f.write(f"{key}\t{values}\n")

        f.write("\n# Ballast tanks\n")
        f.write(
            "# Name\t resource\t permeability\t,density\t,Fill-pct\t,off-x\t off-y\t off-z\t rot-x\t rot-y\t rot-z\t scale-x\t scale-y\t scale-z\tinvert-normals\n"
        )
        f.write("# Use density = -1 for same density as outside water\n")
        f.write("# Use permeability to fine-tune effective volume of the tank\n")
        f.write("*BallastTanks\n")
        for key, value in ballast_tanks.items():
            f.write("\t".join(map(str, value)) + "\n")

        f.write("\n# Buoyancy\n")
        f.write(
            "\n# Name\t resource\t off-x\t off-y\t off-z\t rot-x\t rot-y\t rot-z\t scale-x\t scale-y\t scale-z\tinvert-normals\n"
        )
        f.write("*Buoyancy\n")
        for key, value in buoyancy.items():
            f.write("\t".join(map(str, value)) + "\n")

        f.write("\n# Draft measurement points\n")
        f.write("*Draft_measurement_points\n")
        for key, value in draft_measurement_points.items():
            f.write(f"{key}\t{value[0]}\t{value[1]}\t{value[2]}\n")

        f.write("\n# Visual\n")
        f.write(
            "\n# Name\t resource\t off-x\t off-y\t off-z\t rot-x\t rot-y\t rot-z\t scale-x\t scale-y\t scale-z\n"
        )
        f.write("*Visuals\n")
        for key, value in buoyancy.items():
            f.write("\t".join(map(str, value[:-1])) + "\n")

        f.write(additional)

    output.append(f"saved to: {outfile}")

    return output
