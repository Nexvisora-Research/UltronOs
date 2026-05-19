# Ultron OS - Desktop Shell

Custom GNOME Shell extension providing a polished desktop experience for Ultron OS.

## Components

### Taskbar
- Custom dock/taskbar with app pinning
- Running application indicators
- System tray integration
- Workspace indicators
- Auto-hide support
- Configurable position (bottom, top, left)

### Launcher
- Application search with instant results
- Category browsing
- Recent applications
- Keyboard shortcuts (Super key)
- Fuzzy search support

### Notification Center
- Quick toggles (Wi-Fi, Bluetooth, Dark Mode, Night Light, DND, Airplane)
- Notification history
- Do Not Disturb mode
- Clear all notifications
- Time-stamped notifications

### System Info
- Real-time CPU usage monitoring
- Memory usage display
- Network speed indicator
- Quick access to settings

### Window Manager
- Workspace wrap-around toggle
- Custom animation speeds
- Window focus animations
- Grid arrangement utility
- Show desktop functionality

## Installation

```bash
# Install the extension
./install.sh

# Or manually:
mkdir -p ~/.local/share/gnome-shell/extensions/ultron-shell@ultron.org
cp -r ultron-shell-extension/* ~/.local/share/gnome-shell/extensions/ultron-shell@ultron.org/
glib-compile-schemas ~/.local/share/gnome-shell/extensions/ultron-shell@ultron.org/schemas
gnome-extensions enable ultron-shell@ultron.org
```

## Configuration

Open extension preferences:
```bash
gnome-extensions prefs ultron-shell@ultron.org
```

Or via GNOME Extensions app.

## Keyboard Shortcuts

- `Super` - Open launcher
- `Super + A` - Show all windows
- `Super + D` - Show desktop
- `Ctrl + Alt + Up/Down` - Switch workspaces

## Development

### Project Structure
```
ultron-shell-extension/
├── extension.js          # Main extension entry point
├── prefs.js              # Preferences UI
├── stylesheet.css        # Extension styles
├── metadata.json         # Extension metadata
├── meson.build           # Build configuration
├── schemas/              # GSettings schemas
└── components/           # Shell components
    ├── taskbar.js        # Taskbar implementation
    ├── launcher.js       # Application launcher
    ├── notification-center.js  # Notification center
    ├── system-info.js    # System monitoring
    └── window-manager.js # Window management
```

### Testing
1. Make changes to extension files
2. Restart GNOME Shell: `Alt+F2`, type `r`, press Enter (X11 only)
3. For Wayland, log out and log back in

### Debugging
View logs:
```bash
journalctl /usr/bin/gnome-shell -f
```

## Requirements

- GNOME Shell 45, 46, or 47
- GTK 4
- Libadwaita

## License

GPL-3.0
