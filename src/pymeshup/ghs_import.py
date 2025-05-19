r"""

# https://converthullform.aerohydro.nl/Externals/GHS_format-APPEND-A.htm

General HydroStatics System

Geometry File Format



The GHS Geometry File (GF) describes the shapes and locations of the elements of the vessel model which are involved in: 1) the ship's hull, appendages and other displacers; 2) the internal tanks and compartments; and 3) the non-displacing elements which contribute windage.

The Geometry File format is designed to be easily handled by various programs using various means of internal data storage. Hence, it is an ASCII text file and the numerical values are decimal.

The details of the Geometry File format are presented here. This information can be used to construct interfaces enabling programs using other geometrical representations to read and write GHS Geometry Files.

General

The Geometry File consists of a series of text lines, beginning with a title line and ending with a line containing four asterisks (****). Between these limits there may be one or more of the several data elements and structures described below. The order of occurrence and number of occurrences within the file are restricted only where such restrictions are mentioned.

Where a series of numbers is on a single line, the numbers must be separated by commas (commas within a number are not allowed). Spaces surrounding the commas are optional. A trailing comma at the end of a numerical line should not be used.


Title Line

The title is a single line containing a description and name of the vessel. It must be the first line of a GF, and its length should not exceed 58 characters.


Reference Number

Immediately following the title is an optional line containing a reference number. If present, this line must begin with a digit. The reference number may be divided into two parts separated by a slash:

     Vessel reference \ Owner reference

The vessel reference must begin with a digit and may contain up to 12 characters. The owner reference, which is limited to 3 characters, may contain letters and digits. If the owner reference is omitted, the slash may be omitted also. Blanks are not allowed on this line.


Comments

Comments may be included in the GF to convey notes or to alert the user to peculiarities. (GHS displays the comments when reading a GF, and they are available subsequently through the COMMENT command.) A comment is one line beginning with a back slash character (\) followed by up to 79 characters of text. Example:

\Offsets were scaled from a copy of the lines drawing 1234-A dated 12/19/1938.

Up to 10 comments may be included between the title and the first shape.


Miscellaneous-Information Lines

Also between the title and the first shape, any number of lines of miscellaneous information may appear, subject to the following restrictions:

The first character on any such line must not be an asterisk or a back slash.

To avoid conflict with GHS programs which may place information in this area, such a line
should contain neither colons (:) nor equal signs (=) if it begins with an alphabetic character.

GHS uses the following miscellaneous-information lines:

L:Overall length of the model

W:Overall breadth of the model

P:Units Preference

OL:Longitudinal origin plane description

OT:Transverse origin plane description

OV:Vertical origin plane description

N:Number of Part records in the file

The Units Preference is a single letter: M for meters or F for feet. This does not affect the units used in the Geometry File itself (they are always feet) but indicates to the using program what units it should initially present.

The origin plane descriptions are limited to a maximum of 25 characters of text each.




Parts

The part data structure collects one or more components under a common name, and supplies additional data common to the part.

Part format:
            ***
            Part name \ Part description
            Fluid name
            Type of part
            Specific gravity of the fluid
            Reference point
            n (number of components in the part)
            Component 1 name
            ...
            Component n name
            m (number of points defining a sounding tube)
            Point 1
            ...
            Point m
            -1
            Shear correction factor

1st part line:  three asterisks.  These must be the only characters on the line.

2nd part line:  the part name and optional description.  The part name must be the only thing
preceding the backslash or the only thing on the line; there must be no leading or trailing
blanks around the part name.  Only upper-case letters and digits, periods and hyphens should
be used.  Its length should be not more than 12 characters (14 characters for tanks if a side-
indicating suffix is present).  Suffixes are only recognized on thank parts and must have the
same format as component suffixes, but are otherwise irrelevant to the data structure.  No two
parts in the Geometry File may have the same name.  If the part description is present, it
immediately follows the back slash and contains 20 or fewer characters.

3rd part line:  Fluid name is the description of the fluid with which this part is concerned.  If it
is a displacer, this would be the water environment in which the vessel is floating (e.g. SEA
WATER or FRESH WATER).  If it is a container such as a tank, this would be the contents
(e.g. FUEL OIL, LUBE OIL, FRESH WATER, etc.).   The fluid name should not exceed 12
characters.

4th part line:  Part type is an integer indicating whether the part a) contributes to displacement,
b) is essentially a container or c) is only for windage purposes; specifically:

            1 - Displacement part (e.g. HULL including appendages)
            4 - Containment part  (e.g. a tank or compartment)
           10 - Sail (windage) part (e.g. non-watertight superstructure)

5th part line: specific gravity of the fluid named in line 3 above. Specific gravity is the density of the fluid divided by the maximum density of pure water, which is 1000 kg per cubic meter.

6th part line: The reference point is used for various purposes, depending on the type of the part. For tanks, the reference point can mark the point of suction, the point from which an ullage is taken, the point of damage or spilling, etc. The reference point text contains three numbers giving the longitudinal, transverse and vertical coordinates, respectively. It is relative to the vessel's overall origin.

7th part line: the number of components included in the part. This must be an integer greater than zero. It is the count of the component-referencing lines which follow.

8th ... 7+mth part lines: These lines contain component names exactly matching one of the component names which have previously been defined.

8+mth part line: Beginning the sounding tube definition, this line contains the count of the number of points representing the sounding tube. For displacement-type parts the sounding tube is irrelevant, and this line may be omitted. Containment-type groups should always include this line, even if there is no sounding tube (in which case the number of points is zero).

9+mth ... 8+m+nth part lines: If there is a sounding tube, these lines give the points which define the center of the tube, starting from the striker plate and continuing to the top of the tank or beyond. In case of a straight tube, only two points are required. If the tube is bent or curved, enough points should be included to model the tube with reasonable accuracy. Sounding tube points are relative to the vessel's origin. Each line contains the coordinates of one point; i.e. three numbers in longitudinal, transverse, vertical order.

Additional optional lines: -1 introduces a "shear correction factor" which applies only to tank parts and must be in the range zero to 1.0. The value depends on details of the construction of the tank and is used to reduce the slope of the shear force curve contributed by the load in the tank.


Critical Points

The critical point data structure gives the description and location of a point on the vessel which is of some particular interest, such as a downflooding point.

Critical Point Format:
            *CRT
            n, description
            location

1st critical point line: a single asterisk immediately followed by the upper case letters "CRT".

2nd line: n is the number of the critical point which must be an single digit from 1 to 99. Each critical point must be assigned a different number; hence the total number of critical points cannot exceed 9. Immediately following the critical point number and separated from it by a comma is the description, which may be any displayable text string of up to 25 characters in length.

3rd line: location of the critical point relative to the overall vessel origin (three coordinates in longitudinal, transverse, vertical order).


Notes


Units

Distance units are always in feet. If the metric system is preferred, the programs reading and writing the Geometry File are responsible for conversion.


The Coordinate System

A three-dimensional cartesian coordinate system is used. The three directions are referred to as longitudinal, transverse and vertical.

The longitudinal direction is identified with the vessel's fore and aft direction. Longitudinal coordinates are lesser toward the bow and greater toward the stern. A baseline, assigned when the ship is designed or measured, determines the longitudinal direction. (The baseline may or may not be parallel to the keel.) The longitudinal direction is the direction of the baseline.

Vertical is the direction perpendicular to the waterplane when the baseline is parallel to the waterplane and the vessel has no list or heel. Greater vertical coordinates are more upward, lesser downward.

The transverse direction is identified with the vessel's athwartship direction and is perpendicular to both the vertical and longitudinal directions. Greater transverse coordinates are more to starboard, lesser to port.

The origin of the coordinate system is arbitrary, but its location should be noted prominently, preferably by use of the OL:, OT: and OT: information lines. A COMMENT line further describing the location of the origin may also be helpful. It is usually most convenient to have the origin on the baseline at the centerplane of the vessel.


The Interpretation of Shape Geometry

A three-dimensional shape is represented as a series of sections, or cuts, made perpendicular to the longitudinal axis. The surface of the shape is considered to be flat between sections (i.e. the surface area between sections is minimum). The faces of the first and last sections are themselves the end surfaces of the shape.

It is further assumed that the immersed sectional area and wetted girth from one section to the next varies nearly linearly. Since this requirement should be met at any anticipated angle of heel, depth and trim, even parallel-sided shapes need to be represented by several sections along their length.

Each section is interpreted as a closed curve made up of straight lines connecting points 1...m. In the case of transverse symmetry about the shape's centerplane, it is permissible to omit the negative (port) side of the section curve, in which case the points are re-traversed in reverse order with the transverse coordinate negated. It is always assumed that the curve is closed by returning to the starting point after the last point.


Approximating Curved Surfaces

Curved surfaces can only be represented approximately, since the shape geometry is based on straight lines. However, a close approximation can be obtained by placing the sections and points close together.

The error in area under a smooth curve of average height c which departs from the straight line approximation by an amount d is less than the fraction d/c of the area. This can be used as a guide in fixing the distance between points on sections and the distance between sections.

A reasonable standard of accuracy for ship stability/strength calculations is a volume error of 0.3%. This can be attained if the errors due to longitudinal and transverse linearization are each kept to 0.15%. Most section curves can be represented to this degree of accuracy with 20 or fewer intervals. Typical longitudinal area curves require about 25 intervals.

More closely spaced points and sections are required where extreme curvature or discontinuities are present. Any abrupt change in section should be represented by two closely spaced sections, one on either side of the change. However, the closest section spacing should not be less than 0.01 foot.
Copyright (C) 1997-1999 Creative Systems, Inc.
"""

