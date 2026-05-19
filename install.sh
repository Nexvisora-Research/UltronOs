#!/bin/bash
# Ultron OS - Installation Script
# Installs all components system-wide

set -e

ULTRON_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREFIX="/usr"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Ultron OS - Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check for root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (sudo ./install.sh)${NC}"
    exit 1
fi

echo -e "${YELLOW}Installing Ultron OS components...${NC}"
echo ""

# Phase 1: Foundation
echo -e "${BLUE}[Phase 1] Installing Foundation...${NC}"

# Install themes
echo "  Installing GTK themes..."
mkdir -p $PREFIX/share/themes/Ultron-Dark/gtk-4.0
mkdir -p $PREFIX/share/themes/Ultron-Light/gtk-4.0
cp -r "$ULTRON_ROOT/themes/gtk/Ultron-Dark/gtk-4.0/gtk.css" $PREFIX/share/themes/Ultron-Dark/gtk-4.0/
cp -r "$ULTRON_ROOT/themes/gtk/Ultron-Light/gtk-4.0/gtk.css" $PREFIX/share/themes/Ultron-Light/gtk-4.0/
cp "$ULTRON_ROOT/themes/gtk/Ultron-Dark/index.theme" $PREFIX/share/themes/Ultron-Dark/
cp "$ULTRON_ROOT/themes/gtk/Ultron-Light/index.theme" $PREFIX/share/themes/Ultron-Light/

# Install artwork
echo "  Installing artwork..."
mkdir -p $PREFIX/share/ultron/artwork
cp -r "$ULTRON_ROOT/artwork/"* $PREFIX/share/ultron/artwork/

# Install icons
echo "  Installing icon theme..."
mkdir -p $PREFIX/share/icons/Ultron-Icons
cp -r "$ULTRON_ROOT/artwork/icons/"* $PREFIX/share/icons/Ultron-Icons/

# Install wallpapers
echo "  Installing wallpapers..."
mkdir -p $PREFIX/share/backgrounds
cp "$ULTRON_ROOT/artwork/wallpaper-default.svg" $PREFIX/share/backgrounds/ultron-default.svg

# Install welcome wizard
echo "  Installing welcome wizard..."
mkdir -p $PREFIX/share/ultron-welcome
cp "$ULTRON_ROOT/apps/ultron-welcome/ultron-welcome.py" $PREFIX/bin/ultron-welcome
chmod +x $PREFIX/bin/ultron-welcome
cp "$ULTRON_ROOT/apps/ultron-welcome/ultron-welcome.desktop" $PREFIX/share/applications/

# Install Calamares branding
echo "  Installing Calamares branding..."
mkdir -p /etc/calamares/branding/ultron/slides
cp -r "$ULTRON_ROOT/iso/calamares/"* /etc/calamares/

echo -e "${GREEN}  ✓ Phase 1 complete${NC}"
echo ""

# Phase 2: Desktop Experience
echo -e "${BLUE}[Phase 2] Installing Desktop Shell...${NC}"

# Install GNOME Shell extension
echo "  Installing GNOME Shell extension..."
EXTENSION_UUID="ultron-shell@ultron.org"
EXTENSION_DIR="$PREFIX/share/gnome-shell/extensions/$EXTENSION_UUID"
mkdir -p $EXTENSION_DIR/components
mkdir -p $EXTENSION_DIR/schemas

cp "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/metadata.json" $EXTENSION_DIR/
cp "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/extension.js" $EXTENSION_DIR/
cp "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/prefs.js" $EXTENSION_DIR/
cp "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/stylesheet.css" $EXTENSION_DIR/
cp "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/schemas/"* $EXTENSION_DIR/schemas/
cp -r "$ULTRON_ROOT/desktop-shell/ultron-shell-extension/components/"* $EXTENSION_DIR/components/

# Compile GSettings schemas
glib-compile-schemas $PREFIX/share/glib-2.0/schemas/ 2>/dev/null || true

