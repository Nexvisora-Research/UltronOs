#!/bin/bash
# Ultron OS - Automated ISO Build Script
# Builds a bootable ISO from project configuration
# Requires: root, debootstrap, xorriso, squashfs-tools

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$PROJECT_DIR/build/iso-workspace"
CHROOT_DIR="$BUILD_DIR/chroot"
ISO_DIR="$PROJECT_DIR/build/iso"
ISO_NAME="ultron-os-1.0.0-amd64.iso"
ISO_LABEL="ULTRON_OS_1_0_0"
UBUNTU_MIRROR="http://archive.ubuntu.com/ubuntu"
UBUNTU_RELEASE="noble"
ARCH="amd64"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[ULTRON BUILD]${NC} $1"; }
ok()   { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }

# Root check
if [ "$EUID" -ne 0 ]; then
    err "This script must be run as root (sudo)"
    exit 1
fi

# Dependency check
check_dep() {
    dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -q "install ok installed"
}

DEPS=(debootstrap xorriso squashfs-tools rsync grub-pc-bin grub-efi-amd64-bin isolinux syslinux-common)
MISSING=()
for dep in "${DEPS[@]}"; do
    if ! check_dep "$dep"; then
        MISSING+=("$dep")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    err "Missing dependencies: ${MISSING[*]}"
    echo "Install with: sudo apt install ${MISSING[*]}"
    exit 1
fi

# Clean previous build
log "Cleaning previous build..."
rm -rf "$BUILD_DIR" "$ISO_DIR"
mkdir -p "$BUILD_DIR" "$ISO_DIR" "$CHROOT_DIR"

# Step 1: Bootstrap base system
log "Step 1/12: Bootstrapping Ubuntu $UBUNTU_RELEASE base system..."
debootstrap --arch=$ARCH --variant=minbase "$UBUNTU_RELEASE" "$CHROOT_DIR" "$UBUNTU_MIRROR"
ok "Base system bootstrapped"

# Step 2: Mount virtual filesystems
log "Step 2/12: Mounting virtual filesystems..."
mount -t proc proc "$CHROOT_DIR/proc"
mount -t sysfs sysfs "$CHROOT_DIR/sys"
mount -o bind /dev "$CHROOT_DIR/dev"
mount -o bind /dev/pts "$CHROOT_DIR/dev/pts"
mount -t tmpfs tmpfs "$CHROOT_DIR/tmp"
ok "Filesystems mounted"

# Cleanup function
cleanup() {
    log "Unmounting remaining filesystems..."
    umount -l "$CHROOT_DIR/tmp" 2>/dev/null || true
    umount -l "$CHROOT_DIR/dev/pts" 2>/dev/null || true
    umount -l "$CHROOT_DIR/dev" 2>/dev/null || true
    umount -l "$CHROOT_DIR/sys" 2>/dev/null || true
    umount -l "$CHROOT_DIR/proc" 2>/dev/null || true
}
trap cleanup EXIT

# Step 3: Copy project files into chroot
log "Step 3/12: Copying project files into chroot..."
mkdir -p "$CHROOT_DIR/tmp/ultron"
rsync -a "$PROJECT_DIR/scripts/" "$CHROOT_DIR/tmp/ultron/scripts/"
rsync -a "$PROJECT_DIR/themes/" "$CHROOT_DIR/tmp/ultron/themes/"
rsync -a "$PROJECT_DIR/artwork/" "$CHROOT_DIR/tmp/ultron/artwork/"
rsync -a "$PROJECT_DIR/desktop-shell/" "$CHROOT_DIR/tmp/ultron/desktop-shell/"
rsync -a "$PROJECT_DIR/apps/" "$CHROOT_DIR/tmp/ultron/apps/"
rsync -a "$PROJECT_DIR/tools/" "$CHROOT_DIR/tmp/ultron/tools/"
rsync -a "$PROJECT_DIR/services/" "$CHROOT_DIR/tmp/ultron/services/"
rsync -a "$PROJECT_DIR/iso/calamares/" "$CHROOT_DIR/tmp/ultron/calamares/"
ok "Project files copied"

# Step 4: Configure chroot environment
log "Step 4/12: Configuring chroot environment..."
cp /etc/resolv.conf "$CHROOT_DIR/etc/resolv.conf"
cat > "$CHROOT_DIR/tmp/ultron-setup.sh" << 'SETUP'
#!/bin/bash
set -e

# Prevent interactive prompts
export DEBIAN_FRONTEND=noninteractive

# Install prerequisites first
apt update
apt install -y software-properties-common curl gpg

# Add Universe repository
apt-add-repository universe -y

