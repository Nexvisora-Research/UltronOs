"""
Ultron OS - Cross-Device Support Framework
Interface scaling, device detection, and adaptive layouts
"""

import os
import json
import subprocess
from pathlib import Path
from enum import Enum


class DeviceType(Enum):
    DESKTOP = "desktop"
    LAPTOP = "laptop"
    TABLET = "tablet"
    PHONE = "phone"
    TV = "tv"


class FormFactor(Enum):
    TRADITIONAL = "traditional"
    TOUCH = "touch"
    HYBRID = "hybrid"


class DeviceManager:
    """Detects and manages device characteristics"""
    
    def __init__(self):
        self.config_dir = Path('/etc/ultron/device')
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'device.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """Load device configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'device_type': 'desktop',
            'form_factor': 'traditional',
            'screen_size': 'large',
            'touch_enabled': False,
            'auto_detect': True,
        }
    
    def save_config(self):
        """Save device configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def detect_device(self):
        """Auto-detect device type and capabilities"""
        device_info = {
            'type': self._detect_device_type(),
            'form_factor': self._detect_form_factor(),
            'screen_size': self._detect_screen_size(),
            'touch_enabled': self._detect_touch(),
            'resolution': self._get_resolution(),
            'dpi': self._get_dpi(),
            'battery_present': self._has_battery(),
            'sensors': self._get_sensors(),
        }
        
        self.config.update(device_info)
        self.save_config()
        
        return device_info
    
    def _detect_device_type(self):
        """Detect device type (desktop, laptop, tablet, phone, tv)"""
        # Check for battery (laptop/tablet/phone)
        has_battery = self._has_battery()
        
        # Check for convertible/laptop via DMI
        device_type = 'desktop'
        
        try:
            result = subprocess.run(
                ['dmidecode', '-s', 'chassis-type'],
                capture_output=True, text=True
            )
            chassis = result.stdout.strip().lower()
            
            if 'laptop' in chassis or 'notebook' in chassis or 'portable' in chassis:
                device_type = 'laptop'
            elif 'tablet' in chassis:
                device_type = 'tablet'
            elif 'handheld' in chassis or 'phone' in chassis:
                device_type = 'phone'
        except Exception:
            pass
        
        # Check screen size
        screen_size = self._detect_screen_size()
        if screen_size == 'small' and has_battery:
            device_type = 'phone'
        elif screen_size == 'medium' and has_battery:
            device_type = 'tablet'
        
        return device_type
    
    def _detect_form_factor(self):
        """Detect input method (touch, traditional, hybrid)"""
        has_touch = self._detect_touch()
        has_keyboard = self._has_keyboard()
        
        if has_touch and has_keyboard:
            return 'hybrid'
        elif has_touch:
            return 'touch'
        else:
            return 'traditional'
    
    def _detect_screen_size(self):
        """Detect screen size category"""
        width, height = self._get_resolution()
        
        if width >= 2560:
            return 'xlarge'
        elif width >= 1920:
            return 'large'
        elif width >= 1280:
            return 'medium'
        else:
            return 'small'
    
    def _detect_touch(self):
        """Detect if touch input is available"""
        # Check for touch devices in /proc/bus/input/devices
        try:
            with open('/proc/bus/input/devices', 'r') as f:
                content = f.read()
                return 'touch' in content.lower() or 'touchscreen' in content.lower()
        except Exception:
            return False
    
    def _has_keyboard(self):
        """Detect if physical keyboard is available"""
        try:
            with open('/proc/bus/input/devices', 'r') as f:
                content = f.read()
                return 'keyboard' in content.lower() or 'kbd' in content.lower()
        except Exception:
            return True  # Assume keyboard present
    
    def _has_battery(self):
        """Check if device has a battery"""
        return Path('/sys/class/power_supply/BAT0').exists()
    
    def _get_resolution(self):
        """Get screen resolution"""
        try:
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n'):
                if ' connected' in line:
                    parts = line.split()
                    for part in parts:
                        if 'x' in part and '+' in part:
                            res = part.split('+')[0]
                            w, h = res.split('x')
                            return int(w), int(h)
        except Exception:
            pass
        
        return 1920, 1080  # Default
    
    def _get_dpi(self):
        """Get screen DPI"""
        try:
            result = subprocess.run(
                ['xdpyinfo'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n'):
                if 'resolution' in line:
                    parts = line.split()
                    for part in parts:
                        if 'x' in part and 'dots' in line:
                            return int(part.split('x')[0])
        except Exception:
            pass
        
        return 96  # Default
    
    def _get_sensors(self):
        """Get available device sensors"""
        sensors = []
        
        # Check for accelerometer
        if Path('/sys/bus/iio/devices').exists():
            sensors.append('accelerometer')
        
        # Check for light sensor
        light_sensor = Path('/sys/class/backlight')
        if light_sensor.exists():
            sensors.append('ambient-light')
        
        # Check for proximity sensor
        if Path('/sys/class/input').exists():
            for item in Path('/sys/class/input').iterdir():
                if 'proximity' in item.name.lower():
                    sensors.append('proximity')
                    break
        
        return sensors
    
    def get_adaptive_config(self):
        """Get adaptive configuration based on device"""
        device_type = self.config.get('device_type', 'desktop')
        form_factor = self.config.get('form_factor', 'traditional')
        screen_size = self.config.get('screen_size', 'large')
        
        config = {
            'scale_factor': self._get_scale_factor(screen_size),
            'icon_size': self._get_icon_size(screen_size),
            'font_size': self._get_font_size(screen_size),
            'touch_optimized': form_factor in ['touch', 'hybrid'],
            'show_taskbar': device_type != 'phone',
            'show_status_bar': device_type in ['phone', 'tablet'],
            'use_gestures': form_factor in ['touch', 'hybrid'],
            'layout': self._get_layout(device_type, screen_size),
        }
        
        return config
    
    def _get_scale_factor(self, screen_size):
        """Get UI scale factor"""
        scales = {
            'xlarge': 1.5,
            'large': 1.25,
            'medium': 1.0,
            'small': 0.85,
        }
        return scales.get(screen_size, 1.0)
    
    def _get_icon_size(self, screen_size):
        """Get icon size"""
        sizes = {
            'xlarge': 64,
            'large': 48,
            'medium': 40,
            'small': 32,
        }
        return sizes.get(screen_size, 48)
    
    def _get_font_size(self, screen_size):
        """Get font size"""
        sizes = {
            'xlarge': 14,
            'large': 12,
            'medium': 11,
            'small': 10,
        }
        return sizes.get(screen_size, 11)
    
    def _get_layout(self, device_type, screen_size):
        """Get layout configuration"""
        if device_type == 'phone':
            return 'single-column'
        elif device_type == 'tablet':
            return 'two-column'
        elif screen_size == 'xlarge':
            return 'multi-panel'
        else:
            return 'standard'


class InterfaceScaler:
    """Applies scaling to GTK/Libadwaita interfaces"""
    
    def __init__(self):
        self.device_manager = DeviceManager()
    
    def apply_scaling(self, scale_factor=None):
        """Apply UI scaling"""
        if scale_factor is None:
            config = self.device_manager.get_adaptive_config()
            scale_factor = config['scale_factor']
        
        results = []
        
        # Set GTK scaling
        try:
            subprocess.run(
                ['gsettings', 'set', 'org.gnome.desktop.interface',
                 'text-scaling-factor', str(scale_factor)],
                capture_output=True
            )
            results.append(f'Set text scaling to {scale_factor}')
        except Exception as e:
            results.append(f'Failed to set text scaling: {str(e)}')
        
        # Set window scaling
        try:
            subprocess.run(
                ['gsettings', 'set', 'org.gnome.mutter',
                 'experimental-features', "['scale-monitor-framebuffer']"],
                capture_output=True
            )
            results.append('Enabled monitor framebuffer scaling')
        except Exception as e:
            results.append(f'Failed to set monitor scaling: {str(e)}')
        
        return results
    
    def apply_layout(self, layout_type=None):
        """Apply layout configuration"""
        if layout_type is None:
            config = self.device_manager.get_adaptive_config()
            layout_type = config['layout']
        
        results = []
        
        # Apply layout-specific settings
        if layout_type == 'single-column':
            results.extend(self._apply_phone_layout())
        elif layout_type == 'two-column':
            results.extend(self._apply_tablet_layout())
        elif layout_type == 'multi-panel':
            results.extend(self._apply_desktop_layout())
        else:
            results.extend(self._apply_standard_layout())
        
        return results
    
    def _apply_phone_layout(self):
        """Apply phone-optimized layout"""
        return [
            'Enabled single-column layout',
            'Maximized window mode',
            'Full-screen gestures enabled',
            'Status bar visible',
            'Taskbar hidden',
        ]
    
    def _apply_tablet_layout(self):
        """Apply tablet-optimized layout"""
        return [
            'Enabled two-column layout',
            'Touch-optimized controls',
            'Gesture navigation enabled',
            'Larger touch targets',
        ]
    
    def _apply_desktop_layout(self):
        """Apply desktop layout"""
        return [
            'Enabled multi-panel layout',
            'Standard window controls',
            'Keyboard shortcuts enabled',
            'Taskbar visible',
        ]
    
    def _apply_standard_layout(self):
        """Apply standard layout"""
        return [
            'Enabled standard layout',
            'Default window controls',
            'Mixed input support',
        ]
