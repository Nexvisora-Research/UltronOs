#!/usr/bin/env python3
"""
Ultron OS - App Store
Flatpak and APT package management application
"""

import gi
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib

from .window import StoreWindow


class StoreApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='org.ultron.store',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        
        self._window = None
    
    def do_activate(self):
        if not self._window:
            self._window = StoreWindow(application=self)
        self._window.present()
    
    def do_startup(self):
        Adw.Application.do_startup(self)
        
        # Set up actions
        quit_action = Gio.SimpleAction(name='quit')
        quit_action.connect('activate', lambda *args: self.quit())
        self.add_action(quit_action)
        
        search_action = Gio.SimpleAction(name='search')
        search_action.connect('activate', self._on_search)
        self.add_action(search_action)
        
        self.set_accels_for_action('app.quit', ['<Ctrl>q'])
        self.set_accels_for_action('app.search', ['<Ctrl>f'])
    
    def _on_search(self, action, param):
        if self._window:
            self._window.toggle_search()


def main(version):
    app = StoreApplication()
    return app.run(sys.argv)


if __name__ == '__main__':
    main('1.0.0')
