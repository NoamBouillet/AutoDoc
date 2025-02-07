#!/bin/bash

set -e 

check_dependencies() {
    missing=""
    
    if ! command -v python3 >/dev/null 2>&1; then
        missing="$missing python3"
    fi

    if ! command -v doxygen >/dev/null 2>&1; then
        missing="$missing doxygen"
    fi

    if [ -n "$missing" ]; then
        echo "The following dependencies are missing:$missing"
        
        if command -v apt-get >/dev/null 2>&1; then
            echo "Attempting to install via apt-get..."
            sudo apt-get update
            sudo apt-get install -y $missing
        elif command -v dnf >/dev/null 2>&1; then
            echo "Attempting to install via dnf..."
            sudo dnf install -y $missing
        elif command -v pacman >/dev/null 2>&1; then
            echo "Attempting to install via pacman..."
            sudo pacman -Syu --noconfirm $missing
        else
            echo "No supported package manager found. Please install dependencies manually."
            exit 1
        fi
    else
        echo "All dependencies are installed."
    fi
}

check_dependencies

INSTALL_DIR="/usr/local/bin"

mkdir -p "$INSTALL_DIR"
echo "Downloading autodoc.py..."
curl -sL https://raw.githubusercontent.com/NoamBouillet/AutoDoc/main/autodoc.py -o "$INSTALL_DIR/autodoc.py"
chmod +x "$INSTALL_DIR/autodoc"
echo "Installed autodoc to $INSTALL_DIR/autodoc"
