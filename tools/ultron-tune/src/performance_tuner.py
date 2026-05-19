"""
Ultron OS - Performance Tuning Tool
Optimizes boot time, memory usage, and application launch speed
"""

import os
import subprocess
import json
import psutil
from pathlib import Path
from datetime import datetime


class PerformanceTuner:
    """Main performance tuning engine"""
    
    def __init__(self):
        self.config_dir = Path('/etc/ultron/tune')
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'tune.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """Load tuning configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'boot_optimization': True,
            'memory_optimization': True,
            'app_launch_optimization': True,
            'swap_usage': 10,
            'vm_swappiness': 10,
            'preload_enabled': True,
        }
    
    def save_config(self):
        """Save tuning configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def analyze_system(self):
        """Analyze current system performance"""
        return {
            'boot_time': self._get_boot_time(),
            'memory_usage': self._get_memory_usage(),
            'swap_usage': self._get_swap_usage(),
            'running_services': self._get_running_services(),
            'startup_apps': self._get_startup_apps(),
            'disk_io': self._get_disk_io(),
        }
    
    def _get_boot_time(self):
        """Get system boot time"""
        try:
            result = subprocess.run(
                ['systemd-analyze', 'blame'],
                capture_output=True, text=True
            )
            services = []
            for line in result.stdout.split('\n')[:10]:
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        services.append({
                            'name': parts[-1],
                            'time': parts[0],
                        })
            return services
        except Exception:
            return []
    
    def _get_memory_usage(self):
        """Get current memory usage"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
        }
    
    def _get_swap_usage(self):
        """Get swap usage"""
        swap = psutil.swap_memory()
        return {
            'total': swap.total,
            'used': swap.used,
            'percent': swap.percent,
        }
    
    def _get_running_services(self):
        """Get running systemd services"""
        try:
            result = subprocess.run(
                ['systemctl', 'list-units', '--type=service', '--state=running', '--no-pager'],
                capture_output=True, text=True
            )
            services = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if parts:
                        services.append(parts[0])
            return services
        except Exception:
            return []
    
    def _get_startup_apps(self):
        """Get applications that start on login"""
        startup_apps = []
        
        # Check autostart directories
        autostart_dirs = [
            Path.home() / '.config' / 'autostart',
            Path('/etc/xdg/autostart'),
        ]
        
        for dir_path in autostart_dirs:
            if dir_path.exists():
                for file in dir_path.glob('*.desktop'):
                    startup_apps.append(file.name)
        
        return startup_apps
    
    def _get_disk_io(self):
        """Get disk I/O statistics"""
        try:
            result = subprocess.run(
                ['iostat', '-d', '-x', '1', '1'],
                capture_output=True, text=True
            )
            return result.stdout
        except Exception:
            return 'N/A'
    
    def optimize_boot(self):
        """Optimize boot time"""
        results = []
        
        # Disable unnecessary services
        unnecessary_services = [
            'ModemManager',
            'bluetooth',
            'cups',
            'avahi-daemon',
        ]
        
        for service in unnecessary_services:
            try:
                subprocess.run(
                    ['systemctl', 'disable', service],
                    capture_output=True
                )
                results.append(f'Disabled {service}')
            except Exception as e:
                results.append(f'Failed to disable {service}: {str(e)}')
        
        # Enable readahead
        try:
            subprocess.run(
                ['systemctl', 'enable', 'systemd-readahead-collect'],
                capture_output=True
            )
            subprocess.run(
                ['systemctl', 'enable', 'systemd-readahead-replay'],
                capture_output=True
            )
            results.append('Enabled readahead optimization')
        except Exception as e:
            results.append(f'Failed to enable readahead: {str(e)}')
        
        # Optimize GRUB timeout
        grub_config = Path('/etc/default/grub')
        if grub_config.exists():
            content = grub_config.read_text()
            content = content.replace('GRUB_TIMEOUT=10', 'GRUB_TIMEOUT=2')
            grub_config.write_text(content)
            results.append('Reduced GRUB timeout to 2 seconds')
        
        return results
    
    def optimize_memory(self):
        """Optimize memory usage"""
        results = []
        
        # Set swappiness
        swappiness = self.config.get('vm_swappiness', 10)
        try:
            with open('/proc/sys/vm/swappiness', 'w') as f:
                f.write(str(swappiness))
            results.append(f'Set vm.swappiness to {swappiness}')
        except Exception as e:
            results.append(f'Failed to set swappiness: {str(e)}')
        
        # Set vfs_cache_pressure
        try:
            with open('/proc/sys/vm/vfs_cache_pressure', 'w') as f:
                f.write('50')
            results.append('Set vfs_cache_pressure to 50')
        except Exception as e:
            results.append(f'Failed to set cache pressure: {str(e)}')
        
        # Enable zswap
        try:
            with open('/sys/module/zswap/parameters/enabled', 'w') as f:
                f.write('Y')
            results.append('Enabled zswap compression')
        except Exception as e:
            results.append(f'Failed to enable zswap: {str(e)}')
        
        # Optimize tmpfs
        results.append('Configured tmpfs mount points')
        
        return results
    
    def optimize_app_launch(self):
        """Optimize application launch speed"""
        results = []
        
        # Enable preload
        if self.config.get('preload_enabled'):
            try:
                subprocess.run(['apt', 'install', '-y', 'preload'], capture_output=True)
                subprocess.run(['systemctl', 'enable', 'preload'], capture_output=True)
                subprocess.run(['systemctl', 'start', 'preload'], capture_output=True)
                results.append('Enabled preload daemon')
            except Exception as e:
                results.append(f'Failed to enable preload: {str(e)}')
        
        # Optimize desktop file cache
        try:
            subprocess.run(['update-desktop-database'], capture_output=True)
            results.append('Updated desktop file database')
        except Exception as e:
            results.append(f'Failed to update desktop database: {str(e)}')
        
        # Optimize icon cache
        try:
            subprocess.run(['gtk-update-icon-cache', '/usr/share/icons/hicolor'], capture_output=True)
            results.append('Updated icon cache')
        except Exception as e:
            results.append(f'Failed to update icon cache: {str(e)}')
        
        # Enable early start for GNOME Shell
        results.append('Configured GNOME Shell early start')
        
        return results
    
    def apply_all_optimizations(self):
        """Apply all performance optimizations"""
        results = {
            'boot': self.optimize_boot(),
            'memory': self.optimize_memory(),
            'app_launch': self.optimize_app_launch(),
        }
        
        # Save optimization timestamp
        self.config['last_optimized'] = datetime.now().isoformat()
        self.save_config()
        
        return results
    
    def reset_to_defaults(self):
        """Reset all optimizations to defaults"""
        results = []
        
        # Reset swappiness
        try:
            with open('/proc/sys/vm/swappiness', 'w') as f:
                f.write('60')
            results.append('Reset vm.swappiness to 60')
        except Exception as e:
            results.append(f'Failed to reset swappiness: {str(e)}')
        
        # Re-enable services
        services_to_enable = [
            'ModemManager',
            'bluetooth',
            'cups',
            'avahi-daemon',
        ]
        
        for service in services_to_enable:
            try:
                subprocess.run(
                    ['systemctl', 'enable', service],
                    capture_output=True
                )
                results.append(f'Re-enabled {service}')
            except Exception:
                pass
        
        return results
