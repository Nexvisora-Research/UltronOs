#!/usr/bin/env python3
"""
Ultron OS - Settings Application
Main entry point for the system settings application
"""

import gi
import sys
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib

from .window import SettingsWindow


class SettingsApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='org.ultron.settings',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        
        self._window = None
    
    def do_activate(self):
        if not self._window:
            self._window = SettingsWindow(application=self)
        self._window.present()
    
    def do_startup(self):
        Adw.Application.do_startup(self)
        
        # Set up actions
        self._setup_actions()
    
    def _setup_actions(self):
        # Quit action
        quit_action = Gio.SimpleAction(name='quit')
        quit_action.connect('activate', lambda *args: self.quit())
        self.add_action(quit_action)
        
        # About action
        about_action = Gio.SimpleAction(name='about')
        about_action.connect('activate', self._on_about)
        self.add_action(about_action)
        
        # Search action
        search_action = Gio.SimpleAction(name='search')
        search_action.connect('activate', self._on_search)
        self.add_action(search_action)
        
        # Keyboard shortcuts
        self.set_accels_for_action('app.quit', ['<Ctrl>q'])
        self.set_accels_for_action('app.search', ['<Ctrl>f'])
    
    def _on_about(self, action, param):
        about = Adw.AboutWindow(
            transient_for=self._window,
            application_name='Ultron Settings',
            application_icon='org.ultron.settings',
            developer_name='Ultron OS Project',
            version='1.0.0',
            website='https://ultron.org',
            issue_url='https://ultron.org/bugs',
            license_type=Gtk.License.GPL_3_0,
            copyright='© 2024 Ultron OS Project',
            developers=['Ultron OS Team'],
            designers=['Ultron Design Team'],
        )
        about.present()
    
    def _on_search(self, action, param):
        if self._window:
            self._window.toggle_search()


def main(version):
    app = SettingsApplication()
    return app.run(sys.argv)


if __name__ == '__main__':
    main('1.0.0')
