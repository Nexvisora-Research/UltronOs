# Ultron OS - Phase 6: Expansion

## Overview

Phase 6 focuses on cross-device support, mobile/tablet interfaces, voice assistant integration, smart workflows, gesture support, and device synchronization. This phase transforms Ultron OS into a truly adaptive, intelligent operating system.

## Components

### Cross-Device Support (`tools/ultron-device/`)

**File:** `src/device_manager.py`

Detects device type and adapts the interface accordingly.

**Features:**
- **Device Detection**
  - Auto-detects desktop, laptop, tablet, phone, TV
  - Identifies form factor (touch, traditional, hybrid)
  - Detects screen size category (xlarge, large, medium, small)
  - Checks for touch input, battery, sensors
- **Adaptive Configuration**
  - Automatic UI scaling based on screen size
  - Icon and font size adjustment
  - Layout selection (single-column, two-column, multi-panel, standard)
  - Touch optimization toggles

**Interface Scaler:**
- Applies GTK/Libadwaita scaling
- Configures monitor framebuffer scaling
- Applies device-specific layouts

**Usage:**
```bash
# Detect device
ultron-device detect

# Apply UI scaling
ultron-device scale

# Apply adaptive layout
ultron-device layout

# Show configuration
ultron-device config
```

### Mobile/Tablet Interface (`apps/ultron-mobile/`)

**File:** `src/adaptive_ui.py`

Adaptive UI components for touch devices.

**Features:**
- **AdaptiveWindow**
  - Automatically adjusts layout based on device type
  - Phone mode: single-column, bottom navigation, full-screen
  - Tablet mode: two-column, collapsible sidebar, touch-optimized
  - Desktop mode: standard multi-panel layout
- **Touch Optimization**
  - Larger button sizes (48px minimum)
  - Larger list rows (56px minimum)
  - Increased padding for touch targets
  - CSS-based touch optimization
- **MobileSettingsPage**
  - Settings optimized for touch navigation
  - Larger rows with clear icons
  - Touch-friendly controls

### Voice Assistant (`apps/ultron-voice/`)

**File:** `src/voice_assistant.py`

Voice command recognition and text-to-speech.

**Features:**
- **Voice Recognition**
  - Hotword detection ("Hey Ultron")
  - Continuous listening mode
  - Speech-to-text processing
  - Multi-language support
- **Built-in Commands**
  - Open applications (browser, terminal, settings)
  - System controls (screenshot, lock screen)
  - Volume controls (up, down, mute)
  - Time and date queries
- **Text-to-Speech**
  - espeak/festival integration
  - Multiple voice support
  - Configurable voice selection
- **Custom Commands**
  - VoiceCommandBuilder for creating custom commands
  - Pattern matching for command recognition
  - JSON-based command storage

**Usage:**
```bash
# Start voice assistant
ultron-voice start

# Stop voice assistant
ultron-voice stop

# Speak text
ultron-voice speak "Hello, world!"

# List custom commands
ultron-voice commands

# Test microphone
ultron-voice test
```

### Smart Workflow Engine (`services/ultron-workflow/`)

**File:** `src/workflow_engine.py`

Task automation and context-aware suggestions.

**Features:**
- **Workflow Management**
  - Create, edit, delete workflows
  - Enable/disable workflows
  - Trigger-based execution
  - Action chaining
- **Trigger Types**
  - Time-based (specific time, days of week)
  - App launch (when specific app opens)
  - Network-based (when connected to specific network)
  - Location-based (geofencing)
- **Action Types**
  - Launch application
  - Run shell command
  - Show notification
  - Wait/delay
  - Open URL
  - Type text (via xdotool)
- **Context-Aware Suggestions**
  - Time-based suggestions (morning, lunch, evening)
  - Usage-based suggestions (related apps)
  - Confidence scoring
  - Usage history tracking

**Usage:**
```bash
# List workflows
ultron-workflow list

# Execute workflow
ultron-workflow run 1

# Get suggestions
ultron-workflow suggestions
```

### Gesture Support (`tools/ultron-gesture/`)

**File:** `src/gesture_controller.py`

Touch gesture recognition and handling.

**Features:**
- **Supported Gestures**
  - Swipe (left, right, up, down)
  - Pinch (zoom in/out)
  - Rotate
  - Long press
  - Tap
  - Double tap
- **Gesture Controller**
  - Add gestures to any GTK widget
  - Enable/disable gesture recognition
  - Propagation phase control
- **Touch Settings**
  - Gesture enable/disable
  - Swipe sensitivity (low, medium, high)
  - Gesture action customization
  - Touch feedback options (haptic, sound, visual)
- **TouchOptimizedWindow**
  - Pre-configured touch window
  - Swipe navigation between pages
  - Pinch-to-zoom support

**Usage:**
```bash
# Check gesture status
ultron-gesture status

# Enable gestures
ultron-gesture enable

# Disable gestures
ultron-gesture disable

# Test gestures
ultron-gesture test
```

### Device Synchronization (`services/ultron-sync/`)

**File:** `src/device_sync.py`

Sync settings, files, and state across devices.

**Features:**
- **Sync Items**
  - GSettings (interface, background, shell)
  - GTK bookmarks
  - Wallpaper
  - Theme configuration
  - Keyboard shortcuts
  - Application configurations
- **Sync Management**
  - Unique device ID generation
  - Automatic sync interval
  - Manual sync trigger
  - Apply synced settings
- **Device Tracking**
  - Device name and ID
  - Last sync timestamp
  - Sync item configuration
  - Per-device settings

**Usage:**
```bash
# Check sync status
ultron-sync status

# Sync now
ultron-sync sync

# Apply synced settings
ultron-sync apply

# List devices
ultron-sync devices
```

## Systemd Services

- `ultron-workflow.service` - Workflow engine daemon
- `ultron-sync.service` - Device sync daemon

## Configuration Files

```
~/.config/ultron/
├── device/
│   └── device.json
├── voice/
│   ├── voice.json
│   └── custom_commands.json
├── workflows/
│   └── workflows.json
├── sync/
│   ├── sync.json
│   ├── settings/
│   ├── bookmarks/
│   ├── wallpaper/
│   ├── themes/
│   ├── keybindings/
│   └── app-config/
└── suggestions/
    └── history.json
```

## Installation

```bash
# Install all expansion tools
cd tools/ultron-device && meson setup build --prefix=/usr && sudo ninja -C build install
cd ../ultron-gesture && meson setup build --prefix=/usr && sudo ninja -C build install
cd ../../apps/ultron-voice && meson setup build --prefix=/usr && sudo ninja -C build install
cd ../../services/ultron-workflow && meson setup build --prefix=/usr && sudo ninja -C build install
cd ../../services/ultron-sync && meson setup build --prefix=/usr && sudo ninja -C build install

# Enable services
systemctl --user enable ultron-workflow
systemctl --user enable ultron-sync
systemctl --user start ultron-workflow
systemctl --user start ultron-sync
```

## Dependencies

- Python 3.8+
- GTK 4 / Libadwaita
- espeak or festival (TTS)
- xdotool (text typing)
- nmcli (network detection)
- dmidecode (device detection)

## License

GPL-3.0
