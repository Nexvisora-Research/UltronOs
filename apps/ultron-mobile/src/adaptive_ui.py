"""
Ultron OS - Mobile/Tablet Interface Mode
Adaptive layouts for touch devices
"""

import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class AdaptiveWindow(Adw.ApplicationWindow):
    """Window that adapts to device form factor"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self._device_type = 'desktop'
        self._form_factor = 'traditional'
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Build adaptive UI"""
        # Main container
        self._main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self._main_box)
        
        # Header
        self._header = Adw.HeaderBar()
        self._header.set_show_title(True)
        self._main_box.append(self._header)
        
        # Content area
        self._content_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self._content_area.set_hexpand(True)
        self._content_area.set_vexpand(True)
        self._main_box.append(self._content_area)
        
        # Sidebar
        self._sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self._sidebar.set_size_request(250, -1)
        self._content_area.append(self._sidebar)
        
        # Main content
        self._main_content = Gtk.ScrolledWindow()
        self._main_content.set_hexpand(True)
        self._main_content.set_vexpand(True)
        self._content_area.append(self._main_content)
        
        # Bottom bar (for mobile/tablet)
        self._bottom_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self._bottom_bar.set_visible(False)
        self._main_box.append(self._bottom_bar)
        
        self._apply_adaptive_layout()
    
    def _apply_adaptive_layout(self):
        """Apply layout based on device type"""
        if self._device_type == 'phone':
            self._apply_phone_layout()
        elif self._device_type == 'tablet':
            self._apply_tablet_layout()
        else:
            self._apply_desktop_layout()
    
    def _apply_phone_layout(self):
        """Apply phone-optimized layout"""
        self.set_default_size(400, 800)
        
        # Hide sidebar, show bottom navigation
        self._sidebar.set_visible(False)
        self._bottom_bar.set_visible(True)
        
        # Full-screen header
        self._header.set_show_title(True)
        
        # Add bottom navigation buttons
        nav_buttons = [
            ('Home', 'user-home-symbolic'),
            ('Search', 'system-search-symbolic'),
            ('Settings', 'system-run-symbolic'),
        ]
        
        for label, icon in nav_buttons:
            button = Gtk.Button()
            button.set_hexpand(True)
            
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            
            icon_widget = Gtk.Image.new_from_icon_name(icon)
            icon_widget.set_pixel_size(24)
            box.append(icon_widget)
            
            label_widget = Gtk.Label(label=label)
            label_widget.add_css_class('caption')
            box.append(label_widget)
            
            button.set_child(box)
            self._bottom_bar.append(button)
    
    def _apply_tablet_layout(self):
        """Apply tablet-optimized layout"""
        self.set_default_size(800, 1200)
        
        # Show sidebar but make it collapsible
        self._sidebar.set_visible(True)
        self._sidebar.set_size_request(200, -1)
        self._bottom_bar.set_visible(False)
        
        # Larger touch targets
        self._apply_touch_optimization()
    
    def _apply_desktop_layout(self):
        """Apply desktop layout"""
        self.set_default_size(1200, 800)
        
        # Full sidebar
        self._sidebar.set_visible(True)
        self._sidebar.set_size_request(250, -1)
        self._bottom_bar.set_visible(False)
    
    def _apply_touch_optimization(self):
        """Optimize for touch input"""
        # Increase button sizes
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(b"""
            button {
                min-height: 48px;
                min-width: 48px;
                padding: 12px;
            }
            
            list row {
                min-height: 56px;
                padding: 12px;
            }
        """)
        
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def set_device_type(self, device_type):
        """Set device type and reapply layout"""
        self._device_type = device_type
        self._apply_adaptive_layout()
    
    def set_form_factor(self, form_factor):
        """Set form factor"""
        self._form_factor = form_factor
        
        if form_factor in ['touch', 'hybrid']:
            self._apply_touch_optimization()


class MobileSettingsPage(Adw.PreferencesPage):
    """Settings page optimized for mobile/tablet"""
    
    def __init__(self):
        super().__init__()
        
        self._build_mobile_layout()
    
    def _build_mobile_layout(self):
        """Build mobile-optimized settings"""
        # Use larger cards for touch
        group = Adw.PreferencesGroup()
        group.set_title('Display')
        
        # Larger rows for touch
        settings = [
            ('Brightness', 'display-brightness-symbolic'),
            ('Night Light', 'night-light-symbolic'),
            ('Auto-Rotate', 'object-rotate-right-symbolic'),
            ('Font Size', 'preferences-desktop-font-symbolic'),
        ]
        
        for name, icon in settings:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_icon_name(icon)
            row.set_activatable(True)
            
            # Larger touch target
            row.add_suffix(Gtk.Button.new_from_icon_name('go-next-symbolic'))
            
            group.add(row)
        
        self.add(group)


class TabletShell(Adw.Application):
    """Shell application for tablet mode"""
    
    def __init__(self):
        super().__init__(
            application_id='org.ultron.tablet-shell',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
    
    def do_activate(self):
        win = AdaptiveWindow(application=self)
        win.set_device_type('tablet')
        win.set_form_factor('touch')
        win.present()
