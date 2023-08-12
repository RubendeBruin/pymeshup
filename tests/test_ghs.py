from pymeshup import *

def test_read_ghs():
    a =GHSgeo(r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE.GF1")
    Plot(a.shapes.values())

if __name__ == '__main__':
    filename = r"C:\Users\beneden\Jottacloud\RdBr\HEBO\assets\P56\in\GHS P55\GF\HEBO-P55 - kopie.GF1"
    a = GHSgeo(filename)

    print(a.warnings)

    Plot(a.shapes.values())