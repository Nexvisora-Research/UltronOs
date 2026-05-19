import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class InstalledPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Installed')
        self.set_icon_name('software-installed-symbolic')
        
        self._build_installed_apps()
        self._build_system_packages()
    
    def _build_installed_apps(self):
        group = Adw.PreferencesGroup()
        group.set_title('Applications')
        
        apps = [
            ('Firefox', 'Web browser', 'firefox-symbolic', '121.0', 'Flatpak'),
            ('LibreOffice', 'Office suite', 'x-office-document-symbolic', '7.6.4', 'Flatpak'),
            ('VS Code', 'Code editor', 'code-symbolic', '1.85.1', 'Flatpak'),
            ('Spotify', 'Music streaming', 'audio-x-generic-symbolic', '1.2.25', 'Flatpak'),
            ('VLC', 'Media player', 'video-x-generic-symbolic', '3.0.20', 'Flatpak'),
            ('GIMP', 'Image editor', 'camera-photo-symbolic', '2.10.36', 'Flatpak'),
        ]
        
        for name, desc, icon, version, source in apps:
            row = Adw.ExpanderRow()
            row.set_title(name)
            row.set_subtitle(f'{desc} • {version}')
            row.set_icon_name(icon)
            
            # Version info
            version_row = Adw.ActionRow()
            version_row.set_title('Version')
            version_row.set_subtitle(version)
            row.add_row(version_row)
            
            # Source info
            source_row = Adw.ActionRow()
            source_row.set_title('Source')
            source_row.set_subtitle(source)
            row.add_row(source_row)
            
            # Size info
            size_row = Adw.ActionRow()
            size_row.set_title('Size')
            size_row.set_subtitle('256 MB')
            row.add_row(size_row)
            
            # Last updated
            updated_row = Adw.ActionRow()
            updated_row.set_title('Last Updated')
            updated_row.set_subtitle('2 days ago')
            row.add_row(updated_row)
            
            # Action buttons
            actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            actions_box.set_margin_top(8)
            actions_box.set_margin_bottom(8)
            
            update_button = Gtk.Button(label='Update')
            update_button.add_css_class('suggested-action')
            actions_box.append(update_button)
            
            remove_button = Gtk.Button(label='Remove')
            remove_button.add_css_class('destructive-action')
            actions_box.append(remove_button)
            
            row.add_row(Adw.ActionRow())
            row.get_last_child().set_child(actions_box)
            
            group.add(row)
        
        self.add(group)
    
    def _build_system_packages(self):
        group = Adw.PreferencesGroup()
        group.set_title('System Packages')
        group.set_description('Packages installed via APT')
        
        packages = [
            ('gnome-shell', '46.0'),
            ('nautilus', '45.2'),
            ('gnome-terminal', '3.50.1'),
            ('gimp', '2.10.36'),
        ]
        
        for name, version in packages:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(f'Version {version}')
            row.set_icon_name('package-x-generic-symbolic')
            
            remove_button = Gtk.Button(label='Remove')
            remove_button.add_css_class('destructive-action')
            row.add_suffix(remove_button)
            
            group.add(row)
        
        self.add(group)
