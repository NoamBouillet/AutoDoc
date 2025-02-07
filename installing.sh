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

if [ ! -w "$INSTALL_DIR" ]; then
    if [ -d "$HOME/.local/bin" ]; then
        INSTALL_DIR="$HOME/.local/bin"
    elif [ -d "$HOME/.local/share" ]; then
        mkdir -p "$HOME/.local/share/bin"
        INSTALL_DIR="$HOME/.local/share/bin"
    elif [ -d "$HOME/.local/state" ]; then
        mkdir -p "$HOME/.local/state/bin"
        INSTALL_DIR="$HOME/.local/state/bin"
    else
        mkdir -p "$HOME/.local/bin"
        INSTALL_DIR="$HOME/.local/bin"
    fi
fi

mkdir -p "$INSTALL_DIR"
echo "Downloading autodoc.py..."
curl -sLO https://raw.githubusercontent.com/NoamBouillet/AutoDoc/refs/heads/main/autodoc.py "$INSTALL_DIR/autodoc"
chmod +x "$INSTALL_DIR/autodoc"
echo "Installed autodoc to $INSTALL_DIR/autodoc"


if ! echo "$PATH" | grep -q "$INSTALL_DIR"; then
    echo "WARNING: $INSTALL_DIR is not in your PATH."
    echo "To add it, consider adding the following line to your shell configuration file (e.g. ~/.bashrc or ~/.profile):"
    echo "export PATH=\"$INSTALL_DIR:\$PATH\""
fi

echo "Installation complete! You can now run 'autodoc' from anywhere."
