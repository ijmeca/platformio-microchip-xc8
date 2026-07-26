"""Discovery and normalization helpers for externally installed MPLAB XC8."""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Tuple


XC8_EXECUTABLES = ("xc8-cc", "xc8-cc.exe")


def semantic_version_key(value: object) -> Tuple[int, ...]:
    """Return a numeric key suitable for Microchip dotted versions."""
    text = str(value)
    matches = re.findall(r"(?<![A-Za-z0-9])v?(\d+(?:\.\d+)+)", text)
    if not matches:
        return (0,)
    return tuple(int(part) for part in matches[-1].split("."))


def _version_from_path(path: Path) -> str:
    key = semantic_version_key(path)
    if key == (0,):
        return ""
    return ".".join(str(part) for part in key)


def normalize_xc8_path(value: object) -> Optional[Dict[str, str]]:
    """Normalize an XC8 installation root, bin directory, or compiler path."""
    if value is None or not str(value).strip():
        return None

    base = Path(os.path.expandvars(str(value).strip())).expanduser()
    candidates: List[Path] = [base]
    for executable in XC8_EXECUTABLES:
        candidates.extend((base / executable, base / "bin" / executable))

    for candidate in candidates:
        if not candidate.is_file() or not os.access(str(candidate), os.X_OK):
            continue

        executable_path = candidate.resolve()
        root = (
            executable_path.parent.parent
            if executable_path.parent.name.lower() == "bin"
            else executable_path.parent
        )
        return {
            "executable": str(executable_path),
            "root": str(root),
            "version": _version_from_path(executable_path),
        }
    return None


def default_xc8_roots() -> List[Path]:
    roots = [
        Path("/Applications/microchip/xc8"),
        Path("/opt/microchip/xc8"),
        Path("/usr/local/microchip/xc8"),
    ]
    for variable in ("ProgramFiles", "ProgramFiles(x86)"):
        value = os.environ.get(variable)
        if value:
            roots.append(Path(value) / "Microchip" / "xc8")
    return roots


def _automatic_candidates(roots: Iterable[Path]) -> List[Path]:
    candidates: List[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        for executable in XC8_EXECUTABLES:
            candidates.extend(root.glob("v*/bin/%s" % executable))
    return candidates


def _newest(paths: Iterable[Path]) -> Optional[Dict[str, str]]:
    installations = [
        normalized
        for normalized in (normalize_xc8_path(path) for path in paths)
        if normalized is not None
    ]
    if not installations:
        return None
    return max(
        installations,
        key=lambda item: semantic_version_key(item["version"]),
    )


def find_xc8(
    custom_path: Optional[str] = None,
    environ: Optional[Mapping[str, str]] = None,
    path_lookup: Callable[[str], Optional[str]] = shutil.which,
    search_roots: Optional[Iterable[Path]] = None,
) -> Optional[Dict[str, str]]:
    """Find XC8 in documented priority order."""
    environment = os.environ if environ is None else environ

    if custom_path:
        return normalize_xc8_path(custom_path)

    environment_path = environment.get("XC8_PATH")
    if environment_path:
        return normalize_xc8_path(environment_path)

    executable = path_lookup("xc8-cc")
    if executable:
        normalized = normalize_xc8_path(executable)
        if normalized:
            return normalized

    roots = default_xc8_roots() if search_roots is None else list(search_roots)
    return _newest(_automatic_candidates(roots))
