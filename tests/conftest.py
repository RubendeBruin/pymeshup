from __future__ import annotations

import gc
import os
import sys
from pathlib import Path
import pytest


@pytest.fixture
def assets_dir() -> Path:
    return Path(__file__).parent / "assets_for_tests"

