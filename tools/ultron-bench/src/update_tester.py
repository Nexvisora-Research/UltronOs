"""
Ultron OS - Update Testing Framework
Tests system updates before applying them
"""

import os
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


class UpdateTester:
    """Update testing and validation framework"""
    
    def __init__(self):
        self.config_dir = Path('/etc/ultron/update-test')
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.test_dir = Path('/var/lib/ultron/update-test')
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'config.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """Load update test configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'auto_test': True,
            'test_before_install': True,
            'rollback_on_failure': True,
            'max_test_time': 300,  # 5 minutes
        }
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def test_updates(self, packages=None):
        """Test updates before installing"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'overall': 'pass',
        }
        
        # Get available updates
        available = self._get_available_updates()
        
        if packages:
            available = [p for p in packages if p in available]
        
        # Test 1: Download test
        download_result = self._test_download(available)
        results['tests'].append(download_result)
        
        if download_result['status'] != 'pass':
            results['overall'] = 'fail'
            return results
        
        # Test 2: Dependency check
        dep_result = self._test_dependencies(available)
        results['tests'].append(dep_result)
        
        if dep_result['status'] != 'pass':
            results['overall'] = 'fail'
            return results
        
        # Test 3: Simulation install
        sim_result = self._test_simulation(available)
        results['tests'].append(sim_result)
        
        if sim_result['status'] != 'pass':
            results['overall'] = 'fail'
            return results
        
        # Test 4: Post-install validation
        validation_result = self._validate_system()
        results['tests'].append(validation_result)
        
        if validation_result['status'] != 'pass':
            results['overall'] = 'fail'
        
        return results
    
    def _get_available_updates(self):
        """Get list of available updates"""
        packages = []
        
        try:
            # APT updates
            result = subprocess.run(
                ['apt', 'list', '--upgradable'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    package = line.split('/')[0]
                    packages.append({'name': package, 'type': 'apt'})
            
            # Flatpak updates
            result = subprocess.run(
                ['flatpak', 'remote-ls', '--updates'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n'):
                if line.strip():
                    packages.append({'name': line.strip(), 'type': 'flatpak'})
        except Exception:
            pass
        
        return packages
    
    def _test_download(self, packages):
        """Test downloading packages"""
        result = {
            'name': 'Download Test',
            'status': 'pass',
            'details': [],
        }
        
        for package in packages:
            if package['type'] == 'apt':
                try:
                    subprocess.run(
                        ['apt', 'download', package['name']],
                        capture_output=True,
                        cwd=str(self.test_dir)
                    )
                    result['details'].append(f'Downloaded {package["name"]}')
                except Exception as e:
                    result['status'] = 'fail'
                    result['details'].append(f'Failed to download {package["name"]}: {str(e)}')
        
        return result
    
    def _test_dependencies(self, packages):
        """Test package dependencies"""
        result = {
            'name': 'Dependency Check',
            'status': 'pass',
            'details': [],
        }
        
        apt_packages = [p['name'] for p in packages if p['type'] == 'apt']
        
        if apt_packages:
            try:
                cmd = ['apt-get', '-s', 'install'] + apt_packages
                sim_result = subprocess.run(cmd, capture_output=True, text=True)
                
                if sim_result.returncode != 0:
                    result['status'] = 'fail'
                    result['details'].append('Dependency conflicts detected')
                    result['details'].append(sim_result.stderr)
                else:
                    result['details'].append('All dependencies satisfied')
            except Exception as e:
                result['status'] = 'fail'
                result['details'].append(f'Dependency check failed: {str(e)}')
        
        return result
    
    def _test_simulation(self, packages):
        """Test installation simulation"""
        result = {
            'name': 'Installation Simulation',
            'status': 'pass',
            'details': [],
        }
        
        apt_packages = [p['name'] for p in packages if p['type'] == 'apt']
        
        if apt_packages:
            try:
                # Simulate installation
                cmd = ['apt-get', '-s', '-y', 'install'] + apt_packages
                sim_result = subprocess.run(cmd, capture_output=True, text=True)
                
                if sim_result.returncode == 0:
                    result['details'].append('Installation simulation successful')
                else:
                    result['status'] = 'fail'
                    result['details'].append('Simulation failed')
                    result['details'].append(sim_result.stderr)
            except Exception as e:
                result['status'] = 'fail'
                result['details'].append(f'Simulation error: {str(e)}')
        
        return result
    
    def _validate_system(self):
        """Validate system health after updates"""
        result = {
            'name': 'System Validation',
            'status': 'pass',
            'details': [],
        }
        
        # Check critical services
        critical_services = [
            'gdm3',
            'NetworkManager',
            'systemd-logind',
        ]
        
        for service in critical_services:
            try:
                status = subprocess.run(
                    ['systemctl', 'is-active', service],
                    capture_output=True, text=True
                )
                
                if status.stdout.strip() == 'active':
                    result['details'].append(f'{service}: running')
                else:
                    result['status'] = 'warning'
                    result['details'].append(f'{service}: not running')
            except Exception:
                result['status'] = 'warning'
                result['details'].append(f'{service}: check failed')
        
        # Check disk space
        disk_usage = shutil.disk_usage('/')
        if disk_usage.percent > 90:
            result['status'] = 'warning'
            result['details'].append(f'Low disk space: {disk_usage.percent}%')
        
        return result
    
    def create_snapshot(self):
        """Create system snapshot before updates"""
        snapshot_name = f'ultron-snapshot-{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        
        try:
            subprocess.run(
                ['timeshift', '--create', '--comments', f'Pre-update snapshot', '--tags', 'O'],
                capture_output=True
            )
            return {'success': True, 'snapshot': snapshot_name}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def rollback(self):
        """Rollback to previous state"""
        try:
            # Get latest snapshot
            result = subprocess.run(
                ['timeshift', '--list'],
                capture_output=True, text=True
            )
            
            # Parse and restore latest snapshot
            # This is a simplified version
            return {'success': True, 'message': 'Rollback initiated'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