echo -e "${GREEN}  ✓ Phase 2 complete${NC}"
echo ""

# Phase 3: System Tools
echo -e "${BLUE}[Phase 3] Installing System Tools...${NC}"

# Install settings app
echo "  Installing Settings..."
mkdir -p $PREFIX/share/ultron-settings/src/pages
cp -r "$ULTRON_ROOT/apps/ultron-settings/src/"* $PREFIX/share/ultron-settings/src/
cp "$ULTRON_ROOT/apps/ultron-settings/ultron-settings" $PREFIX/bin/ultron-settings
chmod +x $PREFIX/bin/ultron-settings
cp "$ULTRON_ROOT/apps/ultron-settings/data/org.ultron.settings.desktop" $PREFIX/share/applications/

# Install control center
echo "  Installing Control Center..."
mkdir -p $PREFIX/share/ultron-control-center
cp "$ULTRON_ROOT/apps/ultron-control-center/src/control-center.py" $PREFIX/share/ultron-control-center/
cp "$ULTRON_ROOT/apps/ultron-control-center/ultron-control-center" $PREFIX/bin/ultron-control-center
chmod +x $PREFIX/bin/ultron-control-center
cp "$ULTRON_ROOT/apps/ultron-control-center/data/org.ultron.control-center.desktop" $PREFIX/share/applications/

# Install Nautilus extension
echo "  Installing Nautilus extension..."
mkdir -p $PREFIX/share/nautilus-python/extensions/ultron-nautilus
cp -r "$ULTRON_ROOT/packages/nautilus-extension/ultron-nautilus/"* $PREFIX/share/nautilus-python/extensions/ultron-nautilus/

echo -e "${GREEN}  ✓ Phase 3 complete${NC}"
echo ""

# Phase 4: Ecosystem
echo -e "${BLUE}[Phase 4] Installing Ecosystem...${NC}"

# Install app store
echo "  Installing App Store..."
mkdir -p $PREFIX/share/ultron-store/src/pages
cp -r "$ULTRON_ROOT/apps/ultron-store/src/"* $PREFIX/share/ultron-store/src/
cp "$ULTRON_ROOT/apps/ultron-store/ultron-store" $PREFIX/bin/ultron-store
chmod +x $PREFIX/bin/ultron-store
cp "$ULTRON_ROOT/apps/ultron-store/data/org.ultron.store.desktop" $PREFIX/share/applications/

# Install updater
echo "  Installing Updater..."
mkdir -p $PREFIX/share/ultron-updater
cp "$ULTRON_ROOT/apps/ultron-updater/src/updater.py" $PREFIX/share/ultron-updater/
cp "$ULTRON_ROOT/apps/ultron-updater/ultron-updater" $PREFIX/bin/ultron-updater
chmod +x $PREFIX/bin/ultron-updater
cp "$ULTRON_ROOT/apps/ultron-updater/data/org.ultron.updater.desktop" $PREFIX/share/applications/

# Install driver manager
echo "  Installing Driver Manager..."
mkdir -p $PREFIX/share/ultron-driver
cp "$ULTRON_ROOT/apps/ultron-driver/src/driver-manager.py" $PREFIX/share/ultron-driver/
cp "$ULTRON_ROOT/apps/ultron-driver/ultron-driver" $PREFIX/bin/ultron-driver
chmod +x $PREFIX/bin/ultron-driver
cp "$ULTRON_ROOT/apps/ultron-driver/data/org.ultron.driver.desktop" $PREFIX/share/applications/

# Install cloud service
echo "  Installing Cloud Service..."
mkdir -p $PREFIX/share/ultron-cloud
cp -r "$ULTRON_ROOT/services/ultron-cloud/src/"* $PREFIX/share/ultron-cloud/
cp "$ULTRON_ROOT/services/ultron-cloud/ultron-cloud.service" $PREFIX/lib/systemd/user/

