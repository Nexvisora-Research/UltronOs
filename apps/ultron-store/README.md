# Ultron Store

Application store for Ultron OS, supporting Flatpak and native packages.

## Features

- Browse and search applications
- Flatpak integration
- Application categories
- Ratings and reviews
- Automatic updates
- Application details page

## Dependencies

- GTK 4
- Libadwaita
- Python 3.12+
- Flatpak

## Building

```bash
meson setup build
ninja -C build
```

## Running

```bash
python3 src/ultron-store.py
```

## License

GPL-3.0
