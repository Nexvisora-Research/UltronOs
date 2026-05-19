# Ultron OS - Phase 3: System Tools

## Overview

Phase 3 delivers the core system tools for Ultron OS, including a custom settings application, control center, and file manager enhancements.

## Components

### Ultron Settings (`apps/ultron-settings/`)

A comprehensive settings application built with GTK4 and Libadwaita.

**Pages:**
- **Appearance** - Theme, accent colors, fonts, wallpaper, window style
- **Network** - Wi-Fi, Ethernet, proxy, network tools
- **Bluetooth** - Device pairing, visibility, connected devices
- **Sound** - Output/input devices, volume, alerts, audio profiles
- **Display** - Resolution, refresh rate, night light, scaling
- **Notifications** - DND, app notifications, focus mode
- **Privacy & Security** - Screen lock, location, diagnostics, firewall
- **Accounts** - User profile, online accounts, login options
- **System** - Storage, power, date/time, language, updates
- **About** - System specifications, Ultron info, credits

**Features:**
- Modern Adw.NavigationSplitView layout
- Search functionality
- Responsive design for all screen sizes
- GSettings integration
- Real-time system information

### Ultron Control Center (`apps/ultron-control-center/`)

Quick settings panel for fast system controls.

**Features:**
- Quick toggles: Wi-Fi, Bluetooth, Airplane, Night Light, DND, Dark Mode
- Brightness and volume sliders
- Media playback controls
- Output device selection
- Quick access to Settings, Lock, Power

### Nautilus Extension (`packages/nautilus-extension/`)

File manager enhancements for Ultron OS.

**Features:**
- Custom context menu (Open Terminal, Copy Path, Open as Root, Compress, Upload to Cloud)
- Quick access toolbar buttons (Home, Documents, Downloads, Cloud)
- Cloud sync property page
- Administrator file operations

## Installation

### Settings Application
```bash
cd apps/ultron-settings
meson setup build --prefix=/usr
ninja -C build
sudo ninja -C build install
```

### Control Center
```bash
cd apps/ultron-control-center
meson setup build --prefix=/usr
ninja -C build
sudo ninja -C build install
```

### Nautilus Extension
```bash
cd packages/nautilus-extension
meson setup build --prefix=/usr
ninja -C build
sudo ninja -C build install
nautilus -q  # Restart Nautilus
```

## Technology Stack

- **GTK 4** - Modern UI toolkit
- **Libadwaita** - GNOME application library
- **Python 3** - Application logic
- **GSettings** - Configuration storage
- **Nautilus Python** - File manager extension API

## Configuration

All settings are stored via GSettings schemas:
- `org.ultron.settings` - Settings application preferences
- `org.gnome.desktop.interface` - System interface settings
- `org.gnome.desktop.background` - Desktop background settings

## Screenshots

The settings application features:
- Clean, modern interface with sidebar navigation
- Consistent design language across all pages
- Smooth animations and transitions
- Dark/light theme support

## License

GPL-3.0
