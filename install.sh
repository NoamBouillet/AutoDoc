#!/bin/bash

set -e

if [ -t 1 ]; then
    RED="\e[1;31m"
    GREEN="\e[1;32m"
    YELLOW="\e[1;33m"
    BLUE="\e[1;34m"
    RESET="\e[0m"
else
    RED=""
    GREEN=""
    YELLOW=""
    BLUE=""
    RESET=""
fi

fail()
{
    echo -e "${RED}Error:${RESET} $1" >&2
    exit 1
}

check_dependencies()
{
    missing=()
    
    if ! command -v "pdflatex" >/dev/null ; then
        echo -e "${RED}Missing pdflatex package. Please install it manually.${RESET}"
        exit 1
    fi
    for cmd in python3 doxygen; do
        if ! command -v "$cmd" >/dev/null ; then
            missing+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -eq 0 ]; then
        echo -e "${GREEN}✔ All dependencies are installed.${RESET}"
        return
    fi

    echo -e "${YELLOW}The following dependencies are missing:${RESET} ${missing[*]}"
    for pkg_mgr in "apt-get update && apt-get install -y" "dnf install -y" "pacman -Syu --noconfirm"; do
        if command -v ${pkg_mgr%% *} >/dev/null; then
            echo -e "${BLUE}➜ Attempting to install ${missing[*]} via ${pkg_mgr%% *}...${RESET}"
            sudo bash -c "$pkg_mgr ${missing[*]}" >/dev/null
            return
        fi
    done

    echo -e "${RED}✖ No supported package manager found. Please install dependencies manually.${RESET}"
    exit 1
}

get_su()
{
    if [ "$EUID" -ne 0 ]; then
        echo -e "${BLUE}🔒 Requesting superuser privileges...${RESET}"
        sudo bash "$0" "$@" || fail "Superuser privileges required."
        exit
    fi
}

install_autodoc()
{
    INSTALL_DIR="/usr/local/bin"
    TMP_FILE=$(mktemp)

    echo -e "${BLUE}⬇ Downloading autodoc.py...${RESET}"
    curl -sL -o "$TMP_FILE" https://raw.githubusercontent.com/NoamBouillet/AutoDoc/main/autodoc.py || fail "Failed to download autodoc.py"

    mv "$TMP_FILE" "$INSTALL_DIR/autodoc"
    chmod 755 "$INSTALL_DIR/autodoc"

    echo -e "${GREEN}✔ Installed autodoc to $INSTALL_DIR/autodoc${RESET}"
}

main()
{
    get_su "$@"
    check_dependencies
    install_autodoc
}

main "$@"
