#!/usr/bin/env python3
"""
Ultron OS - Update Manager
System and application update management
"""

import gi
import sys
import subprocess
import threading

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class UpdaterWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_title('Ultron Updater')
        self.set_default_size(800, 600)
        
        self._updates = []
        self._updating = False
        
        self._build_ui()
        self._check_for_updates()
    
    def _build_ui(self):
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # Header
        header = Adw.HeaderBar()
        header.set_show_title(True)
        main_box.append(header)
        
        # Refresh button
        refresh_button = Gtk.Button.new_from_icon_name('view-refresh-symbolic')
        refresh_button.connect('clicked', self._on_refresh)
        header.pack_end(refresh_button)
        
        # Status banner
        self._banner = Adw.Banner()
        self._banner.set_revealed(False)
        main_box.append(self._banner)
        
        # Content area
        self._stack = Gtk.Stack()
        main_box.append(self._stack)
        
        # Loading view
        loading_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        loading_box.set_halign(Gtk.Align.CENTER)
        loading_box.set_valign(Gtk.Align.CENTER)
        
        spinner = Gtk.Spinner()
        spinner.set_spinning(True)
        loading_box.append(spinner)
        
        loading_label = Gtk.Label(label='Checking for updates...')
        loading_box.append(loading_label)
        
        self._stack.add_named(loading_box, 'loading')
        
        # No updates view
        no_updates_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        no_updates_box.set_halign(Gtk.Align.CENTER)
        no_updates_box.set_valign(Gtk.Align.CENTER)
        
        check_icon = Gtk.Image.new_from_icon_name('object-select-symbolic')
        check_icon.set_pixel_size(64)
        check_icon.add_css_class('success')
        no_updates_box.append(check_icon)
        
        no_updates_label = Gtk.Label(label='Your system is up to date')
        no_updates_label.add_css_class('title-2')
        no_updates_box.append(no_updates_label)
        
        self._stack.add_named(no_updates_box, 'no-updates')
        
        # Updates available view
        updates_page = Adw.PreferencesPage()
        self._stack.add_named(updates_page, 'updates')
        
        # System updates group
        self._system_group = Adw.PreferencesGroup()
        self._system_group.set_title('System Updates')
        updates_page.add(self._system_group)
        
        # App updates group
        self._app_group = Adw.PreferencesGroup()
        self._app_group.set_title('Application Updates')
        updates_page.add(self._app_group)
        
        # Update actions
        actions_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        actions_box.set_margin_top(12)
        actions_box.set_margin_bottom(12)
        actions_box.set_margin_start(12)
        actions_box.set_margin_end(12)
        
        self._update_all_button = Gtk.Button(label='Update All')
        self._update_all_button.add_css_class('suggested-action')
        self._update_all_button.set_hexpand(True)
        self._update_all_button.connect('clicked', self._on_update_all)
        actions_box.append(self._update_all_button)
        
        self._stack.add_named(actions_box, 'actions')
        
        # Progress view
        progress_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        progress_box.set_margin_start(24)
        progress_box.set_margin_end(24)
        progress_box.set_halign(Gtk.Align.CENTER)
        progress_box.set_valign(Gtk.Align.CENTER)
        
        self._progress_bar = Gtk.ProgressBar()
        self._progress_bar.set_hexpand(True)
        progress_box.append(self._progress_bar)
        
        self._progress_label = Gtk.Label(label='Preparing updates...')
        progress_box.append(self._progress_label)
        
        self._stack.add_named(progress_box, 'progress')
    
    def _check_for_updates(self):
        self._stack.set_visible_child_name('loading')
        
        # Run in background thread
        thread = threading.Thread(target=self._fetch_updates)
        thread.start()
    
    def _fetch_updates(self):
        # Simulate checking for updates
        GLib.idle_add(self._show_updates)
    
    def _show_updates(self):
        self._updates = [
            {'name': 'gnome-shell', 'version': '46.0-1ubuntu2', 'type': 'system', 'size': '45 MB'},
            {'name': 'linux-firmware', 'version': '20240115', 'type': 'system', 'size': '128 MB'},
            {'name': 'Firefox', 'version': '121.0.1', 'type': 'app', 'size': '85 MB'},
            {'name': 'LibreOffice', 'version': '7.6.5', 'type': 'app', 'size': '256 MB'},
            {'name': 'VS Code', 'version': '1.85.1', 'type': 'app', 'size': '95 MB'},
        ]
        
        if not self._updates:
            self._stack.set_visible_child_name('no-updates')
            return
        
        # Add system updates
        for update in self._updates:
            if update['type'] == 'system':
                row = Adw.ActionRow()
                row.set_title(update['name'])
                row.set_subtitle(f'Version {update["version"]} • {update["size"]}')
                row.set_icon_name('package-x-generic-symbolic')
                
                checkbox = Gtk.CheckButton()
                checkbox.set_active(True)
                row.add_suffix(checkbox)
                
                self._system_group.add(row)
            else:
                row = Adw.ActionRow()
                row.set_title(update['name'])
                row.set_subtitle(f'Version {update["version"]} • {update["size"]}')
                row.set_icon_name('application-x-executable-symbolic')
                
                checkbox = Gtk.CheckButton()
                checkbox.set_active(True)
                row.add_suffix(checkbox)
                
                self._app_group.add(row)
        
        # Update banner
        self._banner.set_title(f'{len(self._updates)} updates available')
        self._banner.set_revealed(True)
        
        self._stack.set_visible_child_name('updates')
    
    def _on_refresh(self, button):
        self._check_for_updates()
    
    def _on_update_all(self, button):
        self._stack.set_visible_child_name('progress')
        self._update_all_button.set_sensitive(False)
        
        # Simulate update progress
        self._simulate_update()
    
    def _simulate_update(self):
        progress = 0
        total = len(self._updates)
        
        def update_progress():
            nonlocal progress
            progress += 1
            
            fraction = progress / total
            self._progress_bar.set_fraction(fraction)
            self._progress_label.set_label(f'Updating {progress} of {total}...')
            
            if progress < total:
                GLib.timeout_add(1000, update_progress)
            else:
                self._progress_label.set_label('Updates complete!')
                self._update_all_button.set_sensitive(True)
                GLib.timeout_add(2000, self._on_update_complete)
        
        GLib.timeout_add(1000, update_progress)
    
    def _on_update_complete(self):
        self._banner.set_title('All updates installed successfully')
        self._banner.set_revealed(True)
        self._stack.set_visible_child_name('no-updates')


class UpdaterApplication(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        win = UpdaterWindow(application=app)
        win.present()


def main(version):
    app = UpdaterApplication(application_id='org.ultron.updater')
    return app.run(sys.argv)


if __name__ == '__main__':
    main('1.0.0')
