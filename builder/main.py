from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from SCons.Script import AlwaysBuild, Default, DefaultEnvironment

env = DefaultEnvironment()

scripts_dir = Path(env.PioPlatform().get_dir()) / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from detect_dfp import discover_dfps, select_dfp_for_mcu
from detect_ipecmd import find_ipecmd, pickit3_command
from detect_pickit3 import find_pickit3, standalone_pickit3_command
from detect_xc8 import find_xc8


board = env.BoardConfig()

mcu = board.get("build.mcu")

if not mcu:
    env.Exit("A placa não definiu build.mcu")


xc8_installation = find_xc8(
    custom_path=env.GetProjectOption("custom_xc8_path", None)
)

if not xc8_installation:
    env.Exit(
        "MPLAB XC8 não encontrado. "
        "Instale o XC8 ou defina custom_xc8_path no platformio.ini "
        "ou exporte XC8_PATH=/caminho/para/xc8."
    )

xc8 = xc8_installation["executable"]
configured_dfp = env.GetProjectOption("custom_dfp_path", None)
dfp_paths = discover_dfps(
    custom_dfp_path=configured_dfp,
    custom_dfp_root=env.GetProjectOption("custom_dfp_root", None),
)
selected_dfp = select_dfp_for_mcu(mcu, dfp_paths)

if not selected_dfp:
    if configured_dfp:
        env.Exit("O DFP configurado não contém o header do MCU %s." % mcu)
    env.Exit(
        "Nenhum DFP instalado oferece suporte ao MCU %s. "
        "Instale o Device Family Pack correspondente no MPLAB X "
        "ou defina custom_dfp_path." % mcu
    )

dfp_path = selected_dfp["dfp_path"]

build_dir = env.subst("$BUILD_DIR")
project_src_dir = env.subst("$PROJECT_SRC_DIR")
project_include_dir = env.subst("$PROJECT_INCLUDE_DIR")

xc8_include_dir = os.path.join(xc8_installation["root"], "pic", "include")
xc8_c99_include_dir = os.path.join(xc8_include_dir, "c99")
dfp_include_dir = os.path.join(dfp_path, "pic", "include")
dfp_proc_include_dir = os.path.join(dfp_include_dir, "proc")

intellisense_include_paths = [
    path
    for path in (
        dfp_include_dir,
        dfp_proc_include_dir,
        xc8_include_dir,
        xc8_c99_include_dir,
        project_include_dir,
        project_src_dir,
    )
    if os.path.isdir(path)
]

intellisense_defines = [
    ("__XC8", 1),
    ("__XC8__", 1),
    ("__bit", "unsigned char"),
    ("__int24", "int"),
    ("__uint24", "unsigned int"),
    ("__bank0", ""),
    ("_%s" % mcu, 1),
    ("__%s" % mcu, 1),
    ("__%s__" % mcu, 1),
]

if str(mcu).upper().startswith("18F"):
    intellisense_defines.append(("__PICC18__", 1))
else:
    intellisense_defines.append(("__PICC__", 1))

env.Append(
    CPPPATH=intellisense_include_paths,
    CPPDEFINES=intellisense_defines,
)

firmware_elf = os.path.join(build_dir, "firmware.elf")
firmware_hex = os.path.join(build_dir, "firmware.hex")

sources = env.Glob(
    os.path.join(project_src_dir, "*.c")
)

if not sources and not env.IsIntegrationDump():
    env.Exit("Nenhum arquivo .c encontrado em src/")


def build_firmware(target, source, env):
    os.makedirs(build_dir, exist_ok=True)

    source_files = [
        str(item)
        for item in source
    ]

    command = [
        xc8,
        "-mcpu=%s" % mcu,
        "-mdfp=%s" % dfp_path,
        "-O1",
        "-o",
        firmware_elf,
    ] + source_files

    print("")
    print("Microchip XC8 build")
    print("XC8:", xc8)
    print("MCU:", mcu)
    print("DFP:", dfp_path)
    print("")

    result = subprocess.run(
        command,
        check=False,
    )

    if result.returncode != 0:
        return result.returncode

    for artifact in (firmware_elf, firmware_hex):
        if not os.path.isfile(artifact):
            print("XC8 n\u00e3o gerou o artefato esperado:", artifact)
            return 1

    return 0


build = env.Command(
    [firmware_elf, firmware_hex],
    sources,
    build_firmware,
)

AlwaysBuild(build)
Default(build)


def upload_firmware(target, source, env):
    protocol = env.subst("$UPLOAD_PROTOCOL") or board.get(
        "upload.protocol", "pickit3"
    )
    if str(protocol).lower() != "pickit3":
        print("Protocolo de upload n\u00e3o suportado:", protocol)
        return 1

    upload_flags = env.GetProjectOption("upload_flags", [])
    if isinstance(upload_flags, str):
        upload_flags = upload_flags.split()

    standalone = find_pickit3(
        custom_path=env.GetProjectOption("custom_pickit3_path", None)
    )
    if standalone:
        csc = os.path.join(
            os.environ.get("WINDIR", r"C:\Windows"),
            "Microsoft.NET",
            "Framework64",
            "v4.0.30319",
            "csc.exe",
        )
        uploader = os.path.join(build_dir, "pickit3-uploader.exe")
        uploader_source = os.path.join(str(scripts_dir), "pickit3_uploader.cs")
        if not os.path.isfile(csc):
            print("Compilador .NET Framework csc.exe n\u00e3o encontrado:", csc)
            return 1
        compile_result = subprocess.run(
            [
                csc,
                "/nologo",
                "/target:exe",
                "/platform:x86",
                "/reference:System.Windows.Forms.dll",
                "/out:%s" % uploader,
                uploader_source,
            ],
            check=False,
        )
        if compile_result.returncode != 0:
            return compile_result.returncode
        command = standalone_pickit3_command(
            uploader,
            standalone["executable"],
            standalone["device_file"],
            mcu,
            firmware_hex,
        ) + upload_flags
        print("PICkit 3 standalone upload via:", standalone["executable"])
    else:
        installation = find_ipecmd(
            custom_path=env.GetProjectOption("custom_ipecmd_path", None)
        )
        if not installation:
            print(
                "PICkit 3 Programmer ou MPLAB IPE IPECMD n\u00e3o encontrado. "
                "Defina custom_pickit3_path, PICKIT3_PATH, custom_ipecmd_path "
                "ou IPECMD_PATH."
            )
            return 1
        command = pickit3_command(
            installation["executable"], mcu, firmware_hex, upload_flags
        )
        print("PICkit 3 upload via:", installation["executable"])
    return subprocess.run(command, check=False).returncode


upload = env.Alias("upload", build, upload_firmware)
AlwaysBuild(upload)
