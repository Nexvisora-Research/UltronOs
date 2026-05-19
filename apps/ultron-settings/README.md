# Ultron Settings

System settings application for Ultron OS, built with GTK4 and Libadwaita.

## Features

- Appearance (themes, icons, cursors, fonts)
- Network configuration
- Bluetooth management
- Display settings
- Sound configuration
- Power management
- User accounts
- Privacy settings
- Default applications
- Keyboard shortcuts

## Dependencies

- GTK 4
- Libadwaita
- Python 3.12+
- gobject-introspection

## Building

```bash
meson setup build
ninja -C build
```

## Running

```bash
python3 src/ultron-settings.py
```

## License

GPL-3.0
