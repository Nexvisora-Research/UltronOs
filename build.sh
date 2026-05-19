#!/bin/bash
# Ultron OS - Master Build Script
# Builds all phases and verifies the complete system

ULTRON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$ULTRON_ROOT/build"
LOG_FILE="$BUILD_DIR/build.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Counters
TOTAL=0
PASSED=0
FAILED=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ultron OS - Master Build System${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create build directory
mkdir -p "$BUILD_DIR"

# Initialize log
echo "Ultron OS Build Log - $(date)" > "$LOG_FILE"

# Function to check if a file exists
check_file() {
    local name="$1"
    local filepath="$2"
    
    TOTAL=$((TOTAL + 1))
    echo -ne "  [$TOTAL] Checking $name... "
    echo "[$TOTAL] Checking $name" >> "$LOG_FILE"
    
    if [ -f "$filepath" ]; then
        echo -e "${GREEN}✓ EXISTS${NC}"
        echo "  Result: EXISTS" >> "$LOG_FILE"
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ MISSING${NC}"
        echo "  Result: MISSING" >> "$LOG_FILE"
        FAILED=$((FAILED + 1))
    fi
}

echo -e "${YELLOW}Phase 1: Foundation${NC}"
echo "-------------------------------------------"

check_file "Base system setup script" "$ULTRON_ROOT/scripts/setup-base-system.sh"
check_file "Post-install script" "$ULTRON_ROOT/scripts/post-install.sh"
check_file "Build script" "$ULTRON_ROOT/scripts/build.sh"
check_file "Color palette" "$ULTRON_ROOT/artwork/color-palette.css"
check_file "Logo SVG" "$ULTRON_ROOT/artwork/logo.svg"
check_file "Wallpaper SVG" "$ULTRON_ROOT/artwork/wallpaper-default.svg"
check_file "Icon theme index" "$ULTRON_ROOT/artwork/icons/index.theme"
check_file "GTK Dark theme CSS" "$ULTRON_ROOT/themes/gtk/Ultron-Dark/gtk-4.0/gtk.css"
check_file "GTK Light theme CSS" "$ULTRON_ROOT/themes/gtk/Ultron-Light/gtk-4.0/gtk.css"
check_file "GTK theme meson.build" "$ULTRON_ROOT/themes/gtk/meson.build"
check_file "Calamares settings" "$ULTRON_ROOT/iso/calamares/settings.conf"
check_file "Calamares branding" "$ULTRON_ROOT/iso/calamares/branding/ultron/branding.desc"
check_file "Calamares theme" "$ULTRON_ROOT/iso/calamares/branding/ultron/ultron.qss"
check_file "Welcome wizard" "$ULTRON_ROOT/apps/ultron-welcome/ultron-welcome.py"
check_file "ISO config" "$ULTRON_ROOT/iso/iso-config.yaml"

echo ""
echo -e "${YELLOW}Phase 2: Desktop Experience${NC}"
echo "-------------------------------------------"

check_file "Shell extension metadata" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/metadata.json"
check_file "Shell extension.js" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/extension.js"
check_file "Shell prefs.js" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/prefs.js"
check_file "Shell stylesheet" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/stylesheet.css"
check_file "Shell meson.build" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/meson.build"
check_file "GSettings schema" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/schemas/org.ultron.shell.gschema.xml"
check_file "Taskbar component" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/taskbar.js"
check_file "Launcher component" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/launcher.js"
check_file "Notification center" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/notification-center.js"
check_file "System info component" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/system-info.js"
check_file "Window manager" "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/window-manager.js"
check_file "Install script" "$ULTRON_ROOT/desktop-shell/install.sh"

echo ""
echo -e "${YELLOW}Phase 3: System Tools${NC}"
echo "-------------------------------------------"

check_file "Settings application" "$ULTRON_ROOT/apps/ultron-settings/src/application.py"
check_file "Settings window" "$ULTRON_ROOT/apps/ultron-settings/src/window.py"
check_file "Appearance page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/appearance.py"
check_file "Network page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/network.py"
check_file "Bluetooth page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/bluetooth.py"
check_file "Sound page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/sound.py"
check_file "Display page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/display.py"
check_file "Notifications page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/notifications.py"
check_file "Privacy page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/privacy.py"
check_file "Accounts page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/accounts.py"
check_file "System page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/system.py"
check_file "About page" "$ULTRON_ROOT/apps/ultron-settings/src/pages/about.py"
check_file "Settings desktop file" "$ULTRON_ROOT/apps/ultron-settings/data/org.ultron.settings.desktop"
check_file "Settings meson.build" "$ULTRON_ROOT/apps/ultron-settings/meson.build"
check_file "Control center" "$ULTRON_ROOT/apps/ultron-control-center/src/control-center.py"
check_file "Nautilus extension" "$ULTRON_ROOT/packages/nautilus-extension/ultron-nautilus/extension.py"

echo ""
echo -e "${YELLOW}Phase 4: Ecosystem${NC}"
echo "-------------------------------------------"

check_file "Store application" "$ULTRON_ROOT/apps/ultron-store/src/application.py"
check_file "Store window" "$ULTRON_ROOT/apps/ultron-store/src/window.py"
check_file "Explore page" "$ULTRON_ROOT/apps/ultron-store/src/pages/explore.py"
check_file "Search page" "$ULTRON_ROOT/apps/ultron-store/src/pages/search.py"
check_file "Installed page" "$ULTRON_ROOT/apps/ultron-store/src/pages/installed.py"
check_file "Updates page" "$ULTRON_ROOT/apps/ultron-store/src/pages/updates.py"
check_file "App detail page" "$ULTRON_ROOT/apps/ultron-store/src/pages/app_detail.py"
check_file "Store desktop file" "$ULTRON_ROOT/apps/ultron-store/data/org.ultron.store.desktop"
check_file "Store meson.build" "$ULTRON_ROOT/apps/ultron-store/meson.build"
check_file "Updater" "$ULTRON_ROOT/apps/ultron-updater/src/updater.py"
check_file "Driver manager" "$ULTRON_ROOT/apps/ultron-driver/src/driver-manager.py"
check_file "Cloud service" "$ULTRON_ROOT/services/ultron-cloud/src/cloud_service.py"
check_file "AI assistant" "$ULTRON_ROOT/apps/ultron-ai/src/ai_assistant.py"

echo ""
echo -e "${YELLOW}Phase 5: Optimization${NC}"
echo "-------------------------------------------"

check_file "Performance tuner" "$ULTRON_ROOT/tools/ultron-tune/src/performance_tuner.py"
check_file "Security hardener" "$ULTRON_ROOT/tools/ultron-security/src/security_hardener.py"
check_file "Power manager" "$ULTRON_ROOT/tools/ultron-power/src/power_manager.py"
check_file "System monitor" "$ULTRON_ROOT/tools/ultron-monitor/src/system_monitor.py"
check_file "Benchmark" "$ULTRON_ROOT/tools/ultron-bench/src/benchmark.py"
check_file "Update tester" "$ULTRON_ROOT/tools/ultron-bench/src/update_tester.py"

echo ""
echo -e "${YELLOW}Phase 6: Expansion${NC}"
echo "-------------------------------------------"

check_file "Device manager" "$ULTRON_ROOT/tools/ultron-device/src/device_manager.py"
check_file "Adaptive UI" "$ULTRON_ROOT/apps/ultron-mobile/src/adaptive_ui.py"
check_file "Voice assistant" "$ULTRON_ROOT/apps/ultron-voice/src/voice_assistant.py"
check_file "Workflow engine" "$ULTRON_ROOT/services/ultron-workflow/src/workflow_engine.py"
check_file "Gesture controller" "$ULTRON_ROOT/tools/ultron-gesture/src/gesture_controller.py"
check_file "Device sync" "$ULTRON_ROOT/services/ultron-sync/src/device_sync.py"

echo ""
echo -e "${YELLOW}Python Syntax Validation${NC}"
echo "-------------------------------------------"

# Validate Python files
PY_COUNT=0
PY_PASS=0
PY_FAIL=0

while IFS= read -r -d '' pyfile; do
    filename=$(basename "$pyfile")
    PY_COUNT=$((PY_COUNT + 1))
    TOTAL=$((TOTAL + 1))
    echo -ne "  [$TOTAL] Syntax: $filename... "
    
    if python3 -m py_compile "$pyfile" >> "$LOG_FILE" 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        PY_PASS=$((PY_PASS + 1))
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}"
        PY_FAIL=$((PY_FAIL + 1))
        FAILED=$((FAILED + 1))
    fi
