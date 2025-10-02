from __future__ import annotations

import gc
import os
import sys
from pathlib import Path
import pytest


def _is_truthy(name: str) -> bool:
    """Return True if the given env var is set to a truthy value."""
    return os.environ.get(name, "").strip().lower() in {"1", "true", "yes", "on"}


# Default is True, override to False with INTERACTIVE=0
val = os.environ.get("PYMESHUP_GUI_INTERACTIVE") or os.environ.get("INTERACTIVE")
if val is None:
    INTERACTIVE = True  # default ON
else:
    INTERACTIVE = str(val).strip().lower() in {"1", "true", "yes", "on"}


# Set GUI/backends BEFORE first Qt/Matplotlib import
if INTERACTIVE:
    # Force GUI backends
    os.environ["MPLBACKEND"] = "QtAgg"
    # Ensure we are not in offscreen mode
    if os.environ.get("QT_QPA_PLATFORM", "").lower() == "offscreen":
        os.environ.pop("QT_QPA_PLATFORM", None)
else:
    os.environ.setdefault("MPLBACKEND", "Agg")
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


def pytest_sessionstart(session):
    pm = session.config.pluginmanager
    names = sorted(getattr(p, "__name__", type(p).__name__) for p in pm.get_plugins())
    print("INTERACTIVE =", INTERACTIVE)
    print(
        "PYMESHUP_GUI_INTERACTIVE_RAW =",
        repr(os.environ.get("PYMESHUP_GUI_INTERACTIVE")),
    )
    print("INTERACTIVE_RAW =", repr(os.environ.get("INTERACTIVE")))
    print("MPLBACKEND =", os.environ.get("MPLBACKEND"))
    print("QT_QPA_PLATFORM =", os.environ.get("QT_QPA_PLATFORM"))
    print(
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD =",
        os.environ.get("PYTEST_DISABLE_PLUGIN_AUTOLOAD"),
    )
    print(
        "LOADED_PLUGINS =",
        [n for n in names if "pytest" in n or "cov" in n or "vscode" in n],
    )
    assert not any(
        "cov" in n.lower() for n in names
    ), f"pytest-cov is loaded in VS Code: {names}"


@pytest.fixture(scope="session", autouse=True)
def _qt_app():
    try:
        from PySide6.QtWidgets import QApplication
    except Exception:
        yield None
        return
    app = QApplication.instance() or QApplication([])
    try:
        yield app
    finally:
        try:
            app.quit()
        except Exception:
            pass
        gc.collect()


def pytest_sessionfinish(session, exitstatus):
    env_hard_exit = os.environ.get("PYTEST_HARD_EXIT", "").lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    flag_hard_exit = (
        session.config.getoption("--hard-exit") if session is not None else False
    )
    hard_exit = env_hard_exit or flag_hard_exit
    if hard_exit:
        try:
            sys.stdout.flush()
            sys.stderr.flush()
        finally:
            os._exit(exitstatus)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--hard-exit",
        action="store_true",
        default=False,
        help="Force hard exit after tests.",
    )


@pytest.fixture
def assets_dir() -> Path:
    return Path(__file__).parent / "assets_for_tests"


def pytest_configure(config: pytest.Config) -> None:
    # Register the marker so pytest doesn't warn
    config.addinivalue_line("markers", "interactive: tests that open real GUI windows")


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    # If not in interactive mode, skip tests marked with @pytest.mark.interactive
    if INTERACTIVE:
        return
    skip_it = pytest.mark.skip(
        reason="Set PYMESHUP_GUI_INTERACTIVE=1 or INTERACTIVE=1 to run interactive GUI tests"
    )
    for item in items:
        if "interactive" in item.keywords:
            item.add_marker(skip_it)
