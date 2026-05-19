#!/bin/bash
# Ultron OS - Base System Setup Script
# Configures Ubuntu 24.04 LTS base system

set -e

echo "=== Ultron OS Base System Setup ==="

# Update system
echo "[1/8] Updating system packages..."
apt update && apt upgrade -y

# Install core system packages
echo "[2/8] Installing core system packages..."
apt install -y \
    build-essential \
    git \
    curl \
    wget \
    zip \
    unzip \
    pkg-config \
    meson \
    ninja-build \
    cmake \
    autoconf \
    automake \
    libtool

# Install GNOME and Wayland dependencies
echo "[3/8] Installing GNOME/Wayland dependencies..."
apt install -y \
    gnome-shell \
    gnome-shell-extensions \
    gnome-tweaks \
    mutter \
    wayland-protocols \
    libwayland-dev \
    libgtk-4-dev \
    libadwaita-1-dev \
    gir1.2-gtk-4.0 \
    gir1.2-adw-1 \
    gsettings-desktop-schemas \
    gsettings-desktop-schemas-dev

# Install Python and development tools
echo "[4/8] Installing Python and development tools..."
apt install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    python3-gi \
    python3-gi-cairo

# Install Flatpak and AppImage support
echo "[5/8] Installing Flatpak and AppImage support..."
apt install -y flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Install AppImage support
wget -O /usr/local/bin/appimagetool "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
chmod +x /usr/local/bin/appimagetool

# Install pre-installed applications
echo "[6/8] Installing pre-installed applications..."

# Install Brave Browser
echo "  Installing Brave Browser..."
curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | tee /etc/apt/sources.list.d/brave-browser-release.list
apt update
apt install -y brave-browser

# Install essential applications
echo "  Installing essential applications..."
apt install -y \
    vlc \
    gimp \
    inkscape \
    libreoffice \
    file-roller \
    gnome-calculator \
    gnome-system-monitor \
    timeshift \
    git \
    curl \
    wget

# Install Flatpak applications
echo "  Installing Flatpak applications..."
flatpak install -y flathub \
    org.videolan.VLC \
    com.github.tchx84.Flatseal \
    --noninteractive || true

# Configure Wayland as default display server
echo "[7/8] Configuring Wayland as default display server..."
cat > /etc/gdm3/custom.conf << 'EOF'
[daemon]
WaylandEnable=true
DefaultSession=gnome.desktop
EOF

# Install Rust toolchain for performance-critical components
echo "[8/8] Installing Rust toolchain..."
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
source $HOME/.cargo/env

# Set up Ultron system directories
echo "[9/9] Setting up Ultron system directories..."
mkdir -p /etc/ultron
mkdir -p /usr/share/ultron
mkdir -p /usr/share/ultron/themes
mkdir -p /usr/share/ultron/artwork
mkdir -p /usr/share/ultron/config

echo "=== Base system setup complete ==="
echo "Reboot recommended to apply Wayland configuration"
