# Ultron Cloud

Cloud synchronization service for Ultron OS.

## Features

- Multi-provider support (Nextcloud, Google Drive, OneDrive)
- File synchronization
- Backup management
- Selective sync
- Conflict resolution

## Dependencies

- Python 3.12+
- rclone (for Google Drive, OneDrive)
- nextcloudcmd (for Nextcloud)

## Building

```bash
meson setup build
ninja -C build
```

## Running

```bash
python3 src/cloud_service.py
```

## License

GPL-3.0
