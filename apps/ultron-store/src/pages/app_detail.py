import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class AppDetailPage(Adw.NavigationPage):
    def __init__(self, app_id=None):
        super().__init__()
        self.set_title('App Details')
        
        self._app_id = app_id
        
        self._build_ui()
    
    def _build_ui(self):
        toolbar = Adw.ToolbarView()
        self.set_child(toolbar)
        
        # Header
        header = Adw.HeaderBar()
        toolbar.add_top_bar(header)
        
        # Scrollable content
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        toolbar.set_content(scroll)
        
        content = Adw.PreferencesPage()
        scroll.set_child(content)
        
        self._build_app_header(content)
        self._build_screenshots(content)
        self._build_description(content)
        self._build_info(content)
        self._build_reviews(content)
    
    def _build_app_header(self, page):
        group = Adw.PreferencesGroup()
        
        # App info box
        app_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        app_box.set_margin_top(16)
        app_box.set_margin_bottom(16)
        
        # App icon
        icon_box = Gtk.Box()
        icon_box.set_size_request(100, 100)
        icon_box.set_css_classes(['card'])
        icon_box.set_halign(Gtk.Align.CENTER)
        icon_box.set_valign(Gtk.Align.CENTER)
        
        icon = Gtk.Image.new_from_icon_name('firefox-symbolic')
        icon.set_pixel_size(64)
        icon_box.append(icon)
        
        # App details
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        
        name_label = Gtk.Label(label='Firefox')
        name_label.add_css_class('title-1')
        name_label.set_halign(Gtk.Align.START)
        info_box.append(name_label)
        
        developer_label = Gtk.Label(label='Mozilla')
        developer_label.add_css_class('caption')
        developer_label.set_halign(Gtk.Align.START)
        info_box.append(developer_label)
        
        category_label = Gtk.Label(label='Internet')
        category_label.add_css_class('caption')
        category_label.add_css_class('dim-label')
        category_label.set_halign(Gtk.Align.START)
        info_box.append(category_label)
        
        # Install button
        install_button = Gtk.Button(label='Install')
        install_button.add_css_class('suggested-action')
        install_button.set_size_request(120, 40)
        install_button.set_halign(Gtk.Align.END)
        install_button.set_valign(Gtk.Align.CENTER)
        
        app_box.append(icon_box)
        app_box.append(info_box)
        app_box.append(install_button)
        
        group.add(app_box)
        page.add(group)
    
    def _build_screenshots(self, page):
        group = Adw.PreferencesGroup()
        group.set_title('Screenshots')
        
        carousel = Adw.Carousel()
        
        for i in range(3):
            screenshot = Gtk.Box()
            screenshot.set_size_request(400, 250)
            screenshot.set_css_classes(['card'])
            carousel.append(screenshot)
        
        indicators = Adw.CarouselIndicatorDots()
        indicators.set_carousel(carousel)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.append(carousel)
        box.append(indicators)
        
        group.add(box)
        page.add(group)
    
    def _build_description(self, page):
        group = Adw.PreferencesGroup()
        group.set_title('About')
        
        desc_label = Gtk.Label(label='Mozilla Firefox is a free and open-source web browser developed by the Mozilla Foundation. It features a fast rendering engine, strong privacy protections, and extensive customization options.')
        desc_label.set_wrap(True)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_margin_top(8)
        desc_label.set_margin_bottom(8)
        
        group.add(desc_label)
        page.add(group)
    
    def _build_info(self, page):
        group = Adw.PreferencesGroup()
        group.set_title('Information')
        
        info = [
            ('Version', '121.0'),
            ('Updated', 'December 20, 2024'),
            ('Size', '256 MB'),
            ('License', 'MPL-2.0'),
            ('Source', 'Flathub'),
        ]
        
        for label, value in info:
            row = Adw.ActionRow()
            row.set_title(label)
            row.set_subtitle(value)
            group.add(row)
        
        page.add(group)
    
    def _build_reviews(self, page):
        group = Adw.PreferencesGroup()
        group.set_title('Reviews')
        
        # Rating summary
        rating_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        rating_box.set_margin_top(12)
        rating_box.set_margin_bottom(12)
        
        # Average rating
        avg_label = Gtk.Label(label='4.5')
        avg_label.add_css_class('title-1')
        rating_box.append(avg_label)
        
        # Stars
        stars_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        
        for i in range(5):
            star = Gtk.Image.new_from_icon_name('starred-symbolic' if i < 4 else 'non-starred-symbolic')
            stars_box.append(star)
        
        rating_box.append(stars_box)
        
        # Count
        count_label = Gtk.Label(label='(1,234 ratings)')
        count_label.add_css_class('caption')
        rating_box.append(count_label)
        
        group.add(rating_box)
        
        # Individual reviews
        reviews = [
            ('User123', 'Great browser! Fast and secure.', 5),
            ('DevGuy', 'Good but uses too much memory.', 4),
            ('WebSurfer', 'Best browser for privacy.', 5),
        ]
        
        for user, text, rating in reviews:
            review_row = Adw.ActionRow()
            review_row.set_title(user)
            review_row.set_subtitle(text)
            
            rating_label = Gtk.Label(label=f'{"★" * rating}{"☆" * (5 - rating)}')
            review_row.add_suffix(rating_label)
            
            group.add(review_row)
        
        page.add(group)
