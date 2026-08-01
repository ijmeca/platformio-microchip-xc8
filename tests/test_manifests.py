import json
import unittest
from pathlib import Path


class BoardManifestTests(unittest.TestCase):
    def test_existing_board_manifests_are_valid(self):
        boards_dir = Path(__file__).resolve().parent.parent / "boards"
        manifests = list(boards_dir.glob("*.json"))
        self.assertTrue(manifests)

        for manifest_path in manifests:
            with self.subTest(manifest=manifest_path.name):
                with manifest_path.open(encoding="utf-8") as manifest_file:
                    manifest = json.load(manifest_file)

                mcu = manifest["build"]["mcu"]
                self.assertIn("xc8", manifest["frameworks"])
                self.assertEqual(manifest["platform"], "microchip8")
                self.assertEqual(manifest["upload"]["protocol"], "pickit3")
                self.assertIn("pickit3", manifest["upload"]["protocols"])
                self.assertEqual(manifest_path.stem, ("pic%s" % mcu).lower())

    def test_new_board_memory_matches_device_data(self):
        boards_dir = Path(__file__).resolve().parent.parent / "boards"
        expected = {
            "pic12f615": (1024, 64, 0),
            "pic16f628": (2048, 224, 128),
            "pic16f628a": (2048, 224, 128),
        }
        for board, (program, ram, eeprom) in expected.items():
            with self.subTest(board=board):
                with (boards_dir / (board + ".json")).open(encoding="utf-8") as source:
                    manifest = json.load(source)
                self.assertEqual(manifest["upload"]["maximum_size"], program)
                self.assertEqual(manifest["upload"]["maximum_ram_size"], ram)
                self.assertEqual(manifest["microchip8"]["eeprom_size"], eeprom)
