#!/bin/bash

set -e

fail()
{
    echo -e "\e[31mError:\e[0m $1" >&2
    exit 1
}

check_dependencies()
{
    missing=()
    
    for cmd in python3 doxygen; do
        command -v "$cmd" >/dev/null 2>&1 || missing+=("$cmd")
    done
    if [ ${#missing[@]} -eq 0 ]; then
        echo "All dependencies are installed."
        return
    fi
    echo "The following dependencies are missing: ${missing[*]}"
    for pkg_mgr in "apt-get update && apt-get install -y" "dnf install -y" "pacman -Syu --noconfirm"; do
        if command -v ${pkg_mgr%% *} >/dev/null 2>&1; then
            echo "Attempting to install via ${pkg_mgr%% *}..."
            sudo bash -c "$pkg_mgr ${missing[*]}"
            return
        fi
    done
    echo "No supported package manager found. Please install dependencies manually."
    exit 1
}

get_su()
{
    if [ "$EUID" -ne 0 ]; then
        sudo bash "$0" "$@"
        exit
    fi
}

install_autodoc()
{
    INSTALL_DIR="/usr/local/bin"
    TMP_FILE=$(mktemp)

    echo "Downloading autodoc.py..."
    curl -sL -o "$TMP_FILE" https://raw.githubusercontent.com/NoamBouillet/AutoDoc/main/autodoc.py || fail "Failed to download autodoc.py"
    mv "$TMP_FILE" "$INSTALL_DIR/autodoc"
    chmod 755 "$INSTALL_DIR/autodoc"
    echo "Installed autodoc to $INSTALL_DIR/autodoc"
}

main()
{
    get_su "$@"
    check_dependencies
    install_autodoc
}

main "$@"

