"""
Ultron OS - System Monitor
Real-time system monitoring and stability tracking
"""

import os
import json
import psutil
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta


class SystemMonitor:
    """Main system monitoring engine"""
    
    def __init__(self):
        self.data_dir = Path('/var/log/ultron/monitor')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.data_dir / 'history.json'
        self.history = self._load_history()
        
        self._monitoring = False
        self._monitor_thread = None
        self._interval = 5  # seconds
    
    def _load_history(self):
        """Load monitoring history"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {'cpu': [], 'memory': [], 'disk': [], 'network': [], 'temperature': []}
    
    def save_history(self):
        """Save monitoring history"""
        # Keep only last 24 hours
        cutoff = datetime.now() - timedelta(hours=24)
        
        for key in self.history:
            self.history[key] = [
                entry for entry in self.history[key]
                if datetime.fromisoformat(entry['timestamp']) > cutoff
            ]
        
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_system_status(self):
        """Get current system status"""
        return {
            'cpu': self._get_cpu_info(),
            'memory': self._get_memory_info(),
            'disk': self._get_disk_info(),
            'network': self._get_network_info(),
            'processes': self._get_process_info(),
            'temperature': self._get_temperature_info(),
            'uptime': self._get_uptime(),
        }
    
    def _get_cpu_info(self):
        """Get CPU information"""
        return {
            'usage_percent': psutil.cpu_percent(interval=1),
            'per_cpu': psutil.cpu_percent(interval=1, percpu=True),
            'frequency': self._get_cpu_frequency(),
            'load_avg': os.getloadavg(),
            'cores': psutil.cpu_count(logical=True),
        }
    
    def _get_cpu_frequency(self):
        """Get CPU frequency"""
        freq = psutil.cpu_freq()
        if freq:
            return {
                'current': freq.current,
                'min': freq.min,
                'max': freq.max,
            }
        return {'current': 0, 'min': 0, 'max': 0}
    
    def _get_memory_info(self):
        """Get memory information"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total,
            'available': mem.available,
            'used': mem.used,
            'percent': mem.percent,
        }
    
    def _get_disk_info(self):
        """Get disk information"""
        disks = []
        
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'fstype': partition.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent,
                })
            except PermissionError:
                pass
        
        # Disk I/O
        try:
            io_counters = psutil.disk_io_counters()
            if io_counters:
                disks.append({
                    'io': {
                        'read_bytes': io_counters.read_bytes,
                        'write_bytes': io_counters.write_bytes,
                        'read_count': io_counters.read_count,
                        'write_count': io_counters.write_count,
                    }
                })
        except Exception:
            pass
        
        return disks
    
    def _get_network_info(self):
        """Get network information"""
        net_io = psutil.net_io_counters()
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv,
            'connections': len(psutil.net_connections()),
        }
    
    def _get_process_info(self):
        """Get process information"""
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
            try:
                info = proc.info
                processes.append({
                    'pid': info['pid'],
                    'name': info['name'],
                    'cpu': info['cpu_percent'] or 0,
                    'memory': info['memory_percent'] or 0,
                    'status': info['status'],
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return sorted(processes, key=lambda x: x['cpu'], reverse=True)[:20]
    
    def _get_temperature_info(self):
        """Get temperature information"""
        temps = {}
        
        try:
            sensors = psutil.sensors_temperatures()
            if sensors:
                for name, entries in sensors.items():
                    temps[name] = [
                        {
                            'label': entry.label,
                            'current': entry.current,
                            'high': entry.high,
                            'critical': entry.critical,
                        }
                        for entry in entries
                    ]
        except Exception:
            pass
        
        return temps
    
    def _get_uptime(self):
        """Get system uptime"""
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return {
            'boot_time': boot_time.isoformat(),
            'uptime': f'{days}d {hours}h {minutes}m {seconds}s',
        }
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop)
        self._monitor_thread.daemon = True
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop continuous monitoring"""
        self._monitoring = False
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self._monitoring:
            status = self.get_system_status()
            
            timestamp = datetime.now().isoformat()
            
            self.history['cpu'].append({
                'timestamp': timestamp,
                'usage': status['cpu']['usage_percent'],
            })
            
            self.history['memory'].append({
                'timestamp': timestamp,
                'usage': status['memory']['percent'],
            })
            
            self.history['disk'].append({
                'timestamp': timestamp,
                'usage': status['disk'][0]['percent'] if status['disk'] else 0,
            })
            
            self.save_history()
            
            time.sleep(self._interval)
    
    def get_health_report(self):
        """Generate system health report"""
        status = self.get_system_status()
        
        issues = []
        warnings = []
        
        # Check CPU usage
        if status['cpu']['usage_percent'] > 90:
            issues.append('CPU usage critically high')
        elif status['cpu']['usage_percent'] > 70:
            warnings.append('CPU usage high')
        
        # Check memory usage
        if status['memory']['percent'] > 95:
            issues.append('Memory usage critically high')
        elif status['memory']['percent'] > 80:
            warnings.append('Memory usage high')
        
        # Check disk usage
        for disk in status['disk']:
            if 'percent' in disk:
                if disk['percent'] > 95:
                    issues.append(f'Disk {disk["mountpoint"]} almost full')
                elif disk['percent'] > 80:
                    warnings.append(f'Disk {disk["mountpoint"]} getting full')
        
        # Check temperature
        for sensor_name, entries in status['temperature'].items():
            for entry in entries:
                if entry['current'] > entry.get('critical', 100):
                    issues.append(f'Critical temperature: {entry["label"]}')
                elif entry['current'] > entry.get('high', 80):
                    warnings.append(f'High temperature: {entry["label"]}')
        
        # Overall health
        if issues:
            health = 'critical'
        elif warnings:
            health = 'warning'
        else:
            health = 'healthy'
        
        return {
            'health': health,
            'issues': issues,
            'warnings': warnings,
            'timestamp': datetime.now().isoformat(),
            'status': status,
        }
    
    def clear_history(self):
        """Clear monitoring history"""
        self.history = {'cpu': [], 'memory': [], 'disk': [], 'network': [], 'temperature': []}
        self.save_history()
