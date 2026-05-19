import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib

from .pages.appearance import AppearancePage
from .pages.network import NetworkPage
from .pages.bluetooth import BluetoothPage
from .pages.sound import SoundPage
from .pages.display import DisplayPage
from .pages.notifications import NotificationsPage
from .pages.privacy import PrivacyPage
from .pages.accounts import AccountsPage
from .pages.system import SystemPage
from .pages.about import AboutPage


class SettingsWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_title('Ultron Settings')
        self.set_default_size(900, 700)
        self.set_resizable(True)
        
        # Create layout
        self._setup_ui()
        
        # Initialize pages
        self._pages = {}
        self._setup_pages()
    
    def _setup_ui(self):
        # Main split view
        self._split = Adw.NavigationSplitView()
        self.set_content(self._split)
        
        # Sidebar
        self._sidebar = Adw.NavigationPage()
        self._sidebar.set_title('Settings')
        
        # Sidebar content
        sidebar_toolbar = Adw.ToolbarView()
        self._sidebar.set_child(sidebar_toolbar)
        
        # Search bar
        self._search_bar = Gtk.SearchBar()
        self._search_entry = Gtk.SearchEntry()
        self._search_entry.connect('search-changed', self._on_search_changed)
        self._search_entry.connect('stop-search', self._on_search_stop)
        self._search_bar.set_child(self._search_entry)
        sidebar_toolbar.add_top_bar(self._search_bar)
        
        # Sidebar header
        header = Adw.HeaderBar()
        header.set_show_title(False)
        sidebar_toolbar.add_top_bar(header)
        
        # Navigation view for sidebar
        self._sidebar_nav = Adw.NavigationView()
        self._sidebar_page = Adw.NavigationPage()
        self._sidebar_page.set_title('Settings')
        sidebar_toolbar.set_content(self._sidebar_nav)
        self._sidebar_nav.push(self._sidebar_page)
        
        # Sidebar list
        self._sidebar_list = Adw.PreferencesPage()
        self._sidebar_page.set_child(self._sidebar_list)
        
        # Content area
        self._content_page = Adw.NavigationPage()
        self._content_page.set_title('Settings')
        
        self._content_toolbar = Adw.ToolbarView()
        self._content_page.set_child(self._content_toolbar)
        
        # Content header
        self._content_header = Adw.HeaderBar()
        self._content_header.set_show_title(True)
        self._content_toolbar.add_top_bar(self._content_header)
        
        # Content navigation view
        self._content_nav = Adw.NavigationView()
        self._content_nav_page = Adw.NavigationPage()
        self._content_nav_page.set_title('Settings')
        self._content_toolbar.set_content(self._content_nav)
        self._content_nav.push(self._content_nav_page)
        
        # Set up split view
        self._split.set_sidebar(self._sidebar)
        self._split.set_content(self._content_page)
        self._split.set_collapsed(True)
        
        # Build sidebar
        self._build_sidebar()
        
        # Show default page
        self._show_page('appearance')
    
    def _build_sidebar(self):
        # Create categories
        categories = [
            {
                'title': 'Appearance',
                'icon': 'brush-symbolic',
                'id': 'appearance',
            },
            {
                'title': 'Network',
                'icon': 'network-wireless-symbolic',
                'id': 'network',
            },
            {
                'title': 'Bluetooth',
                'icon': 'bluetooth-active-symbolic',
                'id': 'bluetooth',
            },
            {
                'title': 'Sound',
                'icon': 'audio-speakers-symbolic',
                'id': 'sound',
            },
            {
                'title': 'Display',
                'icon': 'display-symbolic',
                'id': 'display',
            },
            {
                'title': 'Notifications',
                'icon': 'preferences-system-notifications-symbolic',
                'id': 'notifications',
            },
            {
                'title': 'Privacy & Security',
                'icon': 'system-lock-symbolic',
                'id': 'privacy',
            },
            {
                'title': 'Accounts',
                'icon': 'system-users-symbolic',
                'id': 'accounts',
            },
            {
                'title': 'System',
                'icon': 'system-run-symbolic',
                'id': 'system',
            },
            {
                'title': 'About',
                'icon': 'dialog-information-symbolic',
                'id': 'about',
            },
        ]
        
        # Create groups
        appearance_group = Adw.PreferencesGroup()
        network_group = Adw.PreferencesGroup()
        system_group = Adw.PreferencesGroup()
        
        for cat in categories:
            row = Adw.ActionRow()
            row.set_title(cat['title'])
            row.set_icon_name(cat['icon'])
            row.set_activatable(True)
            row.connect('activated', self._on_row_activated, cat['id'])
            
            if cat['id'] in ['appearance', 'network', 'bluetooth', 'sound', 'display', 'notifications']:
                appearance_group.add(row)
            elif cat['id'] in ['privacy', 'accounts']:
                network_group.add(row)
            else:
                system_group.add(row)
        
        self._sidebar_list.add(appearance_group)
        self._sidebar_list.add(network_group)
        self._sidebar_list.add(system_group)
    
    def _setup_pages(self):
        self._pages = {
            'appearance': AppearancePage(),
            'network': NetworkPage(),
            'bluetooth': BluetoothPage(),
            'sound': SoundPage(),
            'display': DisplayPage(),
            'notifications': NotificationsPage(),
            'privacy': PrivacyPage(),
            'accounts': AccountsPage(),
            'system': SystemPage(),
            'about': AboutPage(),
        }
    
    def _show_page(self, page_id):
        if page_id not in self._pages:
            return
        
        page = self._pages[page_id]
        self._content_nav_page.set_child(page)
        
        # Update title
        for cat in self._sidebar_list:
            for row in cat:
                if hasattr(row, 'get_title') and row.get_title():
                    # Find matching category
                    pass
        
        # Update sidebar selection
        self._update_sidebar_selection(page_id)
    
    def _update_sidebar_selection(self, page_id):
        # Visual feedback for selected item
        pass
    
    def _on_row_activated(self, row, page_id):
        self._show_page(page_id)
        
        # Collapse sidebar on mobile
        if self._split.get_collapsed():
            self._split.set_show_content(True)
    
    def _on_search_changed(self, entry):
        query = entry.get_text()
        if query:
            self._search_pages(query)
    
    def _on_search_stop(self, entry):
        self._search_entry.set_text('')
    
    def _search_pages(self, query):
        # Search through all pages
        pass
    
    def toggle_search(self):
        self._search_bar.set_search_mode(not self._search_bar.get_search_mode())
        if self._search_bar.get_search_mode():
            self._search_entry.grab_focus()
