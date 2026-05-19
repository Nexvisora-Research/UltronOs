#!/bin/bash
# Ultron OS - Desktop Shell Installation Script
# Installs the custom GNOME Shell extension

set -e

ULTRON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EXTENSION_DIR="$ULTRON_ROOT/desktop-shell/ultron-shell-extension"
GNOME_EXTENSIONS_DIR="$HOME/.local/share/gnome-shell/extensions"
EXTENSION_UUID="ultron-shell@ultron.org"

echo "=== Ultron Shell Extension Installer ==="

# Create GNOME extensions directory
mkdir -p "$GNOME_EXTENSIONS_DIR"

# Copy extension files
echo "[1/4] Installing extension files..."
cp -r "$EXTENSION_DIR" "$GNOME_EXTENSIONS_DIR/$EXTENSION_UUID"

# Compile GSettings schemas
echo "[2/4] Compiling GSettings schemas..."
glib-compile-schemas "$GNOME_EXTENSIONS_DIR/$EXTENSION_UUID/schemas"

# Copy system-wide schemas
echo "[3/4] Installing system-wide schemas..."
sudo cp "$EXTENSION_DIR/schemas/org.ultron.shell.gschema.xml" /usr/share/glib-2.0/schemas/
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

# Enable extension
echo "[4/4] Enabling extension..."
gnome-extensions enable "$EXTENSION_UUID"

echo "=== Installation Complete ==="
echo "Please restart GNOME Shell (Alt+F2, r, Enter) or log out and back in"
echo "Configure settings via: gnome-extensions prefs $EXTENSION_UUID"