# Update package lists
apt update

# Install core desktop packages
apt install -y \
    ubuntu-desktop-minimal \
    linux-generic \
    casper \
    gnome-shell gnome-session gdm3 mutter \
    gnome-control-center gnome-settings-daemon \
    gnome-terminal nautilus gedit \
    network-manager pulseaudio pipewire pipewire-pulse \
    bluez cups fonts-noto-color-emoji language-pack-en \
    flatpak gnome-tweaks gnome-software \
    timeshift file-roller gnome-calculator gnome-system-monitor gnome-disk-utility \
    git curl wget python3 python3-pip \
    build-essential meson ninja-build

# Install pre-installed applications
apt install -y \
    firefox \
    libreoffice-core libreoffice-writer libreoffice-calc libreoffice-impress \
    vlc celluloid rhythmbox \
    gimp inkscape eog

# Add Brave Browser repository
mkdir -p /usr/share/keyrings
curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg \
    https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" \
    > /etc/apt/sources.list.d/brave-browser-release.list
apt update
apt install -y brave-browser

# Install Flatpak and apps
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo || true
flatpak install -y flathub org.videolan.VLC com.github.tchx84.Flatseal --noninteractive || true

# Clean up apt cache
apt clean
rm -rf /var/lib/apt/lists/*
SETUP

chmod +x "$CHROOT_DIR/tmp/ultron-setup.sh"
ok "Setup script prepared"

# Step 5: Run setup in chroot
log "Step 5/12: Installing packages in chroot (this may take 15-30 minutes)..."
chroot "$CHROOT_DIR" /tmp/ultron-setup.sh
ok "Packages installed"

# Step 6: Install Ultron custom components
log "Step 6/12: Installing Ultron custom components..."
cat > "$CHROOT_DIR/tmp/ultron-install.sh" << 'INSTALL'
#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

# Create Ultron directories
mkdir -p /usr/share/ultron/artwork
mkdir -p /usr/share/themes/Ultron-Dark/gtk-4.0
mkdir -p /usr/share/icons/Ultron-Icons
mkdir -p /usr/share/cursors/Ultron-Cursor

# Copy artwork
cp -r /tmp/ultron/artwork/* /usr/share/ultron/artwork/ 2>/dev/null || true

# Copy GTK theme
if [ -d /tmp/ultron/themes/gtk ]; then
    cp -r /tmp/ultron/themes/gtk/* /usr/share/themes/Ultron-Dark/gtk-4.0/ 2>/dev/null || true
fi

# Copy cursor theme
if [ -d /tmp/ultron/themes/cursor ]; then
    cp -r /tmp/ultron/themes/cursor/* /usr/share/cursors/Ultron-Cursor/ 2>/dev/null || true
fi

# Copy icon theme
if [ -d /tmp/ultron/artwork/icons ]; then
    cp -r /tmp/ultron/artwork/icons/* /usr/share/icons/Ultron-Icons/ 2>/dev/null || true
fi

# Copy desktop files
find /tmp/ultron/apps -name "*.desktop" -exec cp {} /usr/share/applications/ \; 2>/dev/null || true
find /tmp/ultron/tools -name "*.desktop" -exec cp {} /usr/share/applications/ \; 2>/dev/null || true

# Copy systemd services
find /tmp/ultron -name "*.service" -exec cp {} /usr/lib/systemd/user/ \; 2>/dev/null || true

# Copy Calamares branding
if [ -d /tmp/ultron/calamares ]; then
    mkdir -p /etc/calamares/branding/ultron
    cp -r /tmp/ultron/calamares/* /etc/calamares/ 2>/dev/null || true
fi

# Copy Python applications
for app_dir in /tmp/ultron/apps/*/; do
    app_name=$(basename "$app_dir")
    if [ -d "$app_dir/src" ]; then
        mkdir -p "/opt/ultron/$app_name"
        cp -r "$app_dir/src" "/opt/ultron/$app_name/" 2>/dev/null || true
    fi
done

for tool_dir in /tmp/ultron/tools/*/; do
    tool_name=$(basename "$tool_dir")
    if [ -d "$tool_dir/src" ]; then
        mkdir -p "/opt/ultron/$tool_name"
        cp -r "$tool_dir/src" "/opt/ultron/$tool_name/" 2>/dev/null || true
    fi
done

for svc_dir in /tmp/ultron/services/*/; do
    svc_name=$(basename "$svc_dir")
    if [ -d "$svc_dir/src" ]; then
        mkdir -p "/opt/ultron/$svc_name"
        cp -r "$svc_dir/src" "/opt/ultron/$svc_name/" 2>/dev/null || true
    fi
