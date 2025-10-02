from pymeshup import Box


def test_regrid_box():
    a = Box()
    b = a.regrid(pct=2)
    _c = b.merge_close_vertices(pct=1)


def test_cut_at_waterline():
    a = Box().move(-0.5)
    _b = a.cut_at_waterline()
