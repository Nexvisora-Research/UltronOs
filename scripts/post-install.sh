#!/bin/bash
# Ultron OS - Post-Installation Configuration Script
# Applies Ultron branding and system settings after installation

set -e

echo "=== Ultron OS Post-Installation Configuration ==="

# Apply Ultron GTK theme
echo "[1/6] Applying Ultron GTK theme..."
gsettings set org.gnome.desktop.interface gtk-theme "Ultron-Dark"
gsettings set org.gnome.desktop.interface icon-theme "Ultron-Icons"
gsettings set org.gnome.desktop.interface cursor-theme "Ultron-Cursor"

# Configure default applications
echo "[2/6] Configuring default applications..."
gsettings set org.gnome.shell favorite-apps "['brave-browser.desktop', 'ultron-store.desktop', 'ultron-settings.desktop', 'org.gnome.Nautilus.desktop', 'org.gnome.TextEditor.desktop', 'org.gnome.Terminal.desktop', 'vlc.desktop', 'libreoffice-startcenter.desktop']"

# Set Brave as default browser
echo "  Setting Brave as default browser..."
xdg-settings set default-web-browser brave-browser.desktop 2>/dev/null || true

# Enable Wayland optimizations
echo "[3/6] Enabling Wayland optimizations..."
gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer']"

# Configure power management
echo "[4/6] Configuring power management..."
gsettings set org.gnome.settings-daemon.plugins.power power-button-action 'interactive'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-type 'nothing'
gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-type 'suspend'

# Set up Ultron wallpaper
echo "[5/6] Setting up Ultron wallpaper..."
cp /usr/share/ultron/artwork/wallpaper-default.svg /usr/share/backgrounds/ultron-default.svg
gsettings set org.gnome.desktop.background picture-uri "file:///usr/share/backgrounds/ultron-default.svg"
gsettings set org.gnome.desktop.background picture-uri-dark "file:///usr/share/backgrounds/ultron-default.svg"

# Configure system branding
echo "[6/6] Configuring system branding..."
# Update OS release information
cat > /etc/os-release << 'EOF'
NAME="Ultron OS"
VERSION="1.0.0"
ID=ultron
ID_LIKE=ubuntu
PRETTY_NAME="Ultron OS 1.0.0"
VERSION_ID="1.0.0"
HOME_URL="https://ultron.org"
SUPPORT_URL="https://ultron.org/support"
BUG_REPORT_URL="https://ultron.org/bugs"
PRIVACY_POLICY_URL="https://ultron.org/privacy"
VERSION_CODENAME=noble
UBUNTU_CODENAME=noble
EOF

echo "=== Post-Installation Configuration Complete ==="
echo "Please reboot to apply all changes"
