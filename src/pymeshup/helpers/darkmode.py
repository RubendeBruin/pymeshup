# helpers/darkmode.py
from __future__ import annotations

import os
import sys
import subprocess
from configparser import ConfigParser
from pathlib import Path
from typing import Optional


def _win_is_dark() -> Optional[bool]:
    if sys.platform != "win32":
        return None
    try:
        import winreg  # stdlib on Windows

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        ) as key:
            val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return val == 0  # 0 = dark, 1 = light
    except OSError:
        return None


def _mac_is_dark() -> Optional[bool]:
    if sys.platform != "darwin":
        return None
    try:
        out = subprocess.check_output(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            stderr=subprocess.STDOUT,
            timeout=0.5,
            text=True,
        ).strip()
        return out.lower() == "dark"
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return None


def _linux_is_dark() -> Optional[bool]:
    if sys.platform != "linux":
        return None

    desktop = (os.environ.get("XDG_CURRENT_DESKTOP") or "").lower()
    session = (os.environ.get("DESKTOP_SESSION") or "").lower()

    if "gnome" in desktop or "gnome" in session:
        try:
            out = (
                subprocess.check_output(
                    ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                    stderr=subprocess.DEVNULL,
                    timeout=0.5,
                    text=True,
                )
                .strip()
                .strip("'")
                .strip('"')
                .lower()
            )
            if "prefer-dark" in out:
                return True
            if "prefer-light" in out or "default" in out:
                return False
        except Exception:
            pass

    if "kde" in desktop or "plasma" in session:
        kdeglobals = Path.home() / ".config" / "kdeglobals"
        if kdeglobals.is_file():
            try:
                cfg = ConfigParser()
                cfg.optionxform = str  # preserve case
                cfg.read(kdeglobals, encoding="utf-8")
                scheme = cfg.get("General", "ColorScheme", fallback="")
                if "dark" in scheme.lower():
                    return True
                win_bg = cfg.get("Colors:Window", "BackgroundNormal", fallback="")
                parts = [p.strip() for p in win_bg.split(",") if p.strip().isdigit()]
                if len(parts) == 3:
                    r, g, b = (int(x) for x in parts)
                    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
                    return luma < 96
            except Exception:
                pass

    gtk_theme = (os.environ.get("GTK_THEME") or "").lower()
    if gtk_theme.endswith("-dark") or ":dark" in gtk_theme:
        return True
    if gtk_theme.endswith("-light") or ":light" in gtk_theme:
        return False

    return None


def is_dark_mode() -> bool:
    override = os.environ.get("APP_FORCE_DARK")
    if override is not None:
        return override.strip() in {"1", "true", "True"}

    for probe in (_win_is_dark, _mac_is_dark, _linux_is_dark):
        val = probe()
        if val is not None:
            return bool(val)
    return False
