#!/usr/bin/env python3
"""Install the externally licensed pk2cmd macOS release for PlatformIO."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


VERSION = "1.27.01"
DOWNLOAD_URL = (
    "https://github.com/jaka-fi/pk2cmd/releases/download/"
    "v1.27.01/pk2cmd_mac_1_27_01.zip"
)
DOWNLOAD_SHA256 = (
    "162922f32d893270e07f820dac3c9b6fb100693721350d61620b132f3c96b92d"
)
LICENSE_URL = "https://github.com/jaka-fi/pk2cmd/blob/master/license.txt"
DEFAULT_INSTALL_DIR = Path("~/.platformio/packages/tool-pk2cmd").expanduser()
REQUIRED_FILES = ("pk2cmd", "PK2DeviceFile.dat")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_archive(path: Path, expected_sha256: str = DOWNLOAD_SHA256) -> None:
    actual = sha256(path)
    if actual != expected_sha256:
        raise RuntimeError(
            "SHA-256 inválido para o download do pk2cmd: %s" % actual
        )
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
    missing = [name for name in REQUIRED_FILES if name not in names]
    if missing:
        raise RuntimeError(
            "O pacote do pk2cmd não contém: %s" % ", ".join(missing)
        )


def install_archive(archive_path: Path, destination: Path) -> None:
    destination = destination.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=".tool-pk2cmd-", dir=str(destination.parent))
    )
    try:
        with zipfile.ZipFile(archive_path) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                if Path(member.filename).name != member.filename:
                    raise RuntimeError(
                        "Caminho inesperado no pacote: %s" % member.filename
                    )
                target = staging / member.filename
                with archive.open(member) as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
        (staging / "pk2cmd").chmod(0o755)
        if destination.exists():
            shutil.rmtree(destination)
        staging.replace(destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def validate_runtime(destination: Path) -> None:
    environment = dict(os.environ)
    environment["PATH"] = os.pathsep.join(
        (str(destination), environment.get("PATH", ""))
    )
    result = subprocess.run(
        ["pk2cmd", "-?V"],
        cwd=str(destination),
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "O pk2cmd foi instalado, mas não pôde ser executado:\n%s"
            % (result.stderr or result.stdout).strip()
        )


def require_supported_mac() -> None:
    if sys.platform != "darwin":
        raise RuntimeError("Este instalador é exclusivo para macOS.")
    if os.uname().machine.lower() == "arm64":
        result = subprocess.run(
            ["/usr/bin/arch", "-x86_64", "/usr/bin/true"],
            check=False,
            capture_output=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "O release do pk2cmd é Intel. Instale o Rosetta 2 antes:\n"
                "softwareupdate --install-rosetta"
            )


def confirm(prompt: str) -> bool:
    return input(prompt).strip().upper() == "ACEITO"


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Instala o pk2cmd externo para a plataforma Microchip8."
    )
    parser.add_argument(
        "--accept-license",
        action="store_true",
        help="confirma previamente a aceitação da licença Microchip",
    )
    parser.add_argument(
        "--install-dir",
        type=Path,
        default=DEFAULT_INSTALL_DIR,
        help="diretório de instalação",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        require_supported_mac()
        print("Instalador do pk2cmd %s para PlatformIO Microchip8" % VERSION)
        print("Licença Microchip: %s" % LICENSE_URL)
        print(
            "O pk2cmd, o banco de dispositivos e os firmwares não fazem parte "
            "deste projeto e serão baixados do release oficial."
        )
        if not args.accept_license and not confirm(
            "Leia a licença e digite ACEITO para baixar e instalar: "
        ):
            print("Instalação cancelada; a licença não foi aceita.")
            return 2

        destination = args.install_dir.expanduser().resolve()
        if destination.exists() and not confirm(
            "%s já existe. Digite ACEITO para substituí-lo: " % destination
        ):
            print("Instalação cancelada; os arquivos existentes foram preservados.")
            return 2

        with tempfile.TemporaryDirectory(prefix="pk2cmd-download-") as temporary:
            archive = Path(temporary) / "pk2cmd.zip"
            print("Baixando release oficial...")
            urllib.request.urlretrieve(DOWNLOAD_URL, archive)
            verify_archive(archive)
            install_archive(archive, destination)

        validate_runtime(destination)
        print("pk2cmd instalado e validado em: %s" % destination)
        print("Configuração para platformio.ini:")
        print("custom_pickit3_power = yes")
        print("custom_pk2cmd_path = ~/.platformio/packages/tool-pk2cmd")
        return 0
    except (OSError, RuntimeError, urllib.error.URLError, zipfile.BadZipFile) as error:
        print("Erro: %s" % error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
