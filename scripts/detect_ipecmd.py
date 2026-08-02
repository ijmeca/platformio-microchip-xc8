"""Discovery and command helpers for MPLAB IPE and PICkit 3."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Tuple


IPECMD_EXECUTABLES = ("ipecmd.exe", "ipecmd.sh", "ipecmd")
LAST_PICKIT3_IPECMD_VERSION = (6, 20)


def semantic_version_key(value: object) -> Tuple[int, ...]:
    matches = re.findall(r"(?<![A-Za-z0-9])v?(\d+(?:\.\d+)+)", str(value))
    if not matches:
        return (0,)
    return tuple(int(part) for part in matches[-1].split("."))


def supports_pickit3(installation: Mapping[str, str]) -> bool:
    version = semantic_version_key(installation.get("version", ""))
    return version == (0,) or version <= LAST_PICKIT3_IPECMD_VERSION


def normalize_ipecmd_path(value: object) -> Optional[Dict[str, str]]:
    if value is None or not str(value).strip():
        return None

    base = Path(os.path.expandvars(str(value).strip())).expanduser()
    candidates = [base]
    for executable in IPECMD_EXECUTABLES:
        candidates.extend(
            (
                base / executable,
                base / "mplab_platform" / "mplab_ipe" / executable,
                base / "mplab_platform" / "mplab_ipe" / "bin" / executable,
            )
        )

    for candidate in candidates:
        if not candidate.is_file() or not os.access(str(candidate), os.X_OK):
            continue
        executable_path = candidate.resolve()
        return {
            "executable": str(executable_path),
            "version": ".".join(
                str(part) for part in semantic_version_key(executable_path)
            ),
        }
    return None


def default_ipecmd_roots() -> List[Path]:
    roots = [
        Path("/Applications/microchip/mplabx"),
        Path("/opt/microchip/mplabx"),
        Path("/usr/local/microchip/mplabx"),
    ]
    for variable in ("ProgramFiles", "ProgramFiles(x86)"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value) / "Microchip" / "MPLABX")
    return roots


def _automatic_candidates(roots: Iterable[Path]) -> List[Path]:
    candidates = []
    for root in roots:
        if root.is_dir():
            for executable in IPECMD_EXECUTABLES:
                candidates.extend(
                    root.glob("v*/mplab_platform/mplab_ipe/%s" % executable)
                )
                candidates.extend(
                    root.glob("v*/mplab_platform/mplab_ipe/bin/%s" % executable)
                )
    return candidates


def find_ipecmd(
    custom_path: Optional[str] = None,
    environ: Optional[Mapping[str, str]] = None,
    path_lookup: Callable[[str], Optional[str]] = shutil.which,
    search_roots: Optional[Iterable[Path]] = None,
) -> Optional[Dict[str, str]]:
    environment = os.environ if environ is None else environ

    for value in (custom_path, environment.get("IPECMD_PATH")):
        if value:
            return normalize_ipecmd_path(value)

    for executable_name in IPECMD_EXECUTABLES:
        executable = path_lookup(executable_name)
        if executable:
            normalized = normalize_ipecmd_path(executable)
            if normalized and supports_pickit3(normalized):
                return normalized

    roots = default_ipecmd_roots() if search_roots is None else list(search_roots)
    installations = [
        item
        for item in (
            normalize_ipecmd_path(path) for path in _automatic_candidates(roots)
        )
        if item and supports_pickit3(item)
    ]
    if not installations:
        return None
    return max(installations, key=lambda item: semantic_version_key(item["version"]))


def pickit3_command(
    ipecmd: str, mcu: object, firmware_hex: object, extra_flags=()
) -> List[str]:
    device = str(mcu).strip().upper()
    if device.startswith("PIC"):
        device = device[3:]
    return [
        ipecmd,
        "-P%s" % device,
        "-TPPK3",
        "-F%s" % Path(firmware_hex),
        "-M",
    ] + [str(flag) for flag in extra_flags]
