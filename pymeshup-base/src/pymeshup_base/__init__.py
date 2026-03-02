from __future__ import annotations

import sys
import importlib
from typing import TYPE_CHECKING

if sys.version_info[:2] >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:  # pragma: no cover
    from importlib_metadata import PackageNotFoundError, version  # type: ignore[assignment]

try:
    dist_name = "pymeshup-base"
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

__all__ = [
    "Frame",
    "Volume",
    "Box",
    "Cylinder",
    "Plot",
    "Load",
    "Hull",
    "GHSgeo",
    "STEP",
    "__version__",
]

if TYPE_CHECKING:  # pragma: no cover
    from .frames import Frame
    from .volumes import Volume, Box, Cylinder, Plot, Load
    from .hull import Hull
    from .ghs_import import GHSgeo
    from .step_import import STEP

_def_map = {
    "Frame": (".frames", "Frame"),
    "Volume": (".volumes", "Volume"),
    "Box": (".volumes", "Box"),
    "Cylinder": (".volumes", "Cylinder"),
    "Plot": (".volumes", "Plot"),
    "Load": (".volumes", "Load"),
    "Hull": (".hull", "Hull"),
    "GHSgeo": (".ghs_import", "GHSgeo"),
    "STEP": (".step_import", "STEP"),
}


def __getattr__(name: str):
    """Lazy import of heavy submodules only when actually accessed."""
    try:
        mod_name, attr = _def_map[name]
    except KeyError as exc:
        raise AttributeError(name) from exc
    module = importlib.import_module(mod_name, __name__)
    return getattr(module, attr)


def __dir__():
    return sorted(__all__)