done < <(find "$ULTRON_ROOT" -name "*.py" -type f -print0 2>/dev/null)

echo ""
echo -e "${YELLOW}JSON Validation${NC}"
echo "-------------------------------------------"

# Validate JSON files
JSON_COUNT=0
JSON_PASS=0
JSON_FAIL=0

while IFS= read -r -d '' jsonfile; do
    filename=$(basename "$jsonfile")
    JSON_COUNT=$((JSON_COUNT + 1))
    TOTAL=$((TOTAL + 1))
    echo -ne "  [$TOTAL] JSON: $filename... "
    
    if python3 -m json.tool "$jsonfile" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ VALID${NC}"
        JSON_PASS=$((JSON_PASS + 1))
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ INVALID${NC}"
        JSON_FAIL=$((JSON_FAIL + 1))
        FAILED=$((FAILED + 1))
    fi
done < <(find "$ULTRON_ROOT" -name "*.json" -type f -print0 2>/dev/null)

echo ""
echo -e "${YELLOW}Shell Script Validation${NC}"
echo "-------------------------------------------"

# Validate shell scripts
SH_COUNT=0
SH_PASS=0
SH_FAIL=0

while IFS= read -r -d '' shfile; do
    filename=$(basename "$shfile")
    SH_COUNT=$((SH_COUNT + 1))
    TOTAL=$((TOTAL + 1))
    echo -ne "  [$TOTAL] Shell: $filename... "
    
    if bash -n "$shfile" >> "$LOG_FILE" 2>&1; then
        echo -e "${GREEN}✓ VALID${NC}"
        SH_PASS=$((SH_PASS + 1))
        PASSED=$((PASSED + 1))
    else
        echo -e "${RED}✗ INVALID${NC}"
        SH_FAIL=$((SH_FAIL + 1))
        FAILED=$((FAILED + 1))
    fi
done < <(find "$ULTRON_ROOT" -name "*.sh" -type f -print0 2>/dev/null)

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Build Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "  File checks:    $((TOTAL - PY_COUNT - JSON_COUNT - SH_COUNT))"
echo -e "  Python files:   $PY_COUNT (${GREEN}$PY_PASS passed${NC}, ${RED}$PY_FAIL failed${NC})"
echo -e "  JSON files:     $JSON_COUNT (${GREEN}$JSON_PASS valid${NC}, ${RED}$JSON_FAIL invalid${NC})"
echo -e "  Shell scripts:  $SH_COUNT (${GREEN}$SH_PASS valid${NC}, ${RED}$SH_FAIL invalid${NC})"
echo -e "  ─────────────────────────────────"
echo -e "  Total checks:   $TOTAL"
echo -e "  ${GREEN}Passed:         $PASSED${NC}"
echo -e "  ${RED}Failed:         $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All $TOTAL checks passed! Build successful.${NC}"
    echo -e "${GREEN}  Ultron OS is ready for user launch.${NC}"
    exit 0
else
    echo -e "${RED}✗ $FAILED check(s) failed. Please review the log.${NC}"
    echo -e "  Log file: $LOG_FILE"
    exit 1
fi
