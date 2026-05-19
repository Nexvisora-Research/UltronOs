# Ultron Tune

Performance tuning utility for Ultron OS.

## Features

- System performance analysis
- CPU governor management
- Memory optimization
- I/O scheduler configuration
- Performance profiles (Balanced, Performance, Power Saver)
- Startup application management

## Dependencies

- Python 3.12+
- psutil

## Building

```bash
meson setup build
ninja -C build
```

## Running

```bash
python3 src/performance_tuner.py
```

## License

GPL-3.0
