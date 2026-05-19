"""
Ultron OS - Power & Battery Manager
Power profiles, process optimization, and battery efficiency
"""

import os
import subprocess
import json
import psutil
from pathlib import Path
from datetime import datetime


class PowerManager:
    """Main power management engine"""
    
    def __init__(self):
        self.config_dir = Path('/etc/ultron/power')
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'power.json'
        self.config = self._load_config()
        
        self.current_profile = self.config.get('current_profile', 'balanced')
    
    def _load_config(self):
        """Load power configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'current_profile': 'balanced',
            'profiles': {
                'performance': {
                    'cpu_governor': 'performance',
                    'min_screen_brightness': 50,
                    'sleep_timeout': 0,
                    'usb_autosuspend': False,
                    'wifi_power_save': False,
                },
                'balanced': {
                    'cpu_governor': 'schedutil',
                    'min_screen_brightness': 30,
                    'sleep_timeout': 300,
                    'usb_autosuspend': True,
                    'wifi_power_save': True,
                },
                'powersave': {
                    'cpu_governor': 'powersave',
                    'min_screen_brightness': 10,
                    'sleep_timeout': 120,
                    'usb_autosuspend': True,
                    'wifi_power_save': True,
                },
            },
        }
    
    def save_config(self):
        """Save power configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_battery_info(self):
        """Get battery information"""
        battery_info = {
            'present': False,
            'percentage': 0,
            'charging': False,
            'time_to_full': None,
            'time_to_empty': None,
            'health': 'Unknown',
        }
        
        # Check battery via psutil
        if hasattr(psutil, 'sensors_battery'):
            battery = psutil.sensors_battery()
            if battery:
                battery_info['present'] = True
                battery_info['percentage'] = battery.percent
                battery_info['charging'] = battery.power_plugged
                
                if battery.power_plugged:
                    battery_info['time_to_full'] = self._estimate_time_to_full()
                else:
                    battery_info['time_to_empty'] = self._estimate_time_to_empty()
        
        # Get battery health from sysfs
        battery_path = Path('/sys/class/power_supply/BAT0')
        if battery_path.exists():
            battery_info['present'] = True
            
            capacity_file = battery_path / 'capacity'
            if capacity_file.exists():
                battery_info['percentage'] = int(capacity_file.read_text().strip())
            
            status_file = battery_path / 'status'
            if status_file.exists():
                status = status_file.read_text().strip()
                battery_info['charging'] = status in ['Charging', 'Full']
            
            # Battery health
            capacity_now_file = battery_path / 'charge_now'
            capacity_full_file = battery_path / 'charge_full'
            if capacity_now_file.exists() and capacity_full_file.exists():
                now = int(capacity_now_file.read_text().strip())
                full = int(capacity_full_file.read_text().strip())
                if full > 0:
                    health = (now / full) * 100
                    battery_info['health'] = f'{health:.1f}%'
        
        return battery_info
    
    def _estimate_time_to_full(self):
        """Estimate time to full charge"""
        # This would use actual battery data
        return '2h 30m'
    
    def _estimate_time_to_empty(self):
        """Estimate time to empty"""
        battery_info = self.get_battery_info()
        percentage = battery_info['percentage']
        
        # Rough estimate: 1% = 3 minutes
        minutes = percentage * 3
        hours = minutes // 60
        mins = minutes % 60
        
        return f'{hours}h {mins}m'
    
    def set_profile(self, profile_name):
        """Switch power profile"""
        if profile_name not in self.config['profiles']:
            return {'success': False, 'message': f'Unknown profile: {profile_name}'}
        
        profile = self.config['profiles'][profile_name]
        self.current_profile = profile_name
        self.config['current_profile'] = profile_name
        self.save_config()
        
        results = []
        
        # Set CPU governor
        results.extend(self._set_cpu_governor(profile['cpu_governor']))
        
        # Set screen brightness
        results.extend(self._set_brightness(profile['min_screen_brightness']))
        
        # Set sleep timeout
        results.extend(self._set_sleep_timeout(profile['sleep_timeout']))
        
        # Configure USB autosuspend
        results.extend(self._set_usb_autosuspend(profile['usb_autosuspend']))
        
        # Configure WiFi power save
        results.extend(self._set_wifi_power_save(profile['wifi_power_save']))
        
        return {'success': True, 'profile': profile_name, 'changes': results}
    
    def _set_cpu_governor(self, governor):
        """Set CPU frequency governor"""
        results = []
        cpu_path = Path('/sys/devices/system/cpu')
        
        for cpu_dir in cpu_path.glob('cpu*/cpufreq/scaling_governor'):
            try:
                cpu_dir.write_text(governor)
                results.append(f'Set {cpu_dir.parent.parent.name} to {governor}')
            except Exception as e:
                results.append(f'Failed to set {cpu_dir}: {str(e)}')
        
        return results
    
    def _set_brightness(self, percentage):
        """Set screen brightness"""
        results = []
        
        # Find backlight device
        backlight_path = Path('/sys/class/backlight')
        
        for device in backlight_path.iterdir():
            brightness_file = device / 'brightness'
            max_brightness_file = device / 'max_brightness'
            
            if brightness_file.exists() and max_brightness_file.exists():
                max_brightness = int(max_brightness_file.read_text().strip())
                target = int(max_brightness * (percentage / 100))
                
                try:
                    brightness_file.write_text(str(target))
                    results.append(f'Set brightness to {percentage}%')
                except Exception as e:
                    results.append(f'Failed to set brightness: {str(e)}')
        
        return results
    
    def _set_sleep_timeout(self, seconds):
        """Set sleep timeout"""
        results = []
        
        if seconds == 0:
            # Disable sleep
            try:
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.settings-daemon.plugins.power',
                     'sleep-inactive-ac-type', 'nothing'],
                    capture_output=True
                )
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.settings-daemon.plugins.power',
                     'sleep-inactive-battery-type', 'nothing'],
                    capture_output=True
                )
                results.append('Disabled automatic sleep')
            except Exception as e:
                results.append(f'Failed to disable sleep: {str(e)}')
        else:
            minutes = seconds // 60
            try:
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.settings-daemon.plugins.power',
                     'sleep-inactive-ac-type', 'suspend'],
                    capture_output=True
                )
                subprocess.run(
                    ['gsettings', 'set', 'org.gnome.settings-daemon.plugins.power',
                     'sleep-inactive-ac-timeout', str(minutes)],
                    capture_output=True
                )
                results.append(f'Set sleep timeout to {minutes} minutes')
            except Exception as e:
                results.append(f'Failed to set sleep timeout: {str(e)}')
        
        return results
    
    def _set_usb_autosuspend(self, enabled):
        """Configure USB autosuspend"""
        results = []
        
        usb_path = Path('/sys/bus/usb/devices')
        
        for device in usb_path.iterdir():
            autosuspend_file = device / 'power/autosuspend'
            
            if autosuspend_file.exists():
                try:
                    if enabled:
                        autosuspend_file.write_text('2')
                    else:
                        autosuspend_file.write_text('-1')
                    results.append(f'Configured USB autosuspend for {device.name}')
                except Exception as e:
                    results.append(f'Failed to configure USB {device.name}: {str(e)}')
        
        return results
    
    def _set_wifi_power_save(self, enabled):
        """Configure WiFi power save"""
        results = []
        
        try:
            if enabled:
                subprocess.run(
                    ['iw', 'dev', 'wlan0', 'set', 'power_save', 'on'],
                    capture_output=True
                )
                results.append('Enabled WiFi power save')
            else:
                subprocess.run(
                    ['iw', 'dev', 'wlan0', 'set', 'power_save', 'off'],
                    capture_output=True
                )
                results.append('Disabled WiFi power save')
        except Exception as e:
            results.append(f'Failed to configure WiFi power save: {str(e)}')
        
        return results
    
    def optimize_processes(self):
        """Optimize running processes for power efficiency"""
        results = []
        
        # Find and renice non-essential processes
        non_essential = [
            'tracker-miner-fs',
            'baloo_file',
            'kactivitymanagerd',
        ]
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name']
                if name in non_essential:
                    proc.nice(10)  # Lower priority
                    results.append(f'Reduced priority for {name}')
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Enable CPU frequency scaling
        try:
            subprocess.run(
                ['cpupower', 'frequency-set', '-g', 'schedutil'],
                capture_output=True
            )
            results.append('Enabled CPU frequency scaling')
        except Exception:
            pass
        
        return results
    
    def get_power_report(self):
        """Generate comprehensive power report"""
        return {
            'battery': self.get_battery_info(),
            'current_profile': self.current_profile,
            'cpu_governor': self._get_current_governor(),
            'screen_brightness': self._get_current_brightness(),
            'running_processes': len(psutil.pids()),
            'power_hungry_apps': self._get_power_hungry_apps(),
        }
    
    def _get_current_governor(self):
        """Get current CPU governor"""
        governor_file = Path('/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor')
        if governor_file.exists():
            return governor_file.read_text().strip()
        return 'unknown'
    
    def _get_current_brightness(self):
        """Get current screen brightness"""
        backlight_path = Path('/sys/class/backlight')
        
        for device in backlight_path.iterdir():
            brightness_file = device / 'brightness'
            max_brightness_file = device / 'max_brightness'
            
            if brightness_file.exists() and max_brightness_file.exists():
                brightness = int(brightness_file.read_text().strip())
                max_brightness = int(max_brightness_file.read_text().strip())
                
                if max_brightness > 0:
                    return int((brightness / max_brightness) * 100)
        
        return 0
    
    def _get_power_hungry_apps(self):
        """Get applications using the most power"""
        apps = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                info = proc.info
                if info['cpu_percent'] and info['cpu_percent'] > 10:
                    apps.append({
                        'name': info['name'],
                        'pid': info['pid'],
                        'cpu': info['cpu_percent'],
                        'memory': info['memory_percent'],
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return sorted(apps, key=lambda x: x['cpu'], reverse=True)[:10]
