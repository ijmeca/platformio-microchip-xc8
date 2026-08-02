"""Discovery and MCU-based selection of installed XC8 Device Family Packs."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


DEVICE_HEADER = re.compile(
    r"^pic((?:10f|12f|16f|18f)[a-z0-9]+)\.h$", re.IGNORECASE
)


def semantic_version_key(value: object) -> Tuple[int, ...]:
    matches = re.findall(r"(?<![A-Za-z0-9])(\d+(?:\.\d+)+)", str(value))
    if not matches:
        return (0,)
    return tuple(int(part) for part in matches[-1].split("."))


def normalize_mcu(mcu: object) -> str:
    value = str(mcu).strip().upper()
    return value[3:] if value.startswith("PIC") else value


def normalize_dfp_path(value: object) -> Optional[Path]:
    """Return the DFP's xc8 directory from common user-supplied forms."""
    if value is None or not str(value).strip():
        return None

    path = Path(os.path.expandvars(str(value).strip())).expanduser()
    candidates = [path, path / "xc8"]

    current = path
    while current != current.parent:
        if current.name.lower() == "xc8":
            candidates.append(current)
            break
        current = current.parent

    for candidate in candidates:
        if (candidate / "pic" / "include" / "proc").is_dir():
            return candidate.resolve()
    return None


def default_dfp_roots() -> List[Path]:
    home = Path.home()
    roots = [
        Path("/Applications/microchip/mplabx"),
        Path("/opt/microchip/mplabx"),
        Path("/usr/local/microchip/mplabx"),
        home / "Library" / "microchip" / "packs",
        home / ".mchp_packs",
    ]
    for variable in ("ProgramFiles", "ProgramFiles(x86)"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value) / "Microchip" / "MPLABX")
    user_profile = os.environ.get("USERPROFILE")
    if user_profile:
        roots.append(Path(user_profile) / ".mchp_packs")
    return roots


def _pack_record(xc8_path: Path) -> Dict[str, str]:
    return {
        "dfp_path": str(xc8_path),
        "pack_name": xc8_path.parent.parent.name,
        "pack_version": xc8_path.parent.name,
    }


def _find_under_root(root: Path) -> List[Path]:
    if not root.is_dir():
        return []
    found = []
    for candidate in root.rglob("xc8"):
        if "_DFP" not in str(candidate.parent.parent.name).upper():
            continue
        normalized = normalize_dfp_path(candidate)
        if normalized:
            found.append(normalized)
    return found


def discover_dfps(
    custom_dfp_path: Optional[str] = None,
    custom_dfp_root: Optional[str] = None,
    search_roots: Optional[Iterable[Path]] = None,
) -> List[Path]:
    """Discover DFP xc8 directories in documented priority order."""
    if custom_dfp_path:
        normalized = normalize_dfp_path(custom_dfp_path)
        return [normalized] if normalized else []

    if custom_dfp_root:
        return _deduplicate(_find_under_root(Path(custom_dfp_root).expanduser()))

    roots = default_dfp_roots() if search_roots is None else list(search_roots)
    paths = []
    for root in roots:
        paths.extend(_find_under_root(root))
    return _deduplicate(paths)


def _deduplicate(paths: Iterable[Path]) -> List[Path]:
    unique = {str(path.resolve()): path.resolve() for path in paths}
    return list(unique.values())


def devices_in_dfp(dfp_path: Path) -> Dict[str, str]:
    normalized = normalize_dfp_path(dfp_path)
    if not normalized:
        return {}

    devices = {}
    headers = normalized / "pic" / "include" / "proc"
    for header in headers.iterdir():
        if not header.is_file():
            continue
        match = DEVICE_HEADER.match(header.name)
        if match:
            devices[match.group(1).upper()] = str(header.resolve())
    return devices


def build_device_index(dfp_paths: Iterable[Path]) -> Dict[str, Dict[str, str]]:
    """Build an in-memory MCU index, preferring the newest supporting pack."""
    index: Dict[str, Dict[str, str]] = {}
    for path in dfp_paths:
        normalized = normalize_dfp_path(path)
        if not normalized:
            continue
        pack = _pack_record(normalized)
        for device, header in devices_in_dfp(normalized).items():
            candidate = dict(pack)
            candidate["header"] = header
            current = index.get(device)
            if current is None or semantic_version_key(
                candidate["pack_version"]
            ) > semantic_version_key(current["pack_version"]):
                index[device] = candidate
    return index


def select_dfp_for_mcu(
    mcu: object, dfp_paths: Iterable[Path]
) -> Optional[Dict[str, str]]:
    return build_device_index(dfp_paths).get(normalize_mcu(mcu))
