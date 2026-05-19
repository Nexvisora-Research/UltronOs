"""
Ultron OS - Cloud Integration Service
Handles cloud sync, backup, and account integration
"""

import os
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime


class CloudService:
    """Main cloud integration service"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'ultron' / 'cloud'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.sync_dir = Path.home() / 'Ultron Cloud'
        self.sync_dir.mkdir(exist_ok=True)
        
        self.config_file = self.config_dir / 'config.json'
        self.config = self._load_config()
        
        self._sync_thread = None
        self._syncing = False
    
    def _load_config(self):
        """Load cloud configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'providers': {},
            'sync_folders': [],
            'auto_sync': True,
            'sync_interval': 300,  # 5 minutes
        }
    
    def save_config(self):
        """Save cloud configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_provider(self, provider_type, credentials):
        """Add a cloud provider"""
        self.config['providers'][provider_type] = {
            'type': provider_type,
            'credentials': credentials,
            'enabled': True,
            'added_at': datetime.now().isoformat(),
        }
        self.save_config()
    
    def remove_provider(self, provider_type):
        """Remove a cloud provider"""
        if provider_type in self.config['providers']:
            del self.config['providers'][provider_type]
            self.save_config()
    
    def get_providers(self):
        """Get list of configured providers"""
        return self.config['providers']
    
    def add_sync_folder(self, folder_path):
        """Add a folder to sync"""
        folder = str(Path(folder_path).expanduser())
        if folder not in self.config['sync_folders']:
            self.config['sync_folders'].append(folder)
            self.save_config()
    
    def remove_sync_folder(self, folder_path):
        """Remove a folder from sync"""
        folder = str(Path(folder_path).expanduser())
        if folder in self.config['sync_folders']:
            self.config['sync_folders'].remove(folder)
            self.save_config()
    
    def get_sync_folders(self):
        """Get list of synced folders"""
        return self.config['sync_folders']
    
    def sync(self, provider_type=None):
        """Start sync process"""
        if self._syncing:
            return
        
        self._syncing = True
        self._sync_thread = threading.Thread(target=self._do_sync, args=(provider_type,))
        self._sync_thread.start()
    
    def _do_sync(self, provider_type=None):
        """Perform actual sync"""
        providers = self.config['providers']
        
        if provider_type:
            providers = {provider_type: providers.get(provider_type)}
        
        for ptype, provider in providers.items():
            if not provider.get('enabled'):
                continue
            
            if ptype == 'nextcloud':
                self._sync_nextcloud(provider)
            elif ptype == 'google_drive':
                self._sync_google_drive(provider)
            elif ptype == 'onedrive':
                self._sync_onedrive(provider)
        
        self._syncing = False
    
    def _sync_nextcloud(self, provider):
        """Sync with Nextcloud"""
        credentials = provider['credentials']
        server = credentials.get('server', '')
        username = credentials.get('username', '')
        password = credentials.get('password', '')
        
        # Use rclone or nextcloudcmd
        cmd = ['nextcloudcmd', '--non-interactive', str(self.sync_dir), server]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f'Nextcloud sync failed: {e.stderr.decode()}')
    
    def _sync_google_drive(self, provider):
        """Sync with Google Drive"""
        # Use rclone
        cmd = ['rclone', 'sync', str(self.sync_dir), 'gdrive:Ultron']
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f'Google Drive sync failed: {e.stderr.decode()}')
    
    def _sync_onedrive(self, provider):
        """Sync with OneDrive"""
        # Use onedrive client
        cmd = ['onedrive', '--synchronize']
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f'OneDrive sync failed: {e.stderr.decode()}')
    
    def start_auto_sync(self):
        """Start automatic sync timer"""
        if not self.config.get('auto_sync'):
            return
        
        interval = self.config.get('sync_interval', 300)
        
        def sync_loop():
            while True:
                self.sync()
                import time
                time.sleep(interval)
        
        thread = threading.Thread(target=sync_loop, daemon=True)
        thread.start()
    
    def get_sync_status(self):
        """Get current sync status"""
        return {
            'syncing': self._syncing,
            'providers': len(self.config['providers']),
            'sync_folders': len(self.config['sync_folders']),
            'auto_sync': self.config.get('auto_sync', False),
        }


class BackupService:
    """System backup service"""
    
    def __init__(self):
        self.backup_dir = Path.home() / '.local' / 'share' / 'ultron' / 'backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self, backup_type='full'):
        """Create a system backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'ultron_backup_{backup_type}_{timestamp}'
        backup_path = self.backup_dir / backup_name
        
        if backup_type == 'full':
            return self._full_backup(backup_path)
        elif backup_type == 'config':
            return self._config_backup(backup_path)
        elif backup_type == 'documents':
            return self._documents_backup(backup_path)
    
    def _full_backup(self, backup_path):
        """Full system backup using Timeshift"""
        cmd = ['timeshift', '--create', '--comments', 'Ultron Backup', '--tags', 'O']
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return {'success': True, 'path': str(backup_path)}
        except subprocess.CalledProcessError as e:
            return {'success': False, 'error': e.stderr.decode()}
    
    def _config_backup(self, backup_path):
        """Backup configuration files"""
        import shutil
        
        config_dirs = [
            Path.home() / '.config',
            Path.home() / '.local' / 'share',
        ]
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        for dir_path in config_dirs:
            if dir_path.exists():
                dest = backup_path / dir_path.name
                shutil.copytree(dir_path, dest, dirs_exist_ok=True)
        
        return {'success': True, 'path': str(backup_path)}
    
    def _documents_backup(self, backup_path):
        """Backup documents folder"""
        import shutil
        
        docs_dir = Path.home() / 'Documents'
        if docs_dir.exists():
            backup_path.mkdir(parents=True, exist_ok=True)
            shutil.copytree(docs_dir, backup_path / 'Documents', dirs_exist_ok=True)
            return {'success': True, 'path': str(backup_path)}
        
        return {'success': False, 'error': 'Documents folder not found'}
    
    def list_backups(self):
        """List available backups"""
        backups = []
        
        for item in self.backup_dir.iterdir():
            if item.is_dir():
                stat = item.stat()
                backups.append({
                    'name': item.name,
                    'path': str(item),
                    'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                    'size': self._get_dir_size(item),
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def restore_backup(self, backup_path):
        """Restore from a backup"""
        import shutil
        
        backup = Path(backup_path)
        if not backup.exists():
            return {'success': False, 'error': 'Backup not found'}
        
        # Restore config files
        config_backup = backup / '.config'
        if config_backup.exists():
            shutil.copytree(config_backup, Path.home() / '.config', dirs_exist_ok=True)
        
        return {'success': True}
    
    def _get_dir_size(self, path):
        """Get directory size in bytes"""
        total = 0
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
        return total
