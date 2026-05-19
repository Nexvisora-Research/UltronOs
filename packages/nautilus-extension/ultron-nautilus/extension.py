"""
Ultron OS - Nautilus Extension
Custom toolbar, cloud integration, and quick access features for the file manager
"""

import gi
import os
import subprocess

gi.require_version('Nautilus', '4.0')
gi.require_version('Gtk', '4.0')

from gi.repository import Nautilus, Gtk, Gio, GLib


class UltronMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    """Custom context menu for Ultron OS file manager"""
    
    def __init__(self):
        super().__init__()
    
    def _open_terminal(self, menu, file):
        """Open terminal at current location"""
        if file.is_directory():
            path = file.get_location().get_path()
            subprocess.Popen(['ultron-terminal', '--working-directory', path])
        else:
            path = file.get_location().get_parent().get_path()
            subprocess.Popen(['ultron-terminal', '--working-directory', path])
    
    def _open_as_root(self, menu, file):
        """Open file manager as root"""
        path = file.get_location().get_path()
        subprocess.Popen(['pkexec', 'nautilus', path])
    
    def _copy_path(self, menu, file):
        """Copy file path to clipboard"""
        path = file.get_location().get_path()
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(path, -1)
    
    def _compress(self, menu, files):
        """Compress selected files"""
        paths = [f.get_location().get_path() for f in files]
        subprocess.Popen(['ultron-compress'] + paths)
    
    def _upload_cloud(self, menu, files):
        """Upload to cloud storage"""
        paths = [f.get_location().get_path() for f in files]
        subprocess.Popen(['ultron-cloud', 'upload'] + paths)
    
    def get_file_items(self, window, files):
        """Get context menu items for files"""
        if len(files) == 0:
            return []
        
        # Create Ultron menu
        ultron_menu = Nautilus.Menu()
        ultron_menu.append(Nautilus.MenuItem(
            name='Ultron::OpenTerminal',
            label='Open Terminal Here',
            icon='utilities-terminal-symbolic',
        ))
        
        ultron_menu.append(Nautilus.MenuItem(
            name='Ultron::CopyPath',
            label='Copy Path',
            icon='edit-copy-symbolic',
        ))
        
        if len(files) == 1:
            ultron_menu.append(Nautilus.MenuItem(
                name='Ultron::OpenAsRoot',
                label='Open as Administrator',
                icon='security-high-symbolic',
            ))
        
        if len(files) > 1:
            ultron_menu.append(Nautilus.MenuItem(
                name='Ultron::Compress',
                label='Compress...',
                icon='package-x-generic-symbolic',
            ))
        
        ultron_menu.append(Nautilus.MenuItem(
            name='Ultron::UploadCloud',
            label='Upload to Cloud',
            icon='cloud-upload-symbolic',
        ))
        
        return [ultron_menu]
    
    def get_background_items(self, window, file):
        """Get context menu items for background"""
        menu = Nautilus.Menu()
        
        menu.append(Nautilus.MenuItem(
            name='Ultron::OpenTerminal',
            label='Open Terminal Here',
            icon='utilities-terminal-symbolic',
        ))
        
        menu.append(Nautilus.MenuItem(
            name='Ultron::OpenAsRoot',
            label='Open as Administrator',
            icon='security-high-symbolic',
        ))
        
        return [menu]


class UltronLocationWidgetProvider(GObject.GObject, Nautilus.LocationWidgetProvider):
    """Custom location widget with quick access buttons"""
    
    def __init__(self):
        super().__init__()
    
    def get_widget(self, uri, window):
        """Create custom location widget"""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box.set_margin_start(8)
        box.set_margin_end(8)
        
        # Quick access buttons
        quick_access = [
            ('Home', 'user-home-symbolic', GLib.get_home_dir()),
            ('Documents', 'folder-documents-symbolic', GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOCUMENTS)),
            ('Downloads', 'folder-download-symbolic', GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)),
            ('Cloud', 'cloud-symbolic', os.path.expanduser('~/Cloud')),
        ]
        
        for label, icon, path in quick_access:
            if path and os.path.exists(path):
                button = Gtk.Button()
                button.set_tooltip_text(label)
                
                icon_widget = Gtk.Image.new_from_icon_name(icon)
                button.set_child(icon_widget)
                
                button.connect('clicked', self._on_quick_access_clicked, path, window)
                box.append(button)
        
        return box
    
    def _on_quick_access_clicked(self, button, path, window):
        """Navigate to quick access location"""
        uri = GLib.filename_to_uri(path)
        window.open_location(Gio.File.new_for_uri(uri), Nautilus.NavigationOpenFlags.OPEN)


class UltronPropertyPageProvider(GObject.GObject, Nautilus.PropertyPageProvider):
    """Custom property page for files"""
    
    def __init__(self):
        super().__init__()
    
    def get_pages(self, files):
        """Get property pages for selected files"""
        if len(files) != 1:
            return []
        
        file = files[0]
        path = file.get_location().get_path()
        
        # Create property page
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        page.set_margin_top(12)
        page.set_margin_bottom(12)
        page.set_margin_start(12)
        page.set_margin_end(12)
        
        # Cloud status
        cloud_status = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        
        cloud_icon = Gtk.Image.new_from_icon_name('cloud-symbolic')
        cloud_status.append(cloud_icon)
        
        cloud_label = Gtk.Label(label='Cloud Status: Not synced')
        cloud_status.append(cloud_label)
        
        page.append(cloud_status)
        
        # Sync button
        sync_button = Gtk.Button(label='Sync to Cloud')
        sync_button.set_halign(Gtk.Align.START)
        sync_button.connect('clicked', self._on_sync_clicked, path)
        page.append(sync_button)
        
        # Create property page widget
        property_page = Nautilus.PropertyPage(
            name='Ultron::Cloud',
            label='Ultron Cloud',
            page=page,
        )
        
        return [property_page]
    
    def _on_sync_clicked(self, button, path):
        """Sync file to cloud"""
        subprocess.Popen(['ultron-cloud', 'sync', path])
