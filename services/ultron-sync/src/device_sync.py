"""
Ultron OS - Device Synchronization Framework
Sync settings, files, and state across devices
"""

import os
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime


class DeviceSync:
    """Synchronizes settings and state across devices"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'ultron' / 'sync'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'sync.json'
        self.config = self._load_config()
        
        self._syncing = False
    
    def _load_config(self):
        """Load sync configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'device_id': self._generate_device_id(),
            'device_name': self._get_hostname(),
            'sync_enabled': True,
            'sync_items': {
                'settings': True,
                'bookmarks': True,
                'wallpaper': True,
                'themes': True,
                'keybindings': True,
                'app_config': True,
            },
            'sync_interval': 300,  # 5 minutes
            'last_sync': None,
        }
    
    def save_config(self):
        """Save sync configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _generate_device_id(self):
        """Generate unique device ID"""
        import uuid
        return str(uuid.uuid4())
    
    def _get_hostname(self):
        """Get device hostname"""
        try:
            return subprocess.run(
                ['hostname'],
                capture_output=True, text=True
            ).stdout.strip()
        except Exception:
            return 'ultron-device'
    
    def get_sync_status(self):
        """Get sync status"""
        return {
            'device_id': self.config['device_id'],
            'device_name': self.config['device_name'],
            'sync_enabled': self.config['sync_enabled'],
            'last_sync': self.config['last_sync'],
            'sync_items': self.config['sync_items'],
        }
    
    def sync_now(self):
        """Trigger immediate sync"""
        if self._syncing:
            return {'success': False, 'message': 'Sync already in progress'}
        
        self._syncing = True
        thread = threading.Thread(target=self._do_sync)
        thread.start()
        
        return {'success': True, 'message': 'Sync started'}
    
    def _do_sync(self):
        """Perform actual sync"""
        try:
            sync_items = self.config['sync_items']
            
            if sync_items.get('settings'):
                self._sync_settings()
            
            if sync_items.get('bookmarks'):
                self._sync_bookmarks()
            
            if sync_items.get('wallpaper'):
                self._sync_wallpaper()
            
            if sync_items.get('themes'):
                self._sync_themes()
            
            if sync_items.get('keybindings'):
                self._sync_keybindings()
            
            if sync_items.get('app_config'):
                self._sync_app_config()
            
            self.config['last_sync'] = datetime.now().isoformat()
            self.save_config()
        except Exception as e:
            print(f'Sync failed: {str(e)}')
        finally:
            self._syncing = False
    
    def _sync_settings(self):
        """Sync GSettings"""
        # Export settings
        settings_dir = self.config_dir / 'settings'
        settings_dir.mkdir(exist_ok=True)
        
        schemas = [
            'org.gnome.desktop.interface',
            'org.gnome.desktop.background',
            'org.gnome.shell.extensions.dash-to-dock',
            'org.ultron.shell',
        ]
        
        for schema in schemas:
            try:
                result = subprocess.run(
                    ['gsettings', 'list-recursively', schema],
                    capture_output=True, text=True
                )
                
                settings_file = settings_dir / f'{schema}.txt'
                settings_file.write_text(result.stdout)
            except Exception:
                pass
    
    def _sync_bookmarks(self):
        """Sync GTK bookmarks"""
        bookmarks_file = Path.home() / '.config' / 'gtk-4.0' / 'bookmarks'
        
        if bookmarks_file.exists():
            dest = self.config_dir / 'bookmarks'
            dest.mkdir(exist_ok=True)
            
            import shutil
            shutil.copy2(bookmarks_file, dest / 'bookmarks')
    
    def _sync_wallpaper(self):
        """Sync wallpaper"""
        wallpaper_dir = self.config_dir / 'wallpaper'
        wallpaper_dir.mkdir(exist_ok=True)
        
        # Get current wallpaper
        try:
            result = subprocess.run(
                ['gsettings', 'get', 'org.gnome.desktop.background', 'picture-uri'],
                capture_output=True, text=True
            )
            
            wallpaper_path = result.stdout.strip().strip("'").replace('file://', '')
            
            if wallpaper_path and Path(wallpaper_path).exists():
                import shutil
                shutil.copy2(wallpaper_path, wallpaper_dir / 'current-wallpaper')
        except Exception:
            pass
    
    def _sync_themes(self):
        """Sync theme configuration"""
        themes_dir = self.config_dir / 'themes'
        themes_dir.mkdir(exist_ok=True)
        
        themes = {
            'gtk-theme': None,
            'icon-theme': None,
            'cursor-theme': None,
            'font-name': None,
        }
        
        settings = [
            ('org.gnome.desktop.interface', 'gtk-theme'),
            ('org.gnome.desktop.interface', 'icon-theme'),
            ('org.gnome.desktop.interface', 'cursor-theme'),
            ('org.gnome.desktop.interface', 'font-name'),
        ]
        
        for schema, key in settings:
            try:
                result = subprocess.run(
                    ['gsettings', 'get', schema, key],
                    capture_output=True, text=True
                )
                themes[key] = result.stdout.strip().strip("'")
            except Exception:
                pass
        
        themes_file = themes_dir / 'themes.json'
        with open(themes_file, 'w') as f:
            json.dump(themes, f, indent=2)
    
    def _sync_keybindings(self):
        """Sync keyboard shortcuts"""
        keybindings_dir = self.config_dir / 'keybindings'
        keybindings_dir.mkdir(exist_ok=True)
        
        try:
            result = subprocess.run(
                ['gsettings', 'list-recursively', 'org.gnome.settings-daemon.plugins.media-keys'],
                capture_output=True, text=True
            )
            
            keybindings_file = keybindings_dir / 'custom-keybindings.txt'
            keybindings_file.write_text(result.stdout)
        except Exception:
            pass
    
    def _sync_app_config(self):
        """Sync application configurations"""
        config_dir = self.config_dir / 'app-config'
        config_dir.mkdir(exist_ok=True)
        
        # Sync Ultron app configs
        ultron_config = Path.home() / '.config' / 'ultron'
        
        if ultron_config.exists():
            import shutil
            for item in ultron_config.iterdir():
                if item.is_file():
                    shutil.copy2(item, config_dir / item.name)
    
    def apply_sync(self):
        """Apply synced settings from other devices"""
        results = []
        
        sync_items = self.config['sync_items']
        
        if sync_items.get('settings'):
            results.extend(self._apply_settings())
        
        if sync_items.get('themes'):
            results.extend(self._apply_themes())
        
        if sync_items.get('bookmarks'):
            results.extend(self._apply_bookmarks())
        
        return results
    
    def _apply_settings(self):
        """Apply synced settings"""
        results = []
        
        settings_dir = self.config_dir / 'settings'
        
        if settings_dir.exists():
            for settings_file in settings_dir.glob('*.txt'):
                try:
                    content = settings_file.read_text()
                    
                    for line in content.split('\n'):
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 3:
                                schema = parts[0]
                                key = parts[1]
                                value = ' '.join(parts[2:])
                                
                                subprocess.run(
                                    ['gsettings', 'set', schema, key, value],
                                    capture_output=True
                                )
                    
                    results.append(f'Applied {settings_file.name}')
                except Exception as e:
                    results.append(f'Failed to apply {settings_file.name}: {str(e)}')
        
        return results
    
    def _apply_themes(self):
        """Apply synced themes"""
        results = []
        
        themes_file = self.config_dir / 'themes' / 'themes.json'
        
        if themes_file.exists():
            with open(themes_file, 'r') as f:
                themes = json.load(f)
            
            for key, value in themes.items():
                if value:
                    try:
                        subprocess.run(
                            ['gsettings', 'set', 'org.gnome.desktop.interface', key, value],
                            capture_output=True
                        )
                        results.append(f'Applied {key}: {value}')
                    except Exception as e:
                        results.append(f'Failed to apply {key}: {str(e)}')
        
        return results
    
    def _apply_bookmarks(self):
        """Apply synced bookmarks"""
        results = []
        
        bookmarks_file = self.config_dir / 'bookmarks' / 'bookmarks'
        
        if bookmarks_file.exists():
            dest = Path.home() / '.config' / 'gtk-4.0' / 'bookmarks'
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            import shutil
            shutil.copy2(bookmarks_file, dest)
            results.append('Applied bookmarks')
        
        return results
