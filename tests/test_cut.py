import pytest

from pymeshup import Box, Plot


@pytest.mark.interactive
def test_cut():
    a = Box()
    a = a.cut_at_xz()

    Plot(a)
