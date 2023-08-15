from pymeshup import *

"""

        Er gaat nog iets mis met de Tank7 PS en SB, die gaan beiden over de hele breedte van de bak.
        En dus iets met de skeggen


"""

"""Trick to get volumes as variables:

for part in a.parts.keys():
	name = part.replace('.','_')
	exec(f'{name} = a.parts["{part}"]["volume"]')

"""

def test_read_ghs():
    a =GHSgeo(r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE.GF1", circular_segments_step=1)
    Plot(a.shapes_outside.values())

if __name__ == '__main__':
    filename = r"C:\Users\beneden\Jottacloud\RdBr\HEBO\assets\P56\in\GHS P55\GF\HEBO-P55.GF1"
    # filename = r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE_SPUD.GF1"
    a = GHSgeo(filename, circular_segments_step=10)

    # shapes = [_ for _ in a.shapes_outside.values()]
    # Plot(shapes)

    # print(a.warnings)
    #
    parts = []
    for part in a.parts.values():
        parts.append(part['volume'])

    Plot(parts)

    # Plot(a.parts['HULL']['volume'])
    # # Plot(a.shapes_outside['s2'])

