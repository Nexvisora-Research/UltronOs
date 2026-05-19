import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib

from .pages.explore import ExplorePage
from .pages.search import SearchPage
from .pages.installed import InstalledPage
from .pages.updates import UpdatesPage
from .pages.app_detail import AppDetailPage


class StoreWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_title('Ultron Store')
        self.set_default_size(1100, 750)
        self.set_resizable(True)
        
        self._setup_ui()
        self._setup_pages()
    
    def _setup_ui(self):
        # Main layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # Header bar
        header = Adw.HeaderBar()
        header.set_show_title(True)
        main_box.append(header)
        
        # Search bar
        self._search_bar = Gtk.SearchBar()
        self._search_entry = Gtk.SearchEntry()
        self._search_entry.connect('search-changed', self._on_search_changed)
        self._search_bar.set_child(self._search_entry)
        main_box.append(self._search_bar)
        
        # Tab bar
        self._tab_bar = Adw.TabBar()
        self._tab_bar.set_autohide(False)
        main_box.append(self._tab_bar)
        
        # Stack for pages
        self._stack = Gtk.Stack()
        self._stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        main_box.append(self._stack)
        
        # Status bar
        self._status_bar = Gtk.Label()
        self._status_bar.add_css_class('caption')
        self._status_bar.set_margin_start(12)
        self._status_bar.set_margin_end(12)
        self._status_bar.set_margin_bottom(8)
        self._status_bar.set_halign(Gtk.Align.START)
        main_box.append(self._status_bar)
        
        # Build tabs
        self._build_tabs()
    
    def _build_tabs(self):
        tabs = [
            ('Explore', 'view-grid-symbolic', 'explore'),
            ('Categories', 'view-more-symbolic', 'categories'),
            ('Installed', 'software-installed-symbolic', 'installed'),
            ('Updates', 'software-update-available-symbolic', 'updates'),
        ]
        
        for title, icon, page_id in tabs:
            page = Adw.NavigationPage()
            page.set_title(title)
            page.set_tag(page_id)
            
            self._stack.add_named(page, page_id)
            
            tab = self._tab_bar.append(page)
    
    def _setup_pages(self):
        self._pages = {
            'explore': ExplorePage(),
            'categories': self._build_categories_page(),
            'installed': InstalledPage(),
            'updates': UpdatesPage(),
        }
        
        for page_id, page in self._pages.items():
            if page_id in self._stack:
                self._stack.get_child_by_name(page_id).set_child(page)
    
    def _build_categories_page(self):
        page = Adw.PreferencesPage()
        page.set_title('Categories')
        
        categories = [
            ('Internet', 'web-browser-symbolic', ['Firefox', 'Chrome', 'Thunderbird']),
            ('Office', 'x-office-document-symbolic', ['LibreOffice', 'OnlyOffice', 'WPS Office']),
            ('Graphics', 'camera-photo-symbolic', ['GIMP', 'Inkscape', 'Krita']),
            ('Development', 'code-symbolic', ['VS Code', 'GNOME Builder', 'Git']),
            ('Games', 'applications-games-symbolic', ['Steam', 'Lutris', 'Heroic']),
            ('Media', 'video-x-generic-symbolic', ['VLC', 'Spotify', 'Celluloid']),
            ('Utilities', 'applications-utilities-symbolic', ['GNOME Tweaks', 'Timeshift', 'BleachBit']),
            ('Education', 'accessories-dictionary-symbolic', ['KDE Edu', 'GCompris', 'Stellarium']),
        ]
        
        for name, icon, apps in categories:
            group = Adw.PreferencesGroup()
            group.set_title(name)
            
            for app in apps:
                row = Adw.ActionRow()
                row.set_title(app)
                row.set_icon_name(icon)
                row.set_activatable(True)
                group.add(row)
            
            page.add(group)
        
        return page
    
    def _on_search_changed(self, entry):
        query = entry.get_text()
        if query:
            self._show_search_results(query)
    
    def _show_search_results(self, query):
        # Show search results
        pass
    
    def toggle_search(self):
        self._search_bar.set_search_mode(not self._search_bar.get_search_mode())
        if self._search_bar.get_search_mode():
            self._search_entry.grab_focus()
