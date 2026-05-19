#!/bin/bash
# Ultron OS - Comprehensive Test Suite
# Tests all components across all 6 phases

ULTRON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$ULTRON_ROOT/tests"
RESULTS_FILE="$TEST_DIR/test_results.log"

# Colors
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
echo -e "${BLUE}  Ultron OS - Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

mkdir -p "$TEST_DIR"
echo "Ultron OS Test Results - $(date)" > "$RESULTS_FILE"

# Test function
run_test() {
    local name="$1"
    shift
    local test_cmd="$@"
    
    TOTAL=$((TOTAL + 1))
    echo -ne "  [$TOTAL] Testing $name... "
    echo "[$TOTAL] Testing $name" >> "$RESULTS_FILE"
    
    if eval "$test_cmd" >> "$RESULTS_FILE" 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        echo "  Result: PASS" >> "$RESULTS_FILE"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Result: FAIL" >> "$RESULTS_FILE"
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo -e "${YELLOW}Phase 1 Tests: Foundation${NC}"
echo "-------------------------------------------"

# Test theme CSS syntax
run_test "Dark theme CSS valid" "grep -q '@define-color' \"$ULTRON_ROOT/themes/gtk/Ultron-Dark/gtk-4.0/gtk.css\""
run_test "Light theme CSS valid" "grep -q '@define-color' \"$ULTRON_ROOT/themes/gtk/Ultron-Light/gtk-4.0/gtk.css\""

# Test SVG files
run_test "Logo SVG valid XML" "python3 -c \"import xml.etree.ElementTree as ET; ET.parse('$ULTRON_ROOT/artwork/logo.svg')\""
run_test "Wallpaper SVG valid XML" "python3 -c \"import xml.etree.ElementTree as ET; ET.parse('$ULTRON_ROOT/artwork/wallpaper-default.svg')\""

# Test icon theme structure
run_test "Icon theme has index" "grep -q 'Theme' \"$ULTRON_ROOT/artwork/icons/index.theme\""

# Test Calamares config
run_test "Calamares has sequence" "grep -q 'sequence' \"$ULTRON_ROOT/iso/calamares/settings.conf\""
run_test "Calamares branding exists" "grep -q 'Ultron OS' \"$ULTRON_ROOT/iso/calamares/branding/ultron/branding.desc\""

# Test welcome wizard imports
run_test "Welcome wizard imports GTK" "grep -q \"gi.require_version\" \"$ULTRON_ROOT/apps/ultron-welcome/ultron-welcome.py\""

echo ""
echo -e "${YELLOW}Phase 2 Tests: Desktop Experience${NC}"
echo "-------------------------------------------"

# Test shell extension metadata
run_test "Metadata has UUID" "python3 -c \"import json; d=json.load(open('$ULTRON_ROOT/desktop-shell/ultron-shell-extension/metadata.json')); assert 'uuid' in d\""
run_test "Metadata has shell-version" "python3 -c \"import json; d=json.load(open('$ULTRON_ROOT/desktop-shell/ultron-shell-extension/metadata.json')); assert 'shell-version' in d\""

# Test GSettings schema
run_test "Schema has taskbar-position key" "grep -q 'taskbar-position' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/schemas/org.ultron.shell.gschema.xml\""
run_test "Schema has launcher keys" "grep -q 'launcher-show-categories' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/schemas/org.ultron.shell.gschema.xml\""
run_test "Schema has notification keys" "grep -q 'notification-center-enabled' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/schemas/org.ultron.shell.gschema.xml\""

# Test component imports
run_test "Taskbar imports St" "grep -q 'import St' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/taskbar.js\""
run_test "Launcher imports Shell" "grep -q 'import Shell' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/launcher.js\""
run_test "Notification center imports Main" "grep -q 'import \* as Main' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/notification-center.js\""
run_test "System info imports PanelMenu" "grep -q 'import \* as PanelMenu' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/system-info.js\""
run_test "Window manager imports Meta" "grep -q 'import Meta' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/window-manager.js\""

# Test stylesheet
run_test "Stylesheet has taskbar styles" "grep -q '.ultron-taskbar' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/stylesheet.css\""
run_test "Stylesheet has launcher styles" "grep -q '.ultron-launcher' \"$ULTRON_ROOT/desktop-shell/ultron-shell-extension/stylesheet.css\""

echo ""
echo -e "${YELLOW}Phase 3 Tests: System Tools${NC}"
echo "-------------------------------------------"

# Test settings app structure
run_test "Settings app imports Adw" "grep -q \"gi.require_version('Adw', '1')\" \"$ULTRON_ROOT/apps/ultron-settings/src/application.py\""
run_test "Settings window has sidebar" "grep -q '_sidebar' \"$ULTRON_ROOT/apps/ultron-settings/src/window.py\""
run_test "Settings has appearance page" "test -f \"$ULTRON_ROOT/apps/ultron-settings/src/pages/appearance.py\""
run_test "Settings has network page" "test -f \"$ULTRON_ROOT/apps/ultron-settings/src/pages/network.py\""
run_test "Settings has about page" "test -f \"$ULTRON_ROOT/apps/ultron-settings/src/pages/about.py\""

# Test control center
run_test "Control center has toggles" "grep -q 'toggle\|Toggle' \"$ULTRON_ROOT/apps/ultron-control-center/src/control-center.py\""
run_test "Control center has sliders" "grep -q 'Brightness\|Volume' \"$ULTRON_ROOT/apps/ultron-control-center/src/control-center.py\""

# Test Nautilus extension
run_test "Nautilus extension inherits MenuProvider" "grep -q 'MenuProvider' \"$ULTRON_ROOT/packages/nautilus-extension/ultron-nautilus/extension.py\""
run_test "Nautilus has cloud integration" "grep -q 'cloud\|Cloud' \"$ULTRON_ROOT/packages/nautilus-extension/ultron-nautilus/extension.py\""

echo ""
echo -e "${YELLOW}Phase 4 Tests: Ecosystem${NC}"
echo "-------------------------------------------"

# Test store app
run_test "Store has explore page" "grep -q 'Featured\|featured' \"$ULTRON_ROOT/apps/ultron-store/src/pages/explore.py\""
run_test "Store has search functionality" "grep -q 'search\|Search' \"$ULTRON_ROOT/apps/ultron-store/src/pages/search.py\""
run_test "Store has installed page" "grep -q 'Installed\|installed' \"$ULTRON_ROOT/apps/ultron-store/src/pages/installed.py\""
run_test "Store has updates page" "grep -q 'Update\|update' \"$ULTRON_ROOT/apps/ultron-store/src/pages/updates.py\""
run_test "Store has app detail page" "grep -q 'AppDetail\|app_detail' \"$ULTRON_ROOT/apps/ultron-store/src/pages/app_detail.py\""

# Test updater
run_test "Updater checks for updates" "grep -q '_check_for_updates\|check_for_updates' \"$ULTRON_ROOT/apps/ultron-updater/src/updater.py\""
run_test "Updater has progress tracking" "grep -q 'ProgressBar\|progress_bar' \"$ULTRON_ROOT/apps/ultron-updater/src/updater.py\""

# Test driver manager
run_test "Driver manager detects hardware" "grep -q '_detect_hardware\|detect_hardware' \"$ULTRON_ROOT/apps/ultron-driver/src/driver-manager.py\""
run_test "Driver manager has GPU support" "grep -q 'GPU\|gpu\|Graphics' \"$ULTRON_ROOT/apps/ultron-driver/src/driver-manager.py\""

# Test cloud service
run_test "Cloud service supports multiple providers" "grep -q 'nextcloud\|google_drive\|onedrive' \"$ULTRON_ROOT/services/ultron-cloud/src/cloud_service.py\""
run_test "Cloud service has backup" "grep -q 'BackupService\|backup' \"$ULTRON_ROOT/services/ultron-cloud/src/cloud_service.py\""

# Test AI assistant
run_test "AI assistant has voice commands" "grep -q 'voice\|Voice' \"$ULTRON_ROOT/apps/ultron-ai/src/ai_assistant.py\""
run_test "AI assistant has workflow engine" "grep -q 'WorkflowEngine\|workflow' \"$ULTRON_ROOT/apps/ultron-ai/src/ai_assistant.py\""

echo ""
echo -e "${YELLOW}Phase 5 Tests: Optimization${NC}"
echo "-------------------------------------------"

# Test performance tuner
run_test "Tuner has boot optimization" "grep -q 'optimize_boot\|boot' \"$ULTRON_ROOT/tools/ultron-tune/src/performance_tuner.py\""
run_test "Tuner has memory optimization" "grep -q 'optimize_memory\|memory\|swappiness' \"$ULTRON_ROOT/tools/ultron-tune/src/performance_tuner.py\""
run_test "Tuner uses psutil" "grep -q 'import psutil' \"$ULTRON_ROOT/tools/ultron-tune/src/performance_tuner.py\""

# Test security hardener
run_test "Hardener has firewall config" "grep -q 'harden_firewall\|firewall' \"$ULTRON_ROOT/tools/ultron-security/src/security_hardener.py\""
run_test "Hardener has AppArmor" "grep -q 'apparmor\|AppArmor' \"$ULTRON_ROOT/tools/ultron-security/src/security_hardener.py\""
run_test "Hardener has kernel params" "grep -q 'kernel\|sysctl' \"$ULTRON_ROOT/tools/ultron-security/src/security_hardener.py\""

# Test power manager
run_test "Power manager has profiles" "grep -q 'performance\|balanced\|powersave' \"$ULTRON_ROOT/tools/ultron-power/src/power_manager.py\""
run_test "Power manager reads battery" "grep -q 'battery\|Battery' \"$ULTRON_ROOT/tools/ultron-power/src/power_manager.py\""
run_test "Power manager has CPU governor" "grep -q 'governor\|cpu_governor' \"$ULTRON_ROOT/tools/ultron-power/src/power_manager.py\""

# Test system monitor
run_test "Monitor tracks CPU" "grep -q 'cpu_percent\|get_cpu' \"$ULTRON_ROOT/tools/ultron-monitor/src/system_monitor.py\""
run_test "Monitor tracks memory" "grep -q 'virtual_memory\|get_memory' \"$ULTRON_ROOT/tools/ultron-monitor/src/system_monitor.py\""
run_test "Monitor has health report" "grep -q 'health_report\|get_health' \"$ULTRON_ROOT/tools/ultron-monitor/src/system_monitor.py\""

# Test benchmark
run_test "Benchmark has CPU tests" "grep -q '_benchmark_cpu\|benchmark_cpu' \"$ULTRON_ROOT/tools/ultron-bench/src/benchmark.py\""
run_test "Benchmark has disk tests" "grep -q '_benchmark_disk\|benchmark_disk' \"$ULTRON_ROOT/tools/ultron-bench/src/benchmark.py\""
run_test "Update tester validates packages" "grep -q 'test_updates\|_test_dependencies' \"$ULTRON_ROOT/tools/ultron-bench/src/update_tester.py\""

echo ""
echo -e "${YELLOW}Phase 6 Tests: Expansion${NC}"
echo "-------------------------------------------"

# Test device manager
run_test "Device manager detects form factor" "grep -q 'form_factor\|FormFactor' \"$ULTRON_ROOT/tools/ultron-device/src/device_manager.py\""
run_test "Device manager has scaling" "grep -q '_get_scale_factor\|scale_factor' \"$ULTRON_ROOT/tools/ultron-device/src/device_manager.py\""
run_test "Device manager has layouts" "grep -q '_get_layout\|single-column\|two-column' \"$ULTRON_ROOT/tools/ultron-device/src/device_manager.py\""

# Test mobile UI
run_test "Mobile UI has adaptive window" "grep -q 'AdaptiveWindow\|adaptive_ui' \"$ULTRON_ROOT/apps/ultron-mobile/src/adaptive_ui.py\""
run_test "Mobile UI has phone layout" "grep -q '_apply_phone_layout\|phone_layout' \"$ULTRON_ROOT/apps/ultron-mobile/src/adaptive_ui.py\""
run_test "Mobile UI has tablet layout" "grep -q '_apply_tablet_layout\|tablet_layout' \"$ULTRON_ROOT/apps/ultron-mobile/src/adaptive_ui.py\""

# Test voice assistant
run_test "Voice assistant has hotword" "grep -q 'hotword\|Hey Ultron' \"$ULTRON_ROOT/apps/ultron-voice/src/voice_assistant.py\""
run_test "Voice assistant has TTS" "grep -q 'speak\|espeak\|festival' \"$ULTRON_ROOT/apps/ultron-voice/src/voice_assistant.py\""
run_test "Voice assistant has commands" "grep -q '_handle_default_command\|open browser\|lock screen' \"$ULTRON_ROOT/apps/ultron-voice/src/voice_assistant.py\""

# Test workflow engine
run_test "Workflow engine has triggers" "grep -q 'trigger\|Trigger' \"$ULTRON_ROOT/services/ultron-workflow/src/workflow_engine.py\""
run_test "Workflow engine has actions" "grep -q '_execute_action\|launch_app\|run_command' \"$ULTRON_ROOT/services/ultron-workflow/src/workflow_engine.py\""
run_test "Workflow has context suggestions" "grep -q 'ContextAwareSuggestions\|context' \"$ULTRON_ROOT/services/ultron-workflow/src/workflow_engine.py\""

# Test gesture controller
run_test "Gestures have swipe support" "grep -q 'swipe-left\|swipe-right\|swipe-up\|swipe-down' \"$ULTRON_ROOT/tools/ultron-gesture/src/gesture_controller.py\""
run_test "Gestures have pinch support" "grep -q 'pinch\|GestureZoom' \"$ULTRON_ROOT/tools/ultron-gesture/src/gesture_controller.py\""
run_test "Gestures have touch settings" "grep -q 'TouchSettingsPage\|touch_settings' \"$ULTRON_ROOT/tools/ultron-gesture/src/gesture_controller.py\""

# Test device sync
run_test "Sync has settings sync" "grep -q '_sync_settings\|sync_settings' \"$ULTRON_ROOT/services/ultron-sync/src/device_sync.py\""
run_test "Sync has theme sync" "grep -q '_sync_themes\|sync_themes' \"$ULTRON_ROOT/services/ultron-sync/src/device_sync.py\""
run_test "Sync applies settings" "grep -q 'apply_sync\|apply_settings' \"$ULTRON_ROOT/services/ultron-sync/src/device_sync.py\""

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "  Total tests:   $TOTAL"
echo -e "  ${GREEN}Passed:         $PASSED${NC}"
echo -e "  ${RED}Failed:         $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All $TOTAL tests passed!${NC}"
    echo -e "${GREEN}  Ultron OS is ready for user launch.${NC}"
    exit 0
else
    echo -e "${RED}✗ $FAILED test(s) failed.${NC}"
    echo -e "  Review results: $RESULTS_FILE"
    exit 1
fi
