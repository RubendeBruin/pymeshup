"""
This script creates a Windows desktop shortcut (.url file) for the PyMeshUp application.

Function:
    create_url_shortcut():
        - Locates the paths to the PyMeshUp executable, application icon, and user's desktop.
        - Generates a .url shortcut file that launches the executable.
        - Assigns a custom icon to the shortcut.
        - Saves the shortcut file to the desktop.

Usage:
    Run this script directly to generate the shortcut on the user's desktop.
    
    python.exe make_desktop_launcher.py
"""

from pathlib import Path

def create_url_shortcut():
    # Determine paths
    base_dir = Path(__file__).resolve().parent
    exe_path = base_dir / ".venv" / "Scripts" / "pymeshup.exe"
    icon_path = base_dir / "src" / "pymeshup" / "resources" / "pymeshup_logo.ico"
    desktop_path = Path.home() / "Desktop"
    shortcut_path = desktop_path / "PyMeshUp.url"

    # Make the content of the .url file
    content = f"""[InternetShortcut]
URL=file:///{exe_path.as_posix()}
IconFile={icon_path.as_posix()}
IconIndex=0
"""

    # Write to the desktop
    shortcut_path.write_text(content)
    print(f"Shortcut created at: {shortcut_path}")

if __name__ == "__main__":
    create_url_shortcut()
