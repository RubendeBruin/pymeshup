"""
    Dummy conftest.py for pymeshup.

    If you don't know what this is for, just leave it empty.
    Read more about conftest.py under:
    - https://docs.pytest.org/en/stable/fixture.html
    - https://docs.pytest.org/en/stable/writing_plugins.html
"""
from pathlib import Path

import pytest


@pytest.fixture
def assets_dir() -> Path:
    """Returns the path to the assets directory for tests."""
    return Path(__file__).parent / "assets_for_tests"