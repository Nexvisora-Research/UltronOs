import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class SearchPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Search')
        
        self._results_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_child(self._results_box)
    
    def search(self, query):
        # Clear previous results
        while self._results_box.get_first_child():
            self._results_box.remove(self._results_box.get_first_child())
        
        if not query:
            return
        
        # Mock search results
        results = [
            ('Firefox', 'Web browser', 'firefox-symbolic', True),
            ('File Manager', 'Browse files', 'folder-symbolic', False),
            ('Firefox Developer Edition', 'Web browser for developers', 'firefox-symbolic', True),
        ]
        
        for name, desc, icon, is_flatpak in results:
            if query.lower() in name.lower():
                row = Adw.ActionRow()
                row.set_title(name)
                row.set_subtitle(desc)
                row.set_icon_name(icon)
                row.set_activatable(True)
                
                install_button = Gtk.Button(label='Install')
                install_button.add_css_class('suggested-action')
                row.add_suffix(install_button)
                
                self._results_box.append(row)
