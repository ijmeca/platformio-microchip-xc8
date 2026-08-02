#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
/usr/bin/env python3 "$SCRIPT_DIR/scripts/install_pk2cmd_macos.py"
status=$?
echo
if [ "$status" -eq 0 ]; then
    echo "Instalação concluída. Pressione Enter para fechar."
else
    echo "A instalação falhou. Pressione Enter para fechar."
fi
read -r
exit "$status"
