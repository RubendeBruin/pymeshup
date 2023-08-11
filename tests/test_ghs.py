from pymeshup import *

def test_read_ghs():
    a =read_ghs_file(r"C:\data\Dave\Public\pymeshup\src\pymeshup\gui\examples\DEMOBARGE.GF1")
    Plot(a)