from .frames import Frame
from .volumes import Volume
from .hull import Hull
from .helpers.geo_math import points_on_circle


class GHSgeo:
    def __init__(self, filename, circular_segments_step=999):
        """
        Parameters
        ----------
        filename : str
            The name of the GHS geometry file to read.
        circular_segments_step : maximum distance (degrees) between points on a circular segment. Default to 999 (no additional points segments).
            Used for the "radius" definitions in the geometry file.
        """

        self.filename = filename
        self.circular_segments_step = circular_segments_step

        self.warnings = []
        self.shapes_outside = dict()  # volumes representing the outside of the hull
        self.shapes_inside = (
            dict()
        )  # volumes representing the inside of the hull, difference is due to thickness
        self.shapes_raw = (
            dict()
        )  # raw shapes as read from the geometry file, not autocompleted
        self.components = dict()
        self.parts = dict()

        # self.frames = []
        # self.volumes = []

        self.data = dict()

        self.read()

    def __getitem__(self, name) -> Volume:
        return self.get_volume(name.upper())


    def get_volume(self, name) -> Volume:
        """Returns the volume of the part with the given name"""
        if name not in self.parts:
            raise ValueError(f"Part {name} not found")

        if "volume" not in self.parts[name]:
            raise ValueError(f"Part {name} has no volume")

        return self.parts[name]["volume"]


    def read(self):
        with open(self.filename, "r") as f:
            self.lines = f.readlines()

        # remove comments
        self.lines = [line for line in self.lines if not line.startswith("\\")]

        self.read_header()

        # read the remaining sections

        while self.lines:
            next = self.lines.pop(0)

            if next.startswith("****"):
                break

            elif next.startswith("***"):
                print("Reading part")
                self.read_part()
                continue

            elif next.startswith("**"):
                print("Component part")
                self.read_component()
                continue

            elif next.startswith("*"):
                print("Reading Shape Record")
                self.read_shape_record()
                continue

            self.warnings.append("Unrecognized line: {}".format(next))

        self.compile()

    def rotate180(self):
        """Rotates all parts by 180 degrees"""

        for part in self.parts.values():
            if "volume" in part:
                part["volume"] = part["volume"].rotate(0, 0, 180)

    def compile(self):
        # Compiles the final parts of the geometry file

        for name, values in self.parts.items():
            # combine the components into a single volume

            try:
                volume = Volume()

                print("Compiling part {}".format(name))

                for component_name in values["components"]:
                    component = self.components[component_name]
                    shape_name = component["shape_name"]

                    print("  Adding shape {} to part {}".format(shape_name, name))

                    #
                    side_factor = component["side_factor"]

                    if side_factor == 0:

                        # If the side-factor is 0 then only half the shape was defined.
                        # It is possible that this was already taken into account in the shape definition
                        # using the "autocompleted" function. In that case shapes_outside contains
                        # the autocompleted shape.
                        #
                        # But it is also possible that the shape was purposely defined as a single side shape
                        # on a single side, for example a skeg, and the raw shape shall be mirror-copied
                        # to the other side.
                        #
                        # This is easily checked by looking at the y-bounds of the raw shape. If both of them
                        # are on the same side (product > 0) then the shape was defined as a single side shape
                        # and its mirror shall be added.

                        shape: Volume = self.shapes_outside[shape_name] # default
                        print(
                            "   Side factor = {} using autocompleted volume".format(
                                side_factor
                            )
                        )

                        if shape_name in self.shapes_raw:
                            as_defined_shape = self.shapes_raw[shape_name]
                            if as_defined_shape.bounds[2] * as_defined_shape.bounds[3] > 0:
                                # the shape was defined as a single side shape
                                print(
                                    "   REDEFINING; Using raw volume and adding mirror copy"

                                    )

                                shape = as_defined_shape.add(as_defined_shape.mirrorXZ())




                    else:
                        print(
                            "   Side factor = {} using single-side volume".format(
                                side_factor
                            )
                        )
                        shape: Volume = self.shapes_raw[shape_name]

                    # part_type = component['part_type']

                    # shift and mirror the shape if necessary
                    if component["side_factor"] < 0:
                        print("    Mirroring shape {} in XZ".format(shape_name))
                        shape = shape.mirrorXZ()

                    shape = shape.move(*component["origin_shift"])
                    print(
                        "    Moving shape {} by {}".format(
                            shape_name, component["origin_shift"]
                        )
                    )

                    # are we an addition or a subtraction?
                    if component["effectiveness"] > 0:
                        print("    Adding shape {} to part {}".format(shape_name, name))
                        volume = volume.add(shape)
                    else:
                        print(
                            "    Removing shape {} from part {}".format(
                                shape_name, name
                            )
                        )
                        volume = volume.remove(shape)

                self.parts[name]["volume"] = volume

            except Exception as E:
                print(E)
                self.warnings.append("Error compiling part {}".format(name) + str(E))

    @property
    def volumes(self):
        for part in self.parts.values():
            if "volume" in part:
                yield part["volume"]
            else:
                print("No volume for part {}".format(part["name"]))

    def read_header(self):
        # read till HULL

        self.data["name"] = self.lines.pop(0)

        next = self.lines.pop(0)

        # check if next starts with a digit
        if next[0].isdigit():
            self.data["reference"] = next
            next = self.lines.pop(0)

        while True:
            if next.startswith("*"):
                self.lines.insert(0, next)
                break

            if next.startswith("L:"):
                self.data["overall length"] = next[2:].strip()
            elif next.startswith("W:"):
                self.data["overall width"] = next[2:].strip()
            elif next.startswith("P:"):
                self.data["Units Preference"] = next[2:].strip()
            elif next.startswith("OL:"):
                self.data["Longitudinal origin plane description"] = next[3:].strip()
            elif next.startswith("OT:"):
                self.data["Transverse origin plane description"] = next[3:].strip()
            elif next.startswith("OV:"):
                self.data["Vertical origin plane description"] = next[3:].strip()
            elif next.startswith("N:"):
                self.data["Number of part records"] = next[2:].strip()
            else:
                print(f"ignored: {next}")

            next = self.lines.pop(0)

        return

    def read_shape_record(self):
        """
        Reads a shape record and adds the created volume into shape_outside['name'] as well as shape_inside['name']

        - property tables are ignored

            4th shape line: The first line of the first section.
                The section format is:
                        Location, m
                        Point 1
                        ...
                        Point m


        Shapes

        The shape data structure represents the solid model of some element of the vessel such as, for example, the hull, a skeg or a tank. The solid is represented as a discrete series of slices or planes all parallel to one another. It is assumed that the spacing between these slices (which may vary) is greater than 0.01 and small enough that all important aspects of the solid are adequately represented by the slices. The orientation of these planes is always normal to the longitudinal axis of the overall model.

        At each slice or "section" of the solid shape is a closed curve representing the complete outline of the intersection of the solid with the cross-sectioning plane. Each curve is represented as an ordered series of points where either a straight line or circular arc connects points. The first and last points are always connected by a straight line.

        The vertical axis is recognized as a possible line of symmetry, and the shape data structure takes advantage of this kind of symmetry by allowing the portion of a symmetrical curve that would be on the negative side (to the left of the vertical axis) to be omitted but still implied.

        When a sectional curve is viewed with the positive transverse axis to the right and the positive vertical axis upwards, the progression of points is always such that the area enclosed in going from the first to the last point is positive.

        The format of each shape record in the ASCII Geometry File is:
                    *
                    Shape name
                    n
                    Section 1
                    ...
                    Section n
                    Shell thicknesses
                    Property table

        1st shape line: One asterisk. This must be the only character on the line.

        2nd shape line: The shape name (e.g. HULL). The shape name must be the only thing on this line and there must be no leading or trailing blanks. Only letters and digits may be used, and letters should be upper case (except for the shape names automatically assigned that are of no concern to the user, which may include lower-case letters). Its length must not exceed 8 characters. No two shapes may have the same name within the same Geometry File.

        3rd shape line: An integer n where 1 < n < 256 giving the number of sections comprising the shape.

        4th shape line: The first line of the first section.

        The section format is:
                    Location, m
                    Point 1
                    ...
                    Point m

        1st section line: The section's longitudinal location and number of points on the section. Longitudinal locations may be relative to any convenient origin (different shapes may use different origins). The sections must be arranged in ascending order of their longitudinal locations. A section must have at least one point and less than 256 points.

        2nd section line: The first point of the section. Points must be arranged in sequence so that going from point 1 to point 2 ... to point m results in a counterclockwise traversal of the section curve in a plane where the positive transverse axis is to the right and the positive vertical axis us upward.

        The point format is:

             Trans, Vert [, Surface code, Radius, Line code]

        Trans is the transverse coordinate of the point relative to the shape's origin.

        Vert is the vertical coordinate of the point relative to the shape's origin.

        The remaining three items on the point line are optional. If the values of all three are zero or blank, they may be omitted along with the preceding comma.

        Surface code is a single digit from 0 to 3. It indicates the wettable/covered and shell/no-shell status of the line segment between the point it is attached to and the next point:
                  Surface code        Segment Covered?      Shell Gap Present?
                       0                    No                      No
                       1                    Yes                     No
                       2                    No                      Yes
                       3                    Yes                     Yes

        Surface code 2 is a special case used to indicate portions of a section curve which are not on the surface of the actual shape. Surface codes may be ignored in some programs.

        Radius, if present and not zero, is the radius of the arc connecting this point and neighboring points having exactly the same radius value. The distance between these points should be sufficiently small compared to the radius that straight lines connecting the same points would be an acceptable approximation to the curve. If the center of curvature of the arc is to the right when looking from the point to the next point (with the same radius), the radius number should be negative. The presence of the radius allows programs that recognize it to store the curve in a more compact form while programs that do not recognize the radius can treat the connections between points as linear with acceptable accuracy.

        Line code is a short alphabetical string identifying a longitudinal line such a chine or knuckle. The only line code fully supported is "DK" which marks the point at the deck edge.

        Shell thicknesses indicate the cumulative history of incremental expansions (positive) or contractions (negative) of the sectional outlines in a direction normal to the outline curve in the sectional plane and applying to the bottom, sides and top of every sectional curve on the shape. If omitted, all three thicknesses are assumed to be zero. If present, all three numbers must be present in the following sequence:

             Bottom, Sides, Top

        Zero shell thickness implies that the outlines are to the inside of any shell. A nonzero shell thickness means that the shell is included within the shape and that the interior space of the body it represents can be deduced by contracting the sectional outlines by the amounts of the shell thicknesses.
        In the absence of Line codes defining the transition from bottom to side and side to top, the bottom of each sectional curve extends to the point where the slope passes through 1.0; the top begins where the magnitude of the slope becomes less than 0.25.

        Property table is an optional data structure that contains formal properties of the portions of the shape below a series of horizontal planes. Its purpose is to provide alternate "Calibrated" properties that cannot be derived from the foregoing geometry. The format of this table is:
                    PROP, n
                    Height 1, Props 1
                    ...
                    Height n, Props n

        1st property table line: The keyword "PROP" followed by n, the number of rows in the property table.

        Other property table lines: Height, the vertical offset a "waterplane" normal to the vertical axis; Props, the properties of the portion of the solid below the waterplane. The format of the properties is:

             Volume, LCV, TCV, VCV, Area, LCA, TCA, CML, CMT

        Volume is the volume of the solid below the waterplane in cubic feet.

        LCV, TCV, VCV are the longitudinal, transverse and vertical coordinates of the centroid of the volume below the waterplane, in feet.

        Area is the area of the waterplane's intersection with the shape, in square feet.

        LCA, TCA are the center of the waterplane area, in feet.

        CML, CMT are the longitudinal and transverse moments of inertia of the waterplane area about its own center divided by the volume, in feet.

        The rows in the table must be arranged such that the height increases monotonically. The height should range such that the volume goes from zero to the full volume of the shape.

        A shape definition must appear before any of the component definitions that refer to it.

        """
        data = dict()

        lines = self.lines  # alias (by reference)

        name = lines.pop(0).strip()
        n = int(lines.pop(0))

        vertices = []

        hull_data = []  # autocompleted
        hull_data_raw = []  # raw data
        radius = -1
        previous_radius = -1

        # read sections
        for i in range(n):
            """The section format is:
            Location, m
            Point 1
            ...
            Point m

            """
            section = dict()
            location, m = lines.pop(0).split(",")
            section["location"] = float(location)

            print(f"Location = {location}")

            as_points = []

            # y_at_zero = False # to check for symmetry

            for j in range(int(m)):
                point_line = lines.pop(0)

                parts = point_line.split(",")
                y = float(parts[0])
                z = float(parts[1])

                if len(parts) >= 3:
                    surface_code = int(parts[2])
                if len(parts) >= 4:
                    if parts[3] == "0.\n":
                        radius = 0
                    else:
                        radius = int(parts[3])
                else:
                    radius = -1
                if len(parts) >= 5:
                    line_code = parts[4]

                if radius > 0 and radius == previous_radius:
                    # create arc
                    px = as_points[-2]
                    py = as_points[-1]
                    cx = y * 0.3048
                    cy = z * 0.3048
                    r = radius * 0.3048

                    points = points_on_circle(
                        p1=(px, py),
                        p2=(cx, cy),
                        radius=r,
                        max_angle_deg=self.circular_segments_step,
                    )

                    for p in points[1:-1]:  # skip the endpoints
                        as_points.append(p[0])
                        as_points.append(p[1])

                previous_radius = radius

                as_points.append(y * 0.3048)
                as_points.append(z * 0.3048)

                if y == 0:
                    y_at_zero = True

            print(f"Number of coordinates = {len(as_points)}")

            f = Frame(*as_points)

            # check if auto-completion is needed
            # Checking first and last point is not a solution
            # checking if any point is on y=0 ?
            #
            # if y_at_zero:
            #     if as_points[-1] == as_points[1] and as_points[-2] == as_points[0]:
            #         # curve is already closed
            #         print(f'Frame for shape {name} is already closed, not autocompleting')
            #         pass
            #     else:
            #         f = f.autocomplete()

            hull_data.append(float(location) * 0.3048)
            hull_data.append(f.autocomplete())

            hull_data_raw.append(float(location) * 0.3048)
            hull_data_raw.append(f)

        data["thickness"] = [float(x) for x in lines.pop(0).split(",")]

        # check for property table
        # and then ignore it
        if lines[0].startswith("PROP"):
            n = int(lines.pop(0).split(",")[1])

            for i in range(n):
                print("Skipping property table line : ", lines[0])
                lines.pop(0)  # skip property table

        if hull_data:
            self.shapes_outside[name] = Hull(
                *hull_data
            )  # this is the outside of the hull
            try:
                self.shapes_raw[name] = Hull(*hull_data_raw)  # raw (not autocompleted)
            except ValueError:
                self.warnings.append("Can not create raw shape for %s" % name)
                self.shapes_raw[name] = None
        else:
            self.warnings.append("No hull data found for %s" % name)

        # calculate the inside (due to thickness)
        if any(data["thickness"]):  # any thickness not equal to zero
            Bottom = data["thickness"][0]
            Sides = data["thickness"][1]
            Top = data["thickness"][2]

            # raise ValueError("I do not know how what this data would look like")
            # well, apparently it is only a single line

            # offset the shape and use boolean operations to create the inside
            original: Volume = self.shapes_outside[name]
            side1 = original.move(y=-Sides)
            side2 = original.move(y=Sides)
            bottom = original.move(z=Bottom)
            top = original.move(z=-Top)

            # create the inside
            self.shapes_inside[name] = (
                side1.inside_of(side2).inside_of(bottom).inside_of(top)
            )

        else:  # just the same
            self.shapes_inside[name] = self.shapes_outside[name]

    def read_component(self):
        """
        Reads components into self.components


            Components

        The component data structure gives further definition to a shape by locating it relative to the ship's overall origin and assigning it an effectiveness factor. It also provides symmetry information for proper interpretation of the section curves. Note that more than one component may use the same shape.

        Component format:
                    **
                    Component name
                    Side
                    Effectiveness
                    Shape origin shift
                    Shape name
                    Margins (optional)

        1st component line: two asterisks. These must be the only characters on the line.

        2nd component line: the component name (e.g. HULL). The component name must be the only thing on this line and there must be no leading or trailing blanks.
                            Only upper case letters and digits, periods and hyphens should be used. (Lower case letters may be used for component names that are of no concern to the user.)
                            Its length must not exceed 14 characters including any suffix denoting side.
                            The suffix, if present, may be in one of two forms:
                            1) of the form ".P", ".C", or ".S" which correspond, respectively, with -1, 0 and 1 values of the "side factor" on the next line; or
                            2) "-n" where n must be "0" if the side factor is zero, even if the side factor is negative, and odd if the side factor is positive.

        3rd component line: the side factor is an integer which must be -1, 0 or 1.
                            If the component is fully described by the referenced shape data, the side factor is 1.
                            If the component is as described by the shape data except that the shape's transverse coordinates are to be negated (moved to the opposite side) the side factor is -1.
                            If only half of the component is described by the shape data (the other half being described by reflecting the transverse coordinates about the shape's origin),
                                the side factor is 0.

        IGNORED
        4th component line: effectiveness is a factor which multiplies the volume and waterplane area of the component.
                            It should be a real number in the range negative 1.0 to positive 1.0.
                            If the component represents a tank or compartment where a permeability factor is to be used, the effectiveness is the permeability.
                            Components which represent buoyant or windage structures normally have an effectiveness of 1.0,
                             but in cases where the detail of structure is represented by a simpler enveloping surface,
                             the effective volume would be less than the volume of the envelope, thereby requiring a lesser effectiveness factor.
                             A negative effectiveness factor may be used to deduct the volume of a component when it is representing a void within a part.

        5th component line: the shape's origin shift is a vector (longitudinal, transverse, vertical coordinates) representing the shift of the origin to which the shape data is referred,
                            relative to the overall vessel origin. For example, if the shape data for a skeg is referred to a local origin at the skeg's centerline
                             -- which is 9 feet from the ship's centerline -- and to the forward end of the skeg -- which is 40 feet aft of the ship's longitudinal
                             origin -- the component origin shift would be 40,9,0.

        6th component line: the name of the shape representing this component. The shape data structure must precede the component data which refers to it.

        IGNORED
        7th (optional) component line: three numbers representing freeboard margins relative to the deck edge.
                            The first number applies to the forwardmost (least) section location and the last number applies to the aftmost (greatest) section location.
                            The middle number applies to a location midway between the other two. (The margin distance at other locations is derived by parabolic interpolation.)

        No two components belonging to the same part may have the same name. Two components may have the same name provided only one of them precedes the part to which it belongs
                            (see the part data structure description, below).


        """

        lines = self.lines  # alias by reference

        name = lines.pop(0).strip()
        suffix = name[-2:]

        # side factor is only defined when suffix is not present?
        if suffix in [".P", ".C", ".S"]:
            if suffix == ".P":
                side = -1
            elif suffix == ".C":
                side = 0
            elif suffix == ".S":
                side = 1
        elif suffix in ["-0", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9"]:
            raise ValueError("No idea what to do with this - need example")
        else:
            side = 0  # int(lines.pop(0).strip())

        side_factor = int(lines.pop(0).strip())
        effectiveness = float(lines.pop(0).strip())
        origin_shift = [float(x) * 0.3048 for x in lines.pop(0).strip().split(",")]
        shape_name = lines.pop(0).strip()

        if not lines[0].startswith("*"):
            margins = [float(x) for x in lines.pop(0).strip().split(",")]
        else:
            margins = None

        self.components[name] = {
            "name": name,
            "suffix": suffix,
            "side": side,
            "side_factor": side_factor,
            "effectiveness": effectiveness,
            "origin_shift": origin_shift,
            "shape_name": shape_name,
            "margins": margins,
        }

        print(
            "read component",
            name,
            suffix,
            side,
            effectiveness,
            origin_shift,
            shape_name,
            margins,
        )

    def read_part(self):
        lines = self.lines  # alias by ref

        parts = lines.pop(0).split("\\")
        name = parts[0].strip()
        if len(parts) > 1:
            part_description = parts[1].strip()
        else:
            part_description = None

        fluid_name = lines.pop(0).strip()

        part_type = int(lines.pop(0).strip())
        """
        
            1 - Displacement part (e.g. HULL including appendages)
            4 - Containment part  (e.g. a tank or compartment)
           10 - Sail (windage) part (e.g. non-watertight superstructure)
        """

        specific_gravity = float(lines.pop(0).strip())
        # as fraction of fresh water density

        reference_point = [float(x) for x in lines.pop(0).strip().split(",")]

        n_components = int(lines.pop(0).strip())

        components = []
        for i in range(n_components):
            component_name = lines.pop(0).strip()
            components.append(component_name)

        # sounding tubes and correction factors
        # ignored

        while not lines[0].startswith("*"):
            lines.pop(0)

        self.parts[name] = {
            "name": name,
            "part_description": part_description,
            "fluid_name": fluid_name,
            "part_type": part_type,
            "specific_gravity": specific_gravity,
            "reference_point": reference_point,
            "components": components,
        }

        print(
            "read part",
            name,
            part_description,
            fluid_name,
            part_type,
            specific_gravity,
            reference_point,
            n_components,
        )
