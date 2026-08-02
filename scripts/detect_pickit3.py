"""Discovery and command helpers for the standalone PICkit 3 application."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional


def normalize_pickit3_path(value: object) -> Optional[Dict[str, str]]:
    if value is None or not str(value).strip():
        return None

    base = Path(os.path.expandvars(str(value).strip())).expanduser()
    executable = base if base.is_file() else base / "PICkit3.exe"
    device_file = executable.parent / "PK2DeviceFile.dat"
    if not executable.is_file() or not device_file.is_file():
        return None
    return {
        "executable": str(executable.resolve()),
        "device_file": str(device_file.resolve()),
    }


def default_pickit3_roots(environ: Mapping[str, str]) -> Iterable[Path]:
    for variable in ("ProgramFiles(x86)", "ProgramFiles"):
        value = environ.get(variable)
        if value:
            yield Path(value) / "Microchip" / "PICkit 3 v3"


def find_pickit3(
    custom_path: Optional[str] = None,
    environ: Optional[Mapping[str, str]] = None,
    search_roots: Optional[Iterable[Path]] = None,
) -> Optional[Dict[str, str]]:
    environment = os.environ if environ is None else environ
    for value in (custom_path, environment.get("PICKIT3_PATH")):
        if value:
            return normalize_pickit3_path(value)

    roots = (
        default_pickit3_roots(environment)
        if search_roots is None
        else search_roots
    )
    for root in roots:
        installation = normalize_pickit3_path(root)
        if installation:
            return installation
    return None


def standalone_pickit3_command(
    uploader: object,
    application: object,
    device_file: object,
    mcu: object,
    firmware_hex: object,
):
    return [
        str(uploader),
        "--application",
        str(application),
        "--device-file",
        str(device_file),
        "--device",
        str(mcu).strip().upper().removeprefix("PIC"),
        "--hex",
        str(firmware_hex),
    ]
