import hashlib
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.install_pk2cmd_macos import install_archive, verify_archive


def make_archive(path, members):
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in members.items():
            archive.writestr(name, content)
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PK2CMDInstallerTests(unittest.TestCase):
    def test_verifies_and_installs_required_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "pk2cmd.zip"
            checksum = make_archive(
                archive,
                {
                    "pk2cmd": b"test executable",
                    "PK2DeviceFile.dat": b"test device database",
                    "Readme.txt": b"test documentation",
                },
            )
            verify_archive(archive, checksum)
            destination = root / "installed"
            install_archive(archive, destination)
            self.assertEqual(
                (destination / "PK2DeviceFile.dat").read_bytes(),
                b"test device database",
            )
            self.assertTrue((destination / "pk2cmd").stat().st_mode & 0o100)

    def test_rejects_wrong_checksum(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "pk2cmd.zip"
            make_archive(
                archive,
                {"pk2cmd": b"x", "PK2DeviceFile.dat": b"y"},
            )
            with self.assertRaises(RuntimeError):
                verify_archive(archive, "0" * 64)

    def test_rejects_archive_without_device_database(self):
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "pk2cmd.zip"
            checksum = make_archive(archive, {"pk2cmd": b"x"})
            with self.assertRaises(RuntimeError):
                verify_archive(archive, checksum)


if __name__ == "__main__":
    unittest.main()