# Install AI assistant
echo "  Installing AI Assistant..."
mkdir -p $PREFIX/share/ultron-ai
cp "$ULTRON_ROOT/apps/ultron-ai/src/ai_assistant.py" $PREFIX/share/ultron-ai/
cp "$ULTRON_ROOT/apps/ultron-ai/ultron-ai.service" $PREFIX/lib/systemd/user/

echo -e "${GREEN}  ✓ Phase 4 complete${NC}"
echo ""

# Phase 5: Optimization
echo -e "${BLUE}[Phase 5] Installing Optimization Tools...${NC}"

# Install performance tuner
echo "  Installing Performance Tuner..."
mkdir -p $PREFIX/share/ultron-tune
cp "$ULTRON_ROOT/tools/ultron-tune/src/performance_tuner.py" $PREFIX/share/ultron-tune/
cp "$ULTRON_ROOT/tools/ultron-tune/ultron-tune" $PREFIX/bin/ultron-tune
chmod +x $PREFIX/bin/ultron-tune

# Install security hardener
echo "  Installing Security Hardener..."
mkdir -p $PREFIX/share/ultron-security
cp "$ULTRON_ROOT/tools/ultron-security/src/security_hardener.py" $PREFIX/share/ultron-security/
cp "$ULTRON_ROOT/tools/ultron-security/ultron-security" $PREFIX/bin/ultron-security
chmod +x $PREFIX/bin/ultron-security

# Install power manager
echo "  Installing Power Manager..."
mkdir -p $PREFIX/share/ultron-power
cp "$ULTRON_ROOT/tools/ultron-power/src/power_manager.py" $PREFIX/share/ultron-power/
cp "$ULTRON_ROOT/tools/ultron-power/ultron-power" $PREFIX/bin/ultron-power
chmod +x $PREFIX/bin/ultron-power
cp "$ULTRON_ROOT/tools/ultron-power/ultron-power.service" $PREFIX/lib/systemd/system/

# Install system monitor
echo "  Installing System Monitor..."
mkdir -p $PREFIX/share/ultron-monitor
cp "$ULTRON_ROOT/tools/ultron-monitor/src/system_monitor.py" $PREFIX/share/ultron-monitor/
cp "$ULTRON_ROOT/tools/ultron-monitor/ultron-monitor" $PREFIX/bin/ultron-monitor
chmod +x $PREFIX/bin/ultron-monitor
cp "$ULTRON_ROOT/tools/ultron-monitor/ultron-monitor.service" $PREFIX/lib/systemd/system/

# Install benchmark
echo "  Installing Benchmark Tools..."
mkdir -p $PREFIX/share/ultron-bench
cp -r "$ULTRON_ROOT/tools/ultron-bench/src/"* $PREFIX/share/ultron-bench/
cp "$ULTRON_ROOT/tools/ultron-bench/ultron-bench" $PREFIX/bin/ultron-bench
chmod +x $PREFIX/bin/ultron-bench

echo -e "${GREEN}  ✓ Phase 5 complete${NC}"
echo ""

# Phase 6: Expansion
echo -e "${BLUE}[Phase 6] Installing Expansion Tools...${NC}"

# Install device manager
echo "  Installing Device Manager..."
mkdir -p $PREFIX/share/ultron-device
cp "$ULTRON_ROOT/tools/ultron-device/src/device_manager.py" $PREFIX/share/ultron-device/
cp "$ULTRON_ROOT/tools/ultron-device/ultron-device" $PREFIX/bin/ultron-device
chmod +x $PREFIX/bin/ultron-device

# Install mobile UI
echo "  Installing Mobile UI..."
mkdir -p $PREFIX/share/ultron-mobile
cp "$ULTRON_ROOT/apps/ultron-mobile/src/adaptive_ui.py" $PREFIX/share/ultron-mobile/

