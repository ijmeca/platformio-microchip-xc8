import stat
import tempfile
import unittest
from pathlib import Path

from scripts.detect_dfp import (
    build_device_index,
    devices_in_dfp,
    discover_dfps,
    normalize_dfp_path,
    select_dfp_for_mcu,
)
from scripts.detect_xc8 import (
    find_xc8,
    normalize_xc8_path,
    semantic_version_key,
)


def make_executable(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def make_dfp(root, name, version, devices):
    xc8 = root / "Microchip" / name / version / "xc8"
    proc = xc8 / "pic" / "include" / "proc"
    proc.mkdir(parents=True)
    for device in devices:
        (proc / ("pic%s.h" % device.lower())).touch()
    return xc8


class XC8DetectionTests(unittest.TestCase):
    def test_semantic_version_order(self):
        self.assertGreater(semantic_version_key("v3.10"), semantic_version_key("v3.9"))

    def test_normalizes_root_bin_and_executable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "xc8" / "v3.10"
            executable = make_executable(root / "bin" / "xc8-cc")
            for supplied in (root, root / "bin", executable):
                result = normalize_xc8_path(supplied)
                self.assertEqual(result["executable"], str(executable.resolve()))
                self.assertEqual(result["root"], str(root.resolve()))
                self.assertEqual(result["version"], "3.10")

    def test_respects_priority(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            custom = make_executable(root / "custom" / "v1.0" / "bin" / "xc8-cc")
            environment = make_executable(root / "env" / "v2.0" / "bin" / "xc8-cc")
            on_path = make_executable(root / "path" / "v3.0" / "bin" / "xc8-cc")
            result = find_xc8(
                custom_path=str(custom.parent.parent),
                environ={"XC8_PATH": str(environment)},
                path_lookup=lambda name: str(on_path),
                search_roots=[],
            )
            self.assertEqual(result["executable"], str(custom.resolve()))

    def test_selects_newest_automatic_installation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_executable(root / "v3.9" / "bin" / "xc8-cc")
            newest = make_executable(root / "v3.10" / "bin" / "xc8-cc")
            result = find_xc8(
                environ={},
                path_lookup=lambda name: None,
                search_roots=[root],
            )
            self.assertEqual(result["executable"], str(newest.resolve()))

    def test_environment_precedes_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            environment = make_executable(root / "env" / "v2.0" / "bin" / "xc8-cc")
            on_path = make_executable(root / "path" / "v3.0" / "bin" / "xc8-cc")
            result = find_xc8(
                environ={"XC8_PATH": str(environment.parent.parent)},
                path_lookup=lambda name: str(on_path),
                search_roots=[],
            )
            self.assertEqual(result["executable"], str(environment.resolve()))

    def test_path_precedes_automatic_search(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            on_path = make_executable(root / "path" / "v2.0" / "bin" / "xc8-cc")
            make_executable(root / "automatic" / "v3.0" / "bin" / "xc8-cc")
            result = find_xc8(
                environ={},
                path_lookup=lambda name: str(on_path),
                search_roots=[root / "automatic"],
            )
            self.assertEqual(result["executable"], str(on_path.resolve()))

    def test_returns_none_when_xc8_is_missing(self):
        self.assertIsNone(
            find_xc8(environ={}, path_lookup=lambda name: None, search_roots=[])
        )


class DFPDetectionTests(unittest.TestCase):
    def test_discovers_dfps_and_normalizes_xc8_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dfp = make_dfp(root, "PIC10-12Fxxx_DFP", "1.3.46", ["12f675"])
            self.assertEqual(normalize_dfp_path(dfp / "pic" / "include"), dfp.resolve())
            self.assertEqual(discover_dfps(custom_dfp_root=str(root)), [dfp.resolve()])

    def test_explicit_dfp_precedes_root_search(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            explicit = make_dfp(root / "explicit", "PIC16Fxxx_DFP", "1.0", ["16f877a"])
            make_dfp(root / "search", "PIC16Fxxx_DFP", "2.0", ["16f877a"])
            discovered = discover_dfps(
                custom_dfp_path=str(explicit),
                custom_dfp_root=str(root / "search"),
            )
            self.assertEqual(discovered, [explicit.resolve()])

    def test_identifies_only_device_headers(self):
        with tempfile.TemporaryDirectory() as temporary:
            dfp = make_dfp(
                Path(temporary),
                "PIC16Fxxx_DFP",
                "2.0.0",
                ["16f877a", "18f4550"],
            )
            proc = dfp / "pic" / "include" / "proc"
            (proc / "pic16f.h").touch()
            (proc / "legacy.h").touch()
            self.assertEqual(set(devices_in_dfp(dfp)), {"16F877A", "18F4550"})

    def test_selects_newest_pack_that_contains_mcu(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old = make_dfp(root, "PIC16Fxxx_DFP", "1.9", ["16f877a"])
            new = make_dfp(root, "PIC16Fxxx_DFP", "1.10", ["16f877a"])
            make_dfp(root, "OTHER_DFP", "9.0", ["18f4550"])
            selected = select_dfp_for_mcu("PIC16F877A", [old, new])
            self.assertEqual(selected["dfp_path"], str(new.resolve()))
            self.assertEqual(selected["pack_version"], "1.10")
            self.assertTrue(selected["header"].endswith("pic16f877a.h"))

    def test_builds_reusable_device_index(self):
        with tempfile.TemporaryDirectory() as temporary:
            dfp = make_dfp(
                Path(temporary), "PIC18Fxxxx_DFP", "3.2.1", ["18f4550"]
            )
            record = build_device_index([dfp])["18F4550"]
            self.assertEqual(record["pack_name"], "PIC18Fxxxx_DFP")

    def test_returns_none_when_mcu_is_missing(self):
        with tempfile.TemporaryDirectory() as temporary:
            dfp = make_dfp(
                Path(temporary), "PIC10-12Fxxx_DFP", "1.0", ["12f675"]
            )
            self.assertIsNone(select_dfp_for_mcu("16F877A", [dfp]))


if __name__ == "__main__":
    unittest.main()
