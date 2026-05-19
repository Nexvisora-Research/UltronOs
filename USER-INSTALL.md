# Ultron OS - Installation Guide

Welcome to Ultron OS! This guide will walk you through installing Ultron OS on your computer.

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **Processor** | 64-bit dual-core 2 GHz | 64-bit quad-core 3 GHz+ |
| **RAM** | 4 GB | 8 GB or more |
| **Storage** | 25 GB | 60 GB SSD or more |
| **Graphics** | Intel HD 4000 / AMD Radeon R5 | Dedicated GPU with 2 GB VRAM |
| **Display** | 1280×720 | 1920×1080 or higher |
| **USB Drive** | 4 GB | 8 GB USB 3.0 |
| **Internet** | Optional | Required for updates & apps |

**Supported Architectures:** x86_64 (AMD64)

---

## Step 1: Download Ultron OS

1. Visit the official website: **https://ultron.org/download**
2. Download the latest ISO image:
   - `ultron-os-1.0.0-amd64.iso` (~3.2 GB)
3. Verify the download (recommended):
   ```bash
   sha256sum ultron-os-1.0.0-amd64.iso
   ```
   Compare the output with the checksum on the download page.

---

## Step 2: Create Bootable USB

### Option A: Using Balena Etcher (Recommended)

1. Download [Balena Etcher](https://etcher.balena.io/)
2. Insert a USB drive (8 GB or larger)
3. Open Etcher and select the Ultron OS ISO
4. Select your USB drive
5. Click **Flash** and wait for completion

### Option B: Using Rufus (Windows)

1. Download [Rufus](https://rufus.ie/)
2. Insert your USB drive
3. Select the Ultron OS ISO under **Boot selection**
4. Keep default settings (GPT/UEFI)
5. Click **Start**

### Option C: Using Terminal (Linux)

```bash
# Identify your USB drive (BE CAREFUL - this will erase the drive!)
lsblk

# Write the ISO to the USB drive (replace /dev/sdX with your drive)
sudo dd if=ultron-os-1.0.0-amd64.iso of=/dev/sdX bs=4M status=progress oflag=sync

# Wait for completion and safely remove
sync
```

---

## Step 3: Boot from USB

1. **Insert the USB** into your computer
2. **Restart** your computer
3. **Enter the boot menu** by pressing one of these keys during startup:
   - `F12` — Dell, Lenovo, Toshiba
   - `F9` — HP
   - `F8` — ASUS, Acer
   - `ESC` — Some laptops
   - `F11` — MSI
4. Select your **USB drive** from the boot menu
5. If prompted, select **Try or Install Ultron OS**

> **Tip:** If your computer doesn't boot from USB, enter the BIOS/UEFI settings (usually `F2`, `Del`, or `F10`) and:
> - Disable **Secure Boot** (temporarily)
> - Set **USB** as the first boot device
> - Ensure **UEFI mode** is enabled (not Legacy/CSM)

---

## Step 4: Try or Install

Once booted, you'll see the Ultron OS welcome screen:

```
┌─────────────────────────────────────────┐
│                                         │
│        Welcome to Ultron OS             │
│                                         │
│   [ Try Ultron OS ]  [ Install ]        │
│                                         │
└─────────────────────────────────────────┘
```

- **Try Ultron OS** — Boot into a live session to test the OS without installing
- **Install** — Start the installation process immediately

We recommend trying first to ensure everything works with your hardware.

---

## Step 5: Installation Wizard (Calamares)

The installer will guide you through these steps:

### 5.1 — Welcome

- Select your **language**
- Click **Next**

### 5.2 — Location

- Select your **timezone** on the map
- Click **Next**

### 5.3 — Keyboard

- Select your **keyboard layout** (e.g., English (US))
- Test your layout in the preview box
- Click **Next**

### 5.4 — Partitions

Choose one of the following options:

| Option | Description |
|--------|-------------|
| **Erase disk** | Wipes the entire disk and installs Ultron OS (recommended for fresh installs) |
| **Install alongside** | Keeps your existing OS and adds Ultron OS (dual-boot) |
| **Replace partition** | Replaces a specific partition with Ultron OS |
| **Manual partitioning** | Advanced users — create custom partition layout |

**Recommended partition layout (manual):**

| Mount Point | Size | Type |
|-------------|------|------|
| `/boot/efi` | 512 MB | EFI System |
| `/` | 30+ GB | ext4 or btrfs |
| `swap` | Equal to RAM | swap |
| `/home` | Remaining space | ext4 or btrfs |

> **Warning:** "Erase disk" will permanently delete all data. Back up important files before proceeding.

### 5.5 — User Account

Fill in your details:

| Field | Example |
|-------|---------|
| **Full Name** | John Doe |
| **Computer Name** | john-ultron |
| **Username** | john |
| **Password** | (choose a strong password) |

Options:
- ☑ **Require password to log in** (recommended)
- ☐ **Log in automatically** (convenient but less secure)
- ☐ **Encrypt installation** (for sensitive data)

### 5.6 — Summary

Review your installation summary:

```
Installation Summary
────────────────────
Language:    English (US)
Timezone:    America/New_York
Keyboard:    English (US)
Partition:   Erase disk (sda)
User:        john @ john-ultron
```

Click **Install** to begin.

### 5.7 — Installation Progress

The installer will now:
1. Format the selected partitions
2. Copy system files
3. Install the bootloader (GRUB)
4. Configure the system

This takes **10–20 minutes** depending on your hardware.

---

## Step 6: Complete & Reboot

When installation finishes, you'll see:

```
┌─────────────────────────────────────────┐
│                                         │
│     Installation Complete!              │
│                                         │
│   [ Restart Now ]                       │
│                                         │
└─────────────────────────────────────────┘
```

1. Click **Restart Now**
2. **Remove the USB drive** when prompted
3. Your computer will reboot into Ultron OS

---

## Step 7: First Boot

### Welcome Wizard

On first boot, the **Ultron Welcome** wizard will launch:

1. **Welcome** — Introduction to Ultron OS
2. **Connect** — Connect to Wi-Fi or Ethernet
3. **Updates** — Check for system updates (recommended)
4. **Drivers** — Install proprietary drivers (NVIDIA, Wi-Fi, etc.)
5. **Apps** — Browse recommended applications
6. **Done** — Start using Ultron OS!

### Post-Setup

After the wizard completes:

```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install additional drivers (if needed)
ultron-driver-manager

# Install Flatpak apps
flatpak install flathub com.spotify.Client org.telegram.Desktop
```

---

## Troubleshooting

### Black Screen on Boot

1. At the GRUB menu, press `e` to edit boot options
2. Add `nomodeset` after `quiet splash`
3. Press `F10` to boot
4. After installation, install proper graphics drivers

### Wi-Fi Not Working

1. Connect via Ethernet temporarily
2. Open **Ultron Driver Manager**
3. Install proprietary Wi-Fi drivers
4. Reboot

### Dual Boot Not Showing Windows

```bash
sudo update-grub
```

This should detect and add Windows to the GRUB menu.

### Installation Fails

- Check the **installation log**: `/var/log/calamares/calamares.log`
- Ensure your USB drive is not corrupted (re-create it)
- Try a different USB port (preferably USB 3.0)
- Verify the ISO checksum before writing

### Secure Boot Issues

1. Enter BIOS/UEFI settings
2. Disable **Secure Boot**
3. Save and reboot
4. You can re-enable it after installing the signed bootloader

---

## After Installation

### Essential First Steps

1. **Update your system:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install media codecs:**
   ```bash
   sudo apt install ubuntu-restricted-extras
   ```

3. **Enable firewall:**
   ```bash
   sudo ufw enable
   ```

4. **Set up backups:**
   Open **Timeshift** from the application menu and create your first snapshot.

5. **Customize your desktop:**
   Open **Ultron Settings** to change themes, icons, fonts, and more.

### Useful Commands

| Command | Description |
|---------|-------------|
| `ultron-settings` | Open system settings |
| `ultron-store` | Open application store |
| `ultron-tune` | Performance tuner |
| `ultron-security` | Security hardening tool |
| `timeshift-gtk` | System backup & restore |
| `flatpak update` | Update Flatpak apps |

---

## Getting Help

- **Documentation:** https://ultron.org/docs
- **Community Forum:** https://ultron.org/forum
- **Bug Reports:** https://ultron.org/bugs
- **Support:** https://ultron.org/support
- **Developer:** Nexvisora Research

---

## License

Ultron OS is free software licensed under the **GNU General Public License v3.0**.
You are free to use, modify, and distribute it under the terms of the license.

**© 2026 Nexvisora Research. All rights reserved.**
