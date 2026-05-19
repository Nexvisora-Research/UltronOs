import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class ExplorePage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Explore')
        self.set_icon_name('view-grid-symbolic')
        
        self._build_featured()
        self._build_categories()
        self._build_popular()
        self._build_new_apps()
    
    def _build_featured(self):
        group = Adw.PreferencesGroup()
        group.set_title('Featured')
        
        # Featured app carousel
        carousel = Adw.Carousel()
        carousel.set_vexpand(False)
        carousel.set_size_request(-1, 200)
        
        featured_apps = [
            {
                'name': 'Firefox',
                'description': 'Fast, private & safe web browser',
                'icon': 'firefox-symbolic',
                'color': '#FF9500',
            },
            {
                'name': 'LibreOffice',
                'description': 'Complete office suite for documents, spreadsheets, and presentations',
                'icon': 'x-office-document-symbolic',
                'color': '#1ABC9C',
            },
            {
                'name': 'Spotify',
                'description': 'Music streaming with millions of songs',
                'icon': 'audio-x-generic-symbolic',
                'color': '#1DB954',
            },
        ]
        
        for app in featured_apps:
            card = self._create_featured_card(app)
            carousel.append(card)
        
        # Carousel indicators
        indicators = Adw.CarouselIndicatorDots()
        indicators.set_carousel(carousel)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.append(carousel)
        box.append(indicators)
        
        group.add(box)
        self.add(group)
    
    def _create_featured_card(self, app):
        card = Adw.Bin()
        card.set_css_classes(['card'])
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        box.set_margin_start(24)
        box.set_margin_end(24)
        box.set_margin_top(16)
        box.set_margin_bottom(16)
        
        # App icon
        icon_box = Gtk.Box()
        icon_box.set_size_request(80, 80)
        icon_box.set_css_classes(['card'])
        icon_box.set_halign(Gtk.Align.CENTER)
        icon_box.set_valign(Gtk.Align.CENTER)
        
        icon = Gtk.Image.new_from_icon_name(app['icon'])
        icon.set_pixel_size(48)
        icon_box.append(icon)
        
        # App info
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        
        name_label = Gtk.Label(label=app['name'])
        name_label.add_css_class('title-2')
        name_label.set_halign(Gtk.Align.START)
        info_box.append(name_label)
        
        desc_label = Gtk.Label(label=app['description'])
        desc_label.add_css_class('body')
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_wrap(True)
        info_box.append(desc_label)
        
        # Install button
        install_button = Gtk.Button(label='Install')
        install_button.add_css_class('suggested-action')
        install_button.set_halign(Gtk.Align.END)
        install_button.set_valign(Gtk.Align.CENTER)
        
        box.append(icon_box)
        box.append(info_box)
        box.append(install_button)
        
        card.set_child(box)
        return card
    
    def _build_categories(self):
        group = Adw.PreferencesGroup()
        group.set_title('Browse by Category')
        
        categories = [
            ('Internet', 'web-browser-symbolic'),
            ('Office', 'x-office-document-symbolic'),
            ('Graphics', 'camera-photo-symbolic'),
            ('Development', 'code-symbolic'),
            ('Games', 'applications-games-symbolic'),
            ('Media', 'video-x-generic-symbolic'),
            ('Utilities', 'applications-utilities-symbolic'),
            ('Education', 'accessories-dictionary-symbolic'),
        ]
        
        grid = Gtk.Grid()
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.set_margin_top(12)
        grid.set_margin_bottom(12)
        
        for i, (name, icon) in enumerate(categories):
            col = i % 4
            row = i // 4
            
            button = Gtk.Button()
            button.set_size_request(100, 80)
            
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            
            icon_widget = Gtk.Image.new_from_icon_name(icon)
            icon_widget.set_pixel_size(32)
            box.append(icon_widget)
            
            label = Gtk.Label(label=name)
            label.add_css_class('caption')
            box.append(label)
            
            button.set_child(box)
            grid.attach(button, col, row, 1, 1)
        
        group.add(grid)
        self.add(group)
    
    def _build_popular(self):
        group = Adw.PreferencesGroup()
        group.set_title('Popular Apps')
        
        apps = [
            ('Firefox', 'Fast, private & safe web browser', 'firefox-symbolic', True),
            ('VS Code', 'Code editing. Redefined.', 'code-symbolic', True),
            ('Steam', 'Gaming platform', 'applications-games-symbolic', True),
            ('VLC', 'Free and open source cross-platform multimedia player', 'video-x-generic-symbolic', True),
            ('GIMP', 'GNU Image Manipulation Program', 'camera-photo-symbolic', False),
            ('Spotify', 'Music for everyone', 'audio-x-generic-symbolic', True),
        ]
        
        for name, desc, icon, is_flatpak in apps:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(desc)
            row.set_icon_name(icon)
            row.set_activatable(True)
            
            # Package type badge
            badge = Gtk.Label(label='Flatpak' if is_flatpak else 'System')
            badge.add_css_class('caption')
            badge.add_css_class('dim-label')
            row.add_suffix(badge)
            
            # Install button
            install_button = Gtk.Button(label='Install')
            install_button.add_css_class('suggested-action')
            install_button.set_halign(Gtk.Align.END)
            row.add_suffix(install_button)
            
            group.add(row)
        
        self.add(group)
    
    def _build_new_apps(self):
        group = Adw.PreferencesGroup()
        group.set_title('New & Updated')
        
        apps = [
            ('Ultron Settings', 'System settings application', 'org.ultron.settings', '2.0.0'),
            ('GNOME Builder', 'IDE for writing software for GNOME', 'code-symbolic', '45.1'),
            ('Celluloid', 'Simple GTK+ frontend for mpv', 'video-x-generic-symbolic', '0.26'),
        ]
        
        for name, desc, icon, version in apps:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(f'Updated to {version}')
            row.set_icon_name(icon)
            row.set_activatable(True)
            
            # Version badge
            badge = Gtk.Label(label=f'v{version}')
            badge.add_css_class('caption')
            badge.add_css_class('success')
            row.add_suffix(badge)
            
            group.add(row)
        
        self.add(group)
