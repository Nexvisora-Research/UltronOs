"""
Ultron OS - System Benchmark
Performance benchmarking and reporting
"""

import os
import time
import json
import subprocess
import psutil
from pathlib import Path
from datetime import datetime


class SystemBenchmark:
    """System benchmarking engine"""
    
    def __init__(self):
        self.results_dir = Path('/var/log/ultron/benchmarks')
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        self.results_file = self.results_dir / 'results.json'
        self.results = self._load_results()
    
    def _load_results(self):
        """Load previous benchmark results"""
        if self.results_file.exists():
            with open(self.results_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_results(self):
        """Save benchmark results"""
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def run_all_benchmarks(self):
        """Run all benchmarks"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'system': self._get_system_info(),
            'cpu': self._benchmark_cpu(),
            'memory': self._benchmark_memory(),
            'disk': self._benchmark_disk(),
            'boot': self._benchmark_boot(),
            'app_launch': self._benchmark_app_launch(),
        }
        
        self.results.append(results)
        self.save_results()
        
        return results
    
    def _get_system_info(self):
        """Get system information"""
        info = {
            'os': self._get_os_info(),
            'cpu': self._get_cpu_info(),
            'memory': self._get_memory_info(),
            'gpu': self._get_gpu_info(),
        }
        
        return info
    
    def _get_os_info(self):
        """Get OS information"""
        os_info = {}
        
        os_release = Path('/etc/os-release')
        if os_release.exists():
            for line in os_release.read_text().split('\n'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    os_info[key] = value.strip('"')
        
        return os_info
    
    def _get_cpu_info(self):
        """Get CPU information"""
        cpu_info = {
            'model': '',
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True),
        }
        
        cpuinfo = Path('/proc/cpuinfo')
        if cpuinfo.exists():
            for line in cpuinfo.read_text().split('\n'):
                if 'model name' in line:
                    cpu_info['model'] = line.split(':')[1].strip()
                    break
        
        return cpu_info
    
    def _get_memory_info(self):
        """Get memory information"""
        mem = psutil.virtual_memory()
        return {
            'total_gb': round(mem.total / (1024**3), 1),
        }
    
    def _get_gpu_info(self):
        """Get GPU information"""
        gpu_info = []
        
        try:
            result = subprocess.run(
                ['lspci', '-v'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n'):
                if 'VGA' in line or '3D' in line:
                    gpu_info.append(line.split(': ')[-1])
        except Exception:
            pass
        
        return gpu_info
    
    def _benchmark_cpu(self):
        """Benchmark CPU performance"""
        results = {}
        
        # Single-thread performance
        start = time.time()
        for _ in range(1000000):
            pass
        results['single_thread_loop'] = time.time() - start
        
        # Math operations
        start = time.time()
        result = 0
        for i in range(10000000):
            result += i * 0.001
        results['math_operations'] = time.time() - start
        
        # Multi-thread performance
        import concurrent.futures
        
        def cpu_intensive():
            result = 0
            for i in range(1000000):
                result += i ** 0.5
            return result
        
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(cpu_intensive) for _ in range(4)]
            concurrent.futures.wait(futures)
        results['multi_thread'] = time.time() - start
        
        return results
    
    def _benchmark_memory(self):
        """Benchmark memory performance"""
        results = {}
        
        # Memory allocation speed
        start = time.time()
        data = [0] * 10000000
        results['allocation'] = time.time() - start
        
        # Memory read/write speed
        start = time.time()
        for i in range(len(data)):
            data[i] = i
        for i in range(len(data)):
            _ = data[i]
        results['read_write'] = time.time() - start
        
        # Memory cleanup
        del data
        results['cleanup'] = time.time() - start
        
        return results
    
    def _benchmark_disk(self):
        """Benchmark disk performance"""
        results = {}
        
        test_file = Path('/tmp/ultron_bench_test')
        file_size = 100 * 1024 * 1024  # 100 MB
        
        # Write speed
        start = time.time()
        with open(test_file, 'wb') as f:
            f.write(b'0' * file_size)
        results['write_speed'] = time.time() - start
        results['write_speed_mbps'] = round(file_size / (1024 * 1024) / results['write_speed'], 2)
        
        # Read speed
        start = time.time()
        with open(test_file, 'rb') as f:
            _ = f.read()
        results['read_speed'] = time.time() - start
        results['read_speed_mbps'] = round(file_size / (1024 * 1024) / results['read_speed'], 2)
        
        # Cleanup
        test_file.unlink()
        
        return results
    
    def _benchmark_boot(self):
        """Benchmark boot time"""
        results = {}
        
        try:
            # Get total boot time
            result = subprocess.run(
                ['systemd-analyze'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n'):
                if 'Startup finished in' in line:
                    results['total'] = line
                    break
            
            # Get service breakdown
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
                            'service': parts[-1],
                            'time': parts[0],
                        })
            
            results['services'] = services
        except Exception as e:
            results['error'] = str(e)
        
        return results
    
    def _benchmark_app_launch(self):
        """Benchmark application launch times"""
        results = {}
        
        apps = [
            ('firefox', 'Firefox'),
            ('nautilus', 'File Manager'),
            ('gnome-terminal', 'Terminal'),
            ('gedit', 'Text Editor'),
        ]
        
        for cmd, name in apps:
            times = []
            
            for _ in range(3):
                start = time.time()
                
                try:
                    proc = subprocess.Popen(
                        [cmd],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    
                    # Wait for process to start
                    time.sleep(2)
                    proc.terminate()
                    proc.wait()
                    
                    times.append(time.time() - start)
                except Exception:
                    pass
                
                time.sleep(1)
            
            if times:
                results[name] = {
                    'avg': round(sum(times) / len(times), 3),
                    'min': round(min(times), 3),
                    'max': round(max(times), 3),
                }
        
        return results
    
    def get_comparison(self):
        """Compare current results with previous runs"""
        if len(self.results) < 2:
            return {'message': 'Need at least 2 benchmark runs to compare'}
        
        latest = self.results[-1]
        previous = self.results[-2]
        
        comparison = {}
        
        # Compare CPU
        if 'cpu' in latest and 'cpu' in previous:
            comparison['cpu'] = {
                'single_thread': self._compare_values(
                    latest['cpu'].get('single_thread_loop', 0),
                    previous['cpu'].get('single_thread_loop', 0),
                    lower_is_better=True
                ),
                'multi_thread': self._compare_values(
                    latest['cpu'].get('multi_thread', 0),
                    previous['cpu'].get('multi_thread', 0),
                    lower_is_better=True
                ),
            }
        
        # Compare disk
        if 'disk' in latest and 'disk' in previous:
            comparison['disk'] = {
                'write_speed': self._compare_values(
                    latest['disk'].get('write_speed_mbps', 0),
                    previous['disk'].get('write_speed_mbps', 0),
                    lower_is_better=False
                ),
                'read_speed': self._compare_values(
                    latest['disk'].get('read_speed_mbps', 0),
                    previous['disk'].get('read_speed_mbps', 0),
                    lower_is_better=False
                ),
            }
        
        return comparison
    
    def _compare_values(self, current, previous, lower_is_better=True):
        """Compare two benchmark values"""
        if previous == 0:
            return {'current': current, 'previous': previous, 'change': 'N/A'}
        
        change = ((current - previous) / previous) * 100
        
        if lower_is_better:
            change = -change
        
        return {
            'current': current,
            'previous': previous,
            'change_percent': round(change, 2),
            'improved': change > 0,
        }