done

# Set Brave as default browser
update-alternatives --install /usr/bin/x-www-browser x-www-browser /usr/bin/brave-browser 200 2>/dev/null || true

# Clean up
rm -rf /tmp/ultron
INSTALL

chmod +x "$CHROOT_DIR/tmp/ultron-install.sh"
chroot "$CHROOT_DIR" /tmp/ultron-install.sh
ok "Ultron components installed"

# Step 7: Configure system defaults
log "Step 7/12: Configuring system defaults..."
cat > "$CHROOT_DIR/tmp/ultron-config.sh" << 'CONFIG'
#!/bin/bash
set -e

# Configure hostname
echo "ultron-pc" > /etc/hostname

# Configure hosts
cat > /etc/hosts << 'EOF'
127.0.0.1   localhost
127.0.1.1   ultron-pc
::1         localhost ip6-localhost ip6-loopback
EOF

# Configure OS release
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

# Create default user skeleton
mkdir -p /etc/skel/.config
cat > /etc/skel/.config/ultron-defaults.conf << 'EOF'
[gtk]
theme=Ultron-Dark
icon-theme=Ultron-Icons
cursor-theme=Ultron-Cursor
font=Inter 11

[background]
picture-uri=file:///usr/share/ultron/artwork/wallpaper-default.svg
picture-uri-dark=file:///usr/share/ultron/artwork/wallpaper-default.svg
EOF

# Enable services (ignore chroot warnings)
systemctl enable gdm3 2>/dev/null || true
systemctl enable NetworkManager 2>/dev/null || true
systemctl enable bluetooth 2>/dev/null || true
systemctl enable cups 2>/dev/null || true

# Pipewire is enabled by default in Ubuntu 24.04 via user session
# No need to enable system services for it

# Set up GRUB
cat > /etc/default/grub << 'EOF'
GRUB_DEFAULT=0
GRUB_TIMEOUT=10
GRUB_DISTRIBUTOR="Ultron OS"
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
GRUB_CMDLINE_LINUX=""
EOF
update-grub 2>/dev/null || true

CONFIG

chmod +x "$CHROOT_DIR/tmp/ultron-config.sh"
chroot "$CHROOT_DIR" /tmp/ultron-config.sh
ok "System configured"

# Step 8: Set up live session
log "Step 8/12: Setting up live session..."
mkdir -p "$CHROOT_DIR/etc/casper"

# Casper configuration
cat > "$CHROOT_DIR/etc/casper.conf" << 'EOF'
FLAVOUR="ultron"
USERNAME="ultron"
HOSTNAME="ultron-live"
LIVE_MEDIA_PATH=/casper
EOF

# Create live user
chroot "$CHROOT_DIR" useradd -m -s /bin/bash -G sudo,adm,cdrom,dip,plugdev,lpadmin ultron
chroot "$CHROOT_DIR" bash -c 'echo "ultron:ultron" | chpasswd'
chroot "$CHROOT_DIR" bash -c 'echo "ultron ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'

# Auto-login for live session
mkdir -p "$CHROOT_DIR/etc/gdm3"
cat > "$CHROOT_DIR/etc/gdm3/custom.conf" << 'EOF'
[daemon]
AutomaticLoginEnable=true
AutomaticLogin=ultron
EOF
ok "Live session configured"

# Step 9: Build squashfs
log "Step 9/12: Building squashfs filesystem..."
mkdir -p "$BUILD_DIR/iso/casper"

# Unmount virtual filesystems before squashfs
umount -l "$CHROOT_DIR/tmp" 2>/dev/null || true
umount -l "$CHROOT_DIR/dev/pts" 2>/dev/null || true
umount -l "$CHROOT_DIR/dev" 2>/dev/null || true
umount -l "$CHROOT_DIR/sys" 2>/dev/null || true
umount -l "$CHROOT_DIR/proc" 2>/dev/null || true

# Build squashfs excluding virtual filesystems
mksquashfs "$CHROOT_DIR" "$BUILD_DIR/iso/casper/filesystem.squashfs" \
    -comp zstd -b 1048576 -noappend -Xcompression-level 3 \
    -e proc sys dev run tmp
ok "Squashfs built"

# Generate filesystem manifest
chroot "$CHROOT_DIR" dpkg-query -W --showformat='${Package} ${Version}\n' > "$BUILD_DIR/iso/casper/filesystem.manifest"
cp "$BUILD_DIR/iso/casper/filesystem.manifest" "$BUILD_DIR/iso/casper/filesystem.manifest-desktop"

