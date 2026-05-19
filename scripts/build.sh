#!/bin/bash
# Ultron OS - Build Script
# Builds themes, packages, and ISO image

set -e

ULTRON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$ULTRON_ROOT/build"
ISO_DIR="$ULTRON_ROOT/iso"

echo "=== Ultron OS Build System ==="

# Create build directory
mkdir -p "$BUILD_DIR"
mkdir -p "$ISO_DIR"

# Build GTK theme
echo "[1/4] Building Ultron GTK theme..."
if [ -d "$ULTRON_ROOT/themes/gtk" ]; then
    cd "$ULTRON_ROOT/themes/gtk"
    meson setup build --prefix=/usr
    ninja -C build
    echo "GTK theme built successfully"
else
    echo "GTK theme directory not found, skipping..."
fi

# Build icon theme
echo "[2/4] Building Ultron icon theme..."
if [ -d "$ULTRON_ROOT/themes/icons" ]; then
    cd "$ULTRON_ROOT/themes/icons"
    # Icon themes typically don't need compilation
    echo "Icon theme ready"
else
    echo "Icon theme directory not found, skipping..."
fi

# Build cursor theme
echo "[3/4] Building Ultron cursor theme..."
if [ -d "$ULTRON_ROOT/themes/cursor" ]; then
    cd "$ULTRON_ROOT/themes/cursor"
    if [ -f "index.theme" ]; then
        xcursorgen -q cursor.cfg
        echo "Cursor theme built successfully"
    fi
else
    echo "Cursor theme directory not found, skipping..."
fi

# Generate ISO
echo "[4/4] Generating ISO image..."
if command -v cubic &> /dev/null; then
    echo "Using Cubic for ISO generation..."
    # Cubic configuration would go here
    echo "ISO generation configured (requires manual Cubic execution)"
else
    echo "Cubic not installed. Install with: sudo apt install cubic"
    echo "ISO generation skipped"
fi

echo "=== Build Complete ==="
echo "Build artifacts available in: $BUILD_DIR"
