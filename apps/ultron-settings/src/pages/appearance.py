import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class AppearancePage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Appearance')
        self.set_icon_name('brush-symbolic')
        
        self._settings = Gio.Settings.new('org.gnome.desktop.interface')
        self._background_settings = Gio.Settings.new('org.gnome.desktop.background')
        
        self._build_style()
        self._build_theme()
        self._build_fonts()
        self._build_desktop()
    
    def _build_style(self):
        group = Adw.PreferencesGroup()
        group.set_title('Style')
        group.set_description('Choose your preferred appearance')
        
        # Accent color
        accent_row = Adw.ComboRow()
        accent_row.set_title('Accent Color')
        accent_row.set_subtitle('Primary color for the interface')
        
        accent_model = Gtk.StringList()
        colors = [
            ('Purple', '#6C63FF'),
            ('Blue', '#4A90D9'),
            ('Green', '#2ECC71'),
            ('Orange', '#F39C12'),
            ('Red', '#E74C3C'),
            ('Teal', '#00D4AA'),
        ]
        for name, color in colors:
            accent_model.append(name)
        
        accent_row.set_model(accent_model)
        accent_row.connect('notify::selected', self._on_accent_changed)
        group.add(accent_row)
        
        # Window style
        style_row = Adw.ComboRow()
        style_row.set_title('Window Style')
        style_row.set_subtitle('Border radius and effects')
        
        style_model = Gtk.StringList()
        style_model.append('Rounded')
        style_model.append('Sharp')
        style_row.set_model(style_model)
        group.add(style_row)
        
        # Transparency
        transparency_row = Adw.SwitchRow()
        transparency_row.set_title('Transparency Effects')
        transparency_row.set_subtitle('Enable acrylic blur effects')
        transparency_row.set_active(True)
        group.add(transparency_row)
        
        self.add(group)
    
    def _build_theme(self):
        group = Adw.PreferencesGroup()
        group.set_title('Theme')
        group.set_description('Light, dark, or adaptive appearance')
        
        # Theme mode
        theme_row = Adw.ComboRow()
        theme_row.set_title('Theme')
        theme_row.set_subtitle('Choose between light and dark themes')
        
        theme_model = Gtk.StringList()
        theme_model.append('Light')
        theme_model.append('Dark')
        theme_model.append('Auto')
        theme_row.set_model(theme_model)
        
        # Set current theme
        current = self._settings.get_string('color-scheme')
        if 'dark' in current:
            theme_row.set_selected(1)
        elif 'prefer' in current:
            theme_row.set_selected(2)
        else:
            theme_row.set_selected(0)
        
        theme_row.connect('notify::selected', self._on_theme_changed)
        group.add(theme_row)
        
        # Legacy applications
        legacy_row = Adw.ComboRow()
        legacy_row.set_title('Legacy Applications')
        legacy_row.set_subtitle('Theme for GTK3 and older applications')
        
        legacy_model = Gtk.StringList()
        legacy_model.append('Ultron-Dark')
        legacy_model.append('Ultron-Light')
        legacy_model.append('Adwaita')
        legacy_row.set_model(legacy_model)
        group.add(legacy_row)
        
        self.add(group)
    
    def _build_fonts(self):
        group = Adw.PreferencesGroup()
        group.set_title('Fonts')
        group.set_description('Customize font family and size')
        
        # Interface font
        font_row = Adw.ActionRow()
        font_row.set_title('Interface Font')
        
        font_button = Gtk.FontDialogButton()
        font_dialog = Gtk.FontDialog()
        font_button.set_dialog(font_dialog)
        font_button.set_font_desc(
            Pango.FontDescription.from_string(
                self._settings.get_string('font-name')
            )
        )
        font_row.add_suffix(font_button)
        font_row.set_activatable_widget(font_button)
        group.add(font_row)
        
        # Document font
        doc_font_row = Adw.ActionRow()
        doc_font_row.set_title('Document Font')
        
        doc_font_button = Gtk.FontDialogButton()
        doc_font_button.set_dialog(font_dialog)
        doc_font_row.add_suffix(doc_font_button)
        doc_font_row.set_activatable_widget(doc_font_button)
        group.add(doc_font_row)
        
        # Monospace font
        mono_font_row = Adw.ActionRow()
        mono_font_row.set_title('Monospace Font')
        
        mono_font_button = Gtk.FontDialogButton()
        mono_font_button.set_dialog(font_dialog)
        mono_font_row.add_suffix(mono_font_button)
        mono_font_row.set_activatable_widget(mono_font_button)
        group.add(mono_font_row)
        
        # Font size
        size_row = Adw.SpinRow()
        size_row.set_title('Font Size')
        size_row.set_subtitle('Base font size for the interface')
        size_row.set_adjustment(Gtk.Adjustment(
            lower=8, upper=24, step_increment=1, page_increment=2
        ))
        size_row.set_value(11)
        group.add(size_row)
        
        self.add(group)
    
    def _build_desktop(self):
        group = Adw.PreferencesGroup()
        group.set_title('Desktop')
        group.set_description('Wallpaper and desktop appearance')
        
        # Wallpaper
        wallpaper_row = Adw.ActionRow()
        wallpaper_row.set_title('Wallpaper')
        wallpaper_row.set_subtitle('Choose your desktop background')
        
        wallpaper_button = Gtk.Button()
        wallpaper_button.set_label('Change...')
        wallpaper_button.connect('clicked', self._on_wallpaper_clicked)
        wallpaper_row.add_suffix(wallpaper_button)
        wallpaper_row.set_activatable_widget(wallpaper_button)
        group.add(wallpaper_row)
        
        # Dark style wallpaper
        dark_wallpaper_row = Adw.SwitchRow()
        dark_wallpaper_row.set_title('Different Wallpaper for Dark Mode')
        dark_wallpaper_row.set_subtitle('Use separate wallpapers for light and dark themes')
        group.add(dark_wallpaper_row)
        
        # Desktop icons
        icons_row = Adw.SwitchRow()
        icons_row.set_title('Show Desktop Icons')
        icons_row.set_subtitle('Display files and folders on the desktop')
        icons_row.set_active(True)
        group.add(icons_row)
        
        self.add(group)
    
    def _on_accent_changed(self, row, param):
        selected = row.get_selected()
        colors = ['#6C63FF', '#4A90D9', '#2ECC71', '#F39C12', '#E74C3C', '#00D4AA']
        if selected < len(colors):
            # Apply accent color via CSS or GSettings
            pass
    
    def _on_theme_changed(self, row, param):
        selected = row.get_selected()
        if selected == 0:
            self._settings.set_string('color-scheme', 'default')
        elif selected == 1:
            self._settings.set_string('color-scheme', 'prefer-dark')
        else:
            self._settings.set_string('color-scheme', 'prefer-dark')
    
    def _on_wallpaper_clicked(self, button):
        dialog = Gtk.FileDialog()
        dialog.set_title('Choose Wallpaper')
        
        # Add image filter
        filter_ = Gtk.FileFilter()
        filter_.set_name('Images')
        filter_.add_mime_type('image/*')
        dialog.set_filters(Gio.ListStore.new(Gtk.FileFilter))
        dialog.get_filters().append(filter_)
        
        dialog.open(
            self.get_root(),
            None,
            self._on_wallpaper_selected
        )
    
    def _on_wallpaper_selected(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file:
                uri = file.get_uri()
                self._background_settings.set_string('picture-uri', uri)
                self._background_settings.set_string('picture-uri-dark', uri)
        except GLib.Error:
            pass