# Step 10: Prepare ISO structure
log "Step 10/12: Preparing ISO structure..."
mkdir -p "$BUILD_DIR/iso/isolinux"
mkdir -p "$BUILD_DIR/iso/boot/grub"

# Copy kernel and initrd
cp "$CHROOT_DIR/boot/vmlinuz"* "$BUILD_DIR/iso/casper/vmlinuz"
cp "$CHROOT_DIR/boot/initrd"* "$BUILD_DIR/iso/casper/initrd"

# GRUB configuration
cat > "$BUILD_DIR/iso/boot/grub/grub.cfg" << 'GRUB'
set default=0
set timeout=10

menuentry "Try or Install Ultron OS" {
    linux /casper/vmlinuz boot=casper quiet splash --
    initrd /casper/initrd
}

menuentry "Install Ultron OS (Safe Graphics)" {
    linux /casper/vmlinuz boot=casper quiet splash nomodeset --
    initrd /casper/initrd
}

menuentry "Check disc for defects" {
    linux /casper/vmlinuz boot=casper integrity-check quiet splash --
    initrd /casper/initrd
}

menuentry "Boot from first hard disk" {
    set root=(hd0)
    chainloader +1
}
GRUB

# ISOLINUX configuration (for BIOS)
cp /usr/lib/ISOLINUX/isolinux.bin "$BUILD_DIR/iso/isolinux/"
cp /usr/lib/syslinux/modules/bios/ldlinux.c32 "$BUILD_DIR/iso/isolinux/"

cat > "$BUILD_DIR/iso/isolinux/isolinux.cfg" << 'ISOLINUX'
DEFAULT vesamenu.c32
PROMPT 0
TIMEOUT 100

MENU TITLE Ultron OS 1.0.0

LABEL live
    MENU LABEL Try or Install Ultron OS
    KERNEL /casper/vmlinuz
    APPEND initrd=/casper/initrd boot=casper quiet splash --
    INITRD /casper/initrd

LABEL safe
    MENU LABEL Install Ultron OS (Safe Graphics)
    KERNEL /casper/vmlinuz
    APPEND initrd=/casper/initrd boot=casper quiet splash nomodeset --
    INITRD /casper/initrd

LABEL check
    MENU LABEL Check disc for defects
    KERNEL /casper/vmlinuz
    APPEND initrd=/casper/initrd boot=casper integrity-check quiet splash --
    INITRD /casper/initrd
ISOLINUX

# MD5 checksums
cd "$BUILD_DIR/iso"
find . -type f -print0 | xargs -0 md5sum > md5sum.txt 2>/dev/null || true
cd "$PROJECT_DIR"
ok "ISO structure prepared"

# Step 11: Build ISO
log "Step 11/12: Building ISO image..."
xorriso -as mkisofs \
    -isohybrid-mbr /usr/lib/grub/i386-pc/eltorito.img \
    -c isolinux/boot.cat \
    -b isolinux/isolinux.bin \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    -eltorito-alt-boot \
    -e boot/grub/efi.img \
    -no-emul-boot \
    -isohybrid-gpt-basdat \
    -V "$ISO_LABEL" \
    -o "$ISO_DIR/$ISO_NAME" \
    "$BUILD_DIR/iso"
ok "ISO image built"

# Step 12: Generate checksums
log "Step 12/12: Generating checksums..."
cd "$ISO_DIR"
sha256sum "$ISO_NAME" > "${ISO_NAME}.sha256"
md5sum "$ISO_NAME" > "${ISO_NAME}.md5"
cd "$PROJECT_DIR"
ok "Checksums generated"

# Summary
ISO_SIZE=$(du -h "$ISO_DIR/$ISO_NAME" | cut -f1)
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Build Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "  ISO:         ${GREEN}$ISO_DIR/$ISO_NAME${NC}"
echo -e "  Size:        ${GREEN}$ISO_SIZE${NC}"
echo -e "  SHA256:      ${GREEN}$(cat "$ISO_DIR/${ISO_NAME}.sha256" | awk '{print $1}')${NC}"
echo -e "  MD5:         ${GREEN}$(cat "$ISO_DIR/${ISO_NAME}.md5" | awk '{print $1}')${NC}"
echo ""
echo -e "${GREEN}✓ ISO build complete!${NC}"
echo ""
echo "  Test with QEMU:"
echo "    qemu-system-x86_64 -boot d -cdrom $ISO_DIR/$ISO_NAME -m 4096 -enable-kvm"
echo ""
echo "  Write to USB:"
echo "    sudo dd if=$ISO_DIR/$ISO_NAME of=/dev/sdX bs=4M status=progress oflag=sync"
echo ""
