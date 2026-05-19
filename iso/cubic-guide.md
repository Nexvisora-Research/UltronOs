# Cubic (Custom Ubuntu ISO Creator) Configuration
# This file documents the steps to build the Ultron OS ISO using Cubic

# Step 1: Install Cubic
# sudo apt-add-repository universe
# sudo apt update
# sudo apt install cubic

# Step 2: Launch Cubic
# cubic

# Step 3: Select original Ubuntu 24.04 LTS ISO
# Download from: https://releases.ubuntu.com/24.04/

# Step 4: In the Cubic terminal, run the following commands:

# Add Ultron repository
# echo "deb [trusted=yes] https://ultron.org/repo ./" > /etc/apt/sources.list.d/ultron.list

# Update and install Ultron packages
# apt update
# apt install -y ultron-gtk-theme ultron-icon-theme ultron-cursor-theme ultron-welcome

# Apply Ultron branding
# cp -r /path/to/ultron/artwork/* /usr/share/ultron/artwork/
# cp -r /path/to/ultron/themes/* /usr/share/themes/
# cp -r /path/to/ultron/artwork/icons/* /usr/share/icons/Ultron-Icons/

# Configure default settings
# gsettings set org.gnome.desktop.interface gtk-theme "Ultron-Dark"
# gsettings set org.gnome.desktop.interface icon-theme "Ultron-Icons"
# gsettings set org.gnome.desktop.background picture-uri "file:///usr/share/ultron/artwork/wallpaper-default.svg"

# Install Calamares with Ultron branding
# apt install -y calamares
# cp -r /path/to/ultron/iso/calamares/* /etc/calamares/

# Configure autostart for welcome wizard
# cp /path/to/ultron/apps/ultron-welcome/ultron-welcome.desktop /etc/xdg/autostart/

# Clean up
# apt clean
# rm -rf /tmp/*
# rm -rf /var/lib/apt/lists/*

# Step 5: Generate ISO
# Use Cubic's GUI to generate the final ISO

# Step 6: Test ISO
# qemu-system-x86_64 -boot d -cdrom ultron-os-1.0.0.iso -m 4096 -enable-kvm

# Step 7: Create bootable USB
# dd if=ultron-os-1.0.0.iso of=/dev/sdX bs=4M status=progress oflag=sync
