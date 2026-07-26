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
                self.assertEqual(manifest_path.stem, ("pic%s" % mcu).lower())