# Install voice assistant
echo "  Installing Voice Assistant..."
mkdir -p $PREFIX/share/ultron-voice
cp "$ULTRON_ROOT/apps/ultron-voice/src/voice_assistant.py" $PREFIX/share/ultron-voice/
cp "$ULTRON_ROOT/apps/ultron-voice/ultron-voice" $PREFIX/bin/ultron-voice
chmod +x $PREFIX/bin/ultron-voice

# Install workflow engine
echo "  Installing Workflow Engine..."
mkdir -p $PREFIX/share/ultron-workflow
cp "$ULTRON_ROOT/services/ultron-workflow/src/workflow_engine.py" $PREFIX/share/ultron-workflow/
cp "$ULTRON_ROOT/services/ultron-workflow/ultron-workflow" $PREFIX/bin/ultron-workflow
chmod +x $PREFIX/bin/ultron-workflow
cp "$ULTRON_ROOT/services/ultron-workflow/ultron-workflow.service" $PREFIX/lib/systemd/user/

# Install gesture controller
echo "  Installing Gesture Controller..."
mkdir -p $PREFIX/share/ultron-gesture
cp "$ULTRON_ROOT/tools/ultron-gesture/src/gesture_controller.py" $PREFIX/share/ultron-gesture/
cp "$ULTRON_ROOT/tools/ultron-gesture/ultron-gesture" $PREFIX/bin/ultron-gesture
chmod +x $PREFIX/bin/ultron-gesture

# Install device sync
echo "  Installing Device Sync..."
mkdir -p $PREFIX/share/ultron-sync
cp "$ULTRON_ROOT/services/ultron-sync/src/device_sync.py" $PREFIX/share/ultron-sync/
cp "$ULTRON_ROOT/services/ultron-sync/ultron-sync" $PREFIX/bin/ultron-sync
chmod +x $PREFIX/bin/ultron-sync
cp "$ULTRON_ROOT/services/ultron-sync/ultron-sync.service" $PREFIX/lib/systemd/user/

echo -e "${GREEN}  ✓ Phase 6 complete${NC}"
echo ""

# Create Ultron config directory
echo -e "${YELLOW}Creating configuration directories...${NC}"
mkdir -p /etc/ultron
mkdir -p /etc/ultron/tune
mkdir -p /etc/ultron/security
mkdir -p /etc/ultron/power
mkdir -p /etc/ultron/device

# Set up default configurations
echo -e "${YELLOW}Setting up default configurations...${NC}"

# Enable GNOME Shell extension
echo "  Enabling Ultron Shell extension..."
gnome-extensions enable ultron-shell@ultron.org 2>/dev/null || true

# Enable systemd services
echo "  Enabling system services..."
systemctl daemon-reload
systemctl enable ultron-power 2>/dev/null || true
systemctl enable ultron-monitor 2>/dev/null || true

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Installation Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}Ultron OS 1.0.0 has been installed successfully.${NC}"
echo ""
echo -e "Installed components:"
echo -e "  • GTK Themes (Dark/Light)"
echo -e "  • GNOME Shell Extension"
echo -e "  • Ultron Settings"
echo -e "  • Ultron Control Center"
echo -e "  • Ultron App Store"
echo -e "  • Ultron Updater"
echo -e "  • Ultron Driver Manager"
echo -e "  • Cloud Service"
echo -e "  • AI Assistant"
echo -e "  • Performance Tuner"
echo -e "  • Security Hardener"
echo -e "  • Power Manager"
echo -e "  • System Monitor"
echo -e "  • Benchmark Tools"
echo -e "  • Device Manager"
echo -e "  • Voice Assistant"
echo -e "  • Workflow Engine"
echo -e "  • Gesture Controller"
echo -e "  • Device Sync"
echo ""
echo -e "${YELLOW}Please restart GNOME Shell or log out and back in to apply changes.${NC}"
echo -e "${YELLOW}For Wayland: Log out and log back in.${NC}"
echo -e "${YELLOW}For X11: Press Alt+F2, type 'r', and press Enter.${NC}"
echo ""
