"""Discovery and command helpers for an external pk2cmd installation."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Callable, Dict, Mapping, Optional


PK2CMD_EXECUTABLES = ("pk2cmd.exe", "pk2cmd")


def normalize_pk2cmd_path(value: object) -> Optional[Dict[str, str]]:
    if value is None or not str(value).strip():
        return None

    base = Path(os.path.expandvars(str(value).strip())).expanduser()
    candidates = [base] if base.is_file() else [
        base / executable for executable in PK2CMD_EXECUTABLES
    ]
    for candidate in candidates:
        device_file = candidate.parent / "PK2DeviceFile.dat"
        if (
            candidate.is_file()
            and os.access(str(candidate), os.X_OK)
            and device_file.is_file()
        ):
            return {
                "executable": str(candidate.resolve()),
                "device_file": str(device_file.resolve()),
                "root": str(candidate.parent.resolve()),
            }
    return None


def find_pk2cmd(
    custom_path: Optional[str] = None,
    environ: Optional[Mapping[str, str]] = None,
    path_lookup: Callable[[str], Optional[str]] = shutil.which,
) -> Optional[Dict[str, str]]:
    environment = os.environ if environ is None else environ
    for value in (custom_path, environment.get("PK2CMD_PATH")):
        if value:
            return normalize_pk2cmd_path(value)

    for executable_name in PK2CMD_EXECUTABLES:
        executable = path_lookup(executable_name)
        if executable:
            installation = normalize_pk2cmd_path(executable)
            if installation:
                return installation
    return None


def pk2cmd_command(
    executable: object,
    mcu: object,
    firmware_hex: object,
    externally_powered: bool = False,
    extra_flags=(),
):
    device = str(mcu).strip().upper()
    if not device.startswith("PIC"):
        device = "PIC" + device
    command = [
        Path(executable).name,
        "-P%s" % device,
        "-F%s" % firmware_hex,
        "-M",
    ]
    if externally_powered:
        command.append("-W")
    return command + [str(flag) for flag in extra_flags]
