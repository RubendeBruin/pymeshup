# Contributing to `pymeshup`

This guide assumes you are using **uv** to manage your Python environment.
Adapt accordingly if you are using **conda** or plain **pip**.

## Preparing your repository

1. **Fork on GitHub** to your own account: `github.com/<YourLogin>/pymeshup.git`

2. **Clone the repository**

   ```bash
   git clone git@github.com:YourLogin/pymeshup.git
   cd pymeshup
   ```

3. **Create a virtual environment**

   ```bash
   uv venv -p 3.12
   ```

4. **Activate the virtual environment**

   ```bash
   # Linux / macOS
   source .venv/bin/activate

   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   ```

5. **Synchronize your virtual environment**

   ```bash
   uv sync --dev
   ```

   This installs all the packages, including the onces needed for development.

6. **Install the project in editable mode (with extras for testing/dev)**

   ```bash
   uv pip install -e . --no-deps
   ```

---

## Linux runtime requirements (PyMeshLab booleans)

Some tests use PyMeshLab boolean filters (union/intersection). These require the
system library **GMP** to be present at runtime:

- **Debian/Ubuntu**: `sudo apt install libgmp10` (or `libgmp-dev`)
- **Fedora/RHEL**: `sudo dnf install gmp` (or `gmp-devel`)
- **Arch/Manjaro**: `sudo pacman -S gmp`
- **openSUSE**: `sudo zypper install gmp`
- **NixOS**: run tests inside a shell that includes `gmp`
  (e.g. `nix-shell -p gmp --run "pytest"`)

If `gmp` is missing you’ll see plugin load errors like:

```shell
libfilter_mesh_booleans.so: (... libgmp.so.10: cannot open shared object file ...)
```

### Headless test defaults

We run tests headless by default. You can enforce this if needed:

```bash
export QT_QPA_PLATFORM=offscreen
export MPLBACKEND=Agg
pytest -q
```

For interactive GUI tests:

```bash
export PYMESHUP_GUI_INTERACTIVE=1
export QT_QPA_PLATFORM=xcb
export MPLBACKEND=QtAgg
pytest -m interactive -q
```

### Quick self-check

To verify your environment can load boolean filters:

```bash
python - <<'PY'
import pymeshlab as ml, inspect
ms = ml.MeshSet()
print("pymeshlab:", getattr(ml,'__version__','?'), ml.__file__)
print("has boolean union?:", hasattr(ms, "generate_boolean_union"))
PY
```

If this prints `True`, your GMP/boolean setup is OK.

---

### Configure pre-commit

`pre-commit` is already included in the `dev` group of dependencies and will be
installed automatically via:

```bash
uv sync --dev
```

To enable it for your local Git repo, run:

```bash
pre-commit install
```

This adds a Git hook so checks are automatically run before every commit.

### Run pre-commit manually (optional)

To apply all checks all files once:

```bash
pre-commit run --all-files
```

---

## Running tests

The project is configured with `pytest`. From your activated virtual environment:

- **Quick test run (default)** — interactive tests are skipped by default per `pyproject.toml`:

  ```bash
  pytest -q
  # or, using uv to ensure deps:
  uv run pytest -q
  ```

- **Run only interactive tests**

  ```bash
  pytest -q -m interactive
  ```

- **Run everything including interactive tests**:

  ```bash
  pytest -q -m "interactive or not interactive"
  # or simply re-specify to include all
  pytest -q -m ""
  ```

- **Measure coverage** (example):

  ```bash
  pytest --cov --cov-report=term-missing
  ```

Pytest markers are defined in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = ["-m", "not interactive", "-p", "no:cov"]
markers = [
    "interactive: mark tests as interactive (skipped by default)",
]
testpaths = ["tests"]
norecursedirs = ["dist", "build", ".tox"]
```

---

## Build intructions

### Building the GUI executable with PyInstaller

We provide a spec file: **`PyMeshupGUI.spec`**. To build the executable:

1. **Install PyInstaller (inside your venv)**

   ```bash
   uv pip install pyinstaller
   ```

2. **Run PyInstaller with the spec file**

   ```bash
   pyinstaller PyMeshupGUI.spec
   ```

3. **Copy the `casadi` package**

   The `casadi` package does not get complete included correctly in the pyinstaller-directory.
   To fix this, you need to copy it manually.
   - In linux do

     ```bash
         rsync -arv .venv/lib/python3.12/site-packages/casadi                  dist/PyMeshupGUI/_internal
     ```

   - In Windows do

     ```powershell
         RoboCopy.exe .venv/Lib/site-packages/casadi                       dist/PyMeshupGUI/_internal
     ```

4. **Find the output**
   - Executable & runtime files will be under `dist/PyMeshupGUI/`.
   - Logs appear in the terminal; build artifacts and caches go under `build/`.

5. **Run the built app**

   ```bash
   # On Linux/macOS
   ./dist/PyMeshupGUI/PyMeshupGUI

   # On Windows
   .\dist\PyMeshupGUI\PyMeshupGUI.exe
   ```

### Linux (NixOS) — Force X11 (avoid Wayland)

Use X11 for stable Qt/VTK/PyMeshLab behavior.

```bash
# .envrc (direnv) — force X11 and safe Matplotlib backend
export QT_QPA_PLATFORM=xcb           # Force X11 instead of Wayland
export QT_XCB_GL_INTEGRATION=glx     # Helps on NVIDIA
export MPLBACKEND=Agg                # Headless Matplotlib by default

