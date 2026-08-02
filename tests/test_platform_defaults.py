import importlib.util
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch


PLATFORM_MODULE = Path(__file__).resolve().parents[1] / "platform.py"
SPEC = importlib.util.spec_from_file_location("microchip8_platform", PLATFORM_MODULE)
MODULE = importlib.util.module_from_spec(SPEC)
PLATFORMIO = types.ModuleType("platformio")
PLATFORMIO_PUBLIC = types.ModuleType("platformio.public")
PLATFORMIO_PUBLIC.PlatformBase = type("PlatformBase", (), {})
with patch.dict(
    sys.modules,
    {"platformio": PLATFORMIO, "platformio.public": PLATFORMIO_PUBLIC},
):
    SPEC.loader.exec_module(MODULE)


class FakeProjectConfig:
    def __init__(self, src_dir):
        self.src_dir = str(src_dir)
        self.values = {}
        self.saved = False

    def get(self, section, option, default=None):
        if (section, option) == ("env:pic12f683", "framework"):
            return ["xc8"]
        if (section, option) == ("platformio", "src_dir"):
            return self.src_dir
        return default

    def set(self, section, option, value):
        self.values[(section, option)] = value

    def save(self):
        self.saved = True


class PlatformDefaultsTests(unittest.TestCase):
    def test_new_unix_project_writes_native_pickit3_defaults(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = FakeProjectConfig(Path(temporary) / "src")
            with patch.object(MODULE.os, "name", "posix"):
                generated = MODULE.Microchip8Platform.generate_sample_code(
                    object(), config, "pic12f683"
                )

            self.assertTrue(generated)
            self.assertTrue(config.saved)
            self.assertEqual(
                config.values[("env:pic12f683", "custom_pickit3_power")],
                "yes",
            )
            self.assertEqual(
                config.values[("env:pic12f683", "custom_pk2cmd_path")],
                "~/.platformio/packages/tool-pk2cmd",
            )
            self.assertTrue((Path(temporary) / "src" / "main.c").is_file())

    def test_new_windows_project_keeps_standalone_backend(self):
        with tempfile.TemporaryDirectory() as temporary:
            config = FakeProjectConfig(Path(temporary) / "src")
            with patch.object(MODULE.os, "name", "nt"):
                MODULE.Microchip8Platform.generate_sample_code(
                    object(), config, "pic12f683"
                )

            self.assertNotIn(
                ("env:pic12f683", "custom_pk2cmd_path"), config.values
            )


if __name__ == "__main__":
    unittest.main()
