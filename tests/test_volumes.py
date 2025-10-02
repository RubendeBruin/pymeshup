import pytest
from pathlib import Path
from pymeshup import Box, Cylinder, Plot, Load

HERE = Path(__file__).parent  # folder waarin dit testbestand staat


def test_crop():
    a = Box()
    a.crop(xmax=0)


@pytest.mark.interactive
def test_add():
    a = Box()
    c = Cylinder()

    p = a.add(c)

    Plot(p)


@pytest.mark.interactive
def test_load():
    a = Load(HERE / "cheetah.obj")
    Plot(a)