# Optional: auto-activate venv
if [ -d .venv ]; then
  source .venv/bin/activate
else
  echo ".venv is missing – create it with 'uv venv' or 'python -m venv .venv'"
fi
```

> Tip: run `direnv allow` after creating or editing `.envrc`.

---

### VS Code — Match the terminal environment

Create a `.env` file in your project root and let VS Code load it.

```text
# .env (English comments)
QT_QPA_PLATFORM=xcb
QT_XCB_GL_INTEGRATION=glx
MPLBACKEND=Agg

# Toggle interactive GUI tests (see below)
PYMESHUP_GUI_INTERACTIVE=1
```

Minimal `/.vscode/settings.json`:

```json
{
  "python.envFile": "${workspaceFolder}/.env",
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestPath": "${workspaceFolder}/.venv/bin/pytest",
  "python.testing.cwd": "${workspaceFolder}",
  "python.testing.pytestArgs": ["tests"],
  "python.testing.autoTestDiscoverOnSaveEnabled": false,
  "[yaml]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "[markdown]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "[json]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "prettier.prettierPath": "./node_modules/prettier",
  "prettier.useEditorConfig": true
}
```

---

### Interactive tests (GUI windows)

- **Default (non-interactive)**: Matplotlib uses `Agg`, Qt runs `offscreen`, no windows.
- **Enable interactive mode** (manual runs):

```bash
# Linux terminal
export PYMESHUP_GUI_INTERACTIVE=1     # or: export INTERACTIVE=1
export QT_QPA_PLATFORM=xcb
export QT_XCB_GL_INTEGRATION=glx
export MPLBACKEND=QtAgg

pytest -m interactive -q
```

> In VS Code: set the same variables in `.env` and run tests via the Test Explorer.

- **Pytest configuration (`conftest.py`)**: interactive tests are skipped unless
  `PYMESHUP_GUI_INTERACTIVE=1` (or `INTERACTIVE=1`) is set.
  You don’t need both a marker and an env var:
  - Use no options → interactive tests skipped.
  - Use `-m interactive` and `INTERACTIVE=1` → run only the interactive subset.

---

### Windows notes

```powershell
# PowerShell — clean PyInstaller build
Remove-Item -Recurse -Force build, dist
pyinstaller .\PyMeshupGUI.spec
```

- Ensure Qt plugins and extra data are included via the `.spec` file.
- Verify Visual C++ Redistributable and GPU drivers if the GUI fails to start.

---

### Troubleshooting

- **Check which PyMeshLab/Qt/vars are active** (must match between terminal and VSCode):

```bash
python - << 'PY'
import sys, os, pymeshlab
from pymeshlab import MeshSet
ms = MeshSet()
print("Python:", sys.executable)
print("PyMeshLab:", pymeshlab.__version__, pymeshlab.__file__)
print("QT_QPA_PLATFORM:", os.environ.get("QT_QPA_PLATFORM"))
print("MPLBACKEND:", os.environ.get("MPLBACKEND"))
print("has generate_boolean_union?:", hasattr(ms, "generate_boolean_union"))
PY
```

- **After dependency or backend changes**: always perform a clean PyInstaller build.
- **Wayland issues**: explicitly set `QT_QPA_PLATFORM=xcb` in both terminal and VSCode.

---

### Optional Makefile targets

```make
run-tests:
    @pytest -q

run-tests-interactive:
    @PYMESHUP_GUI_INTERACTIVE=1 QT_QPA_PLATFORM=xcb \
    QT_XCB_GL_INTEGRATION=glx MPLBACKEND=QtAgg \
    pytest -m interactive -q
```
