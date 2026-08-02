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
from scripts.detect_ipecmd import (
    find_ipecmd,
    normalize_ipecmd_path,
    pickit3_command,
)
from scripts.detect_pk2cmd import (
    find_pk2cmd,
    normalize_pk2cmd_path,
    pk2cmd_command,
)
from scripts.detect_pickit3 import find_pickit3, standalone_pickit3_command


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
                ["10f200", "16f877a", "18f4550"],
            )
            proc = dfp / "pic" / "include" / "proc"
            (proc / "pic16f.h").touch()
            (proc / "legacy.h").touch()
            self.assertEqual(
                set(devices_in_dfp(dfp)), {"10F200", "16F877A", "18F4550"}
            )

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


class PICkit3DetectionTests(unittest.TestCase):
    def test_normalizes_native_pk2cmd_installation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "pk2cmd"
            executable = make_executable(root / "pk2cmd")
            device_file = root / "PK2DeviceFile.dat"
            device_file.touch()
            for supplied in (root, executable):
                result = normalize_pk2cmd_path(supplied)
                self.assertEqual(result["executable"], str(executable.resolve()))
                self.assertEqual(result["device_file"], str(device_file.resolve()))

    def test_native_pk2cmd_respects_custom_environment_path_priority(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            custom = make_executable(root / "custom" / "pk2cmd")
            (custom.parent / "PK2DeviceFile.dat").touch()
            environment = make_executable(root / "environment" / "pk2cmd")
            (environment.parent / "PK2DeviceFile.dat").touch()
            on_path = make_executable(root / "path" / "pk2cmd")
            (on_path.parent / "PK2DeviceFile.dat").touch()
            result = find_pk2cmd(
                custom_path=str(custom.parent),
                environ={"PK2CMD_PATH": str(environment.parent)},
                path_lookup=lambda name: str(on_path),
            )
            self.assertEqual(result["executable"], str(custom.resolve()))

    def test_builds_native_pk2cmd_command_without_shell(self):
        command = pk2cmd_command(
            "/external/tools/pk2cmd",
            "12F683",
            "../../../project/firmware.hex",
            externally_powered=True,
            extra_flags=["-X"],
        )
        self.assertEqual(
            command[:4],
            [
                "pk2cmd",
                "-PPIC12F683",
                "-F../../../project/firmware.hex",
                "-M",
            ],
        )
        self.assertEqual(command[-2:], ["-W", "-X"])

    def test_finds_standalone_application_and_builds_command(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "PICkit 3 v3"
            application = make_executable(root / "PICkit3.exe")
            device_file = root / "PK2DeviceFile.dat"
            device_file.touch()
            result = find_pickit3(environ={}, search_roots=[root])
            command = standalone_pickit3_command(
                "uploader.exe",
                result["executable"],
                result["device_file"],
                "PIC12F683",
                "firmware.hex",
            )
            self.assertEqual(result["executable"], str(application.resolve()))
            self.assertIn("12F683", command)
            self.assertEqual(command[-2:], ["--hex", "firmware.hex"])

    def test_selects_newest_ipecmd(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_executable(
                root / "v6.10" / "mplab_platform" / "mplab_ipe" / "ipecmd.exe"
            )
            newest = make_executable(
                root / "v6.20" / "mplab_platform" / "mplab_ipe" / "ipecmd.exe"
            )
            result = find_ipecmd(
                environ={}, path_lookup=lambda name: None, search_roots=[root]
            )
            self.assertEqual(result["executable"], str(newest.resolve()))

    def test_normalizes_macos_ipecmd_script_from_mplabx_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "mplabx" / "v6.25"
            script = make_executable(
                root / "mplab_platform" / "mplab_ipe" / "bin" / "ipecmd.sh"
            )
            result = normalize_ipecmd_path(root)
            self.assertEqual(result["executable"], str(script.resolve()))
            self.assertEqual(result["version"], "6.25")

    def test_selects_newest_macos_ipecmd(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            make_executable(
                root
                / "v5.45"
                / "mplab_platform"
                / "mplab_ipe"
                / "bin"
                / "ipecmd.sh"
            )
            unsupported = make_executable(
                root
                / "v6.25"
                / "mplab_platform"
                / "mplab_ipe"
                / "bin"
                / "ipecmd.sh"
            )
            self.assertTrue(unsupported.is_file())
            result = find_ipecmd(
                environ={}, path_lookup=lambda name: None, search_roots=[root]
            )
            expected = root / "v5.45" / "mplab_platform" / "mplab_ipe" / "bin" / "ipecmd.sh"
            self.assertEqual(result["executable"], str(expected.resolve()))

    def test_selects_ipecmd_620_as_latest_pickit3_compatible_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            supported = make_executable(
                root
                / "v6.20"
                / "mplab_platform"
                / "mplab_ipe"
                / "bin"
                / "ipecmd.sh"
            )
            make_executable(
                root
                / "v6.25"
                / "mplab_platform"
                / "mplab_ipe"
                / "bin"
                / "ipecmd.sh"
            )
            result = find_ipecmd(
                environ={}, path_lookup=lambda name: None, search_roots=[root]
            )
            self.assertEqual(result["executable"], str(supported.resolve()))

    def test_custom_macos_ipecmd_precedes_automatic_search(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            custom = make_executable(root / "custom" / "bin" / "ipecmd.sh")
            make_executable(
                root
                / "automatic"
                / "v6.25"
                / "mplab_platform"
                / "mplab_ipe"
                / "bin"
                / "ipecmd.sh"
            )
            result = find_ipecmd(
                custom_path=str(custom),
                environ={},
                path_lookup=lambda name: None,
                search_roots=[root / "automatic"],
            )
            self.assertEqual(result["executable"], str(custom.resolve()))

    def test_builds_pickit3_command_without_shell(self):
        command = pickit3_command(
            "ipecmd.exe", "PIC12F675", "build/firmware.hex", ["-OL"]
        )
        self.assertEqual(command[0:3], ["ipecmd.exe", "-P12F675", "-TPPK3"])
        self.assertIn("-F%s" % Path("build/firmware.hex"), command)
        self.assertEqual(command[-2:], ["-M", "-OL"])


if __name__ == "__main__":
    unittest.main()
