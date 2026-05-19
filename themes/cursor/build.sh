#!/bin/bash
# Build script for Ultron Cursor Theme
# Converts PNG source files to XCursor format

set -e

THEME_NAME="Ultron-Cursor"
BUILD_DIR="build"
SIZES=(24 32 48 64)

# Cursor definitions: name hotspot_x hotspot_y
CURSORS=(
    "left_ptr 12 12"
    "hand2 12 12"
    "xterm 12 12"
    "sb_h_double_arrow 12 12"
    "sb_v_double_arrow 12 12"
    "fd_double_arrow 12 12"
    "watch 16 16"
    "fleur 16 16"
    "no_drop 12 12"
)

echo "Building ${THEME_NAME} cursor theme..."

# Create build directory
mkdir -p "${BUILD_DIR}/${THEME_NAME}/cursors"

# Copy theme index
cp index.theme "${BUILD_DIR}/${THEME_NAME}/"

# Build cursors for each size
for size in "${SIZES[@]}"; do
    echo "  Building ${size}px cursors..."
    mkdir -p "${BUILD_DIR}/${THEME_NAME}/${size}x${size}"
    
    for cursor_def in "${CURSORS[@]}"; do
        read -r name hx hy <<< "$cursor_def"
        src="src/${name}.png"
        
        if [ -f "$src" ]; then
            # Generate XCursor file
            echo "    ${name} (${size}px)"
            xcursorgen -s "${size}" "${BUILD_DIR}/${THEME_NAME}/${size}x${size}/cursor.cfg" \
                "${BUILD_DIR}/${THEME_NAME}/cursors/${name}" 2>/dev/null || true
        fi
    done
done

# Create symlinks for cursor aliases
cd "${BUILD_DIR}/${THEME_NAME}/cursors"
ln -sf left_ptr arrow 2>/dev/null || true
ln -sf left_ptr top_left_arrow 2>/dev/null || true
ln -sf hand2 pointer 2>/dev/null || true
ln -sf xterm ibeam 2>/dev/null || true
ln -sf sb_h_double_arrow h_double_arrow 2>/dev/null || true
ln -sf sb_v_double_arrow v_double_arrow 2>/dev/null || true
ln -sf fd_double_arrow size_fdiag 2>/dev/null || true
ln -sf fleur move 2>/dev/null || true
ln -sf watch left_ptr_watch 2>/dev/null || true
ln -sf no_drop banned 2>/dev/null || true

echo "✓ Cursor theme built successfully in ${BUILD_DIR}/"
