import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class UpdatesPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Updates')
        self.set_icon_name('software-update-available-symbolic')
        
        self._build_update_header()
        self._build_app_updates()
        self._build_system_updates()
        self._build_update_settings()
    
    def _build_update_header(self):
        group = Adw.PreferencesGroup()
        
        # Status card
        status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        status_box.set_margin_top(16)
        status_box.set_margin_bottom(16)
        
        # Update icon
        icon = Gtk.Image.new_from_icon_name('software-update-available-symbolic')
        icon.set_pixel_size(64)
        icon.add_css_class('accent')
        status_box.append(icon)
        
        # Status label
        status_label = Gtk.Label(label='5 updates available')
        status_label.add_css_class('title-2')
        status_box.append(status_label)
        
        # Description
        desc_label = Gtk.Label(label='Keep your system and apps up to date for the best experience')
        desc_label.add_css_class('caption')
        desc_label.set_wrap(True)
        status_box.append(desc_label)
        
        # Update all button
        update_all_button = Gtk.Button(label='Update All')
        update_all_button.add_css_class('suggested-action')
        update_all_button.set_halign(Gtk.Align.CENTER)
        update_all_button.connect('clicked', self._on_update_all)
        status_box.append(update_all_button)
        
        group.add(status_box)
        self.add(group)
    
    def _build_app_updates(self):
        group = Adw.PreferencesGroup()
        group.set_title('Application Updates')
        
        updates = [
            ('Firefox', '121.0 → 121.0.1', 'firefox-symbolic', 'Security update'),
            ('LibreOffice', '7.6.4 → 7.6.5', 'x-office-document-symbolic', 'Bug fixes'),
            ('VS Code', '1.85.0 → 1.85.1', 'code-symbolic', 'Performance improvements'),
        ]
        
        for name, version, icon, notes in updates:
            row = Adw.ExpanderRow()
            row.set_title(name)
            row.set_subtitle(version)
            row.set_icon_name(icon)
            
            # Release notes
            notes_row = Adw.ActionRow()
            notes_row.set_title('Release Notes')
            notes_row.set_subtitle(notes)
            row.add_row(notes_row)
            
            # Size
            size_row = Adw.ActionRow()
            size_row.set_title('Download Size')
            size_row.set_subtitle('128 MB')
            row.add_row(size_row)
            
            # Update button
            update_button = Gtk.Button(label='Update')
            update_button.add_css_class('suggested-action')
            update_button.set_halign(Gtk.Align.END)
            row.add_suffix(update_button)
            
            group.add(row)
        
        self.add(group)
    
    def _build_system_updates(self):
        group = Adw.PreferencesGroup()
        group.set_title('System Updates')
        
        system_updates = [
            ('gnome-shell', '46.0-1ubuntu1 → 46.0-1ubuntu2', 'Security patches'),
            ('linux-firmware', '20231211 → 20240115', 'Hardware support'),
        ]
        
        for name, version, notes in system_updates:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(version)
            row.set_icon_name('package-x-generic-symbolic')
            
            update_button = Gtk.Button(label='Update')
            update_button.add_css_class('suggested-action')
            row.add_suffix(update_button)
            
            group.add(row)
        
        self.add(group)
    
    def _build_update_settings(self):
        group = Adw.PreferencesGroup()
        group.set_title('Update Settings')
        
        # Auto-update
        auto_row = Adw.SwitchRow()
        auto_row.set_title('Automatic Updates')
        auto_row.set_subtitle('Download and install updates automatically')
        auto_row.set_active(True)
        group.add(auto_row)
        
        # Update frequency
        freq_row = Adw.ComboRow()
        freq_row.set_title('Check Frequency')
        
        freq_model = Gtk.StringList()
        freq_model.append('Daily')
        freq_model.append('Weekly')
        freq_model.append('Monthly')
        freq_row.set_model(freq_model)
        freq_row.set_selected(0)
        group.add(freq_row)
        
        # Notify only
        notify_row = Adw.SwitchRow()
        notify_row.set_title('Notify Only')
        notify_row.set_subtitle('Show notifications but don\'t install automatically')
        group.add(notify_row)
        
        self.add(group)
    
    def _on_update_all(self, button):
        # Update all apps
        button.set_label('Updating...')
        button.set_sensitive(False)
