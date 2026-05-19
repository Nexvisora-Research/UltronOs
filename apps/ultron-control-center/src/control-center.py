#!/usr/bin/env python3
"""
Ultron OS - Control Center
Quick settings panel for system controls
"""

import gi
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class ControlCenterWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_title('Control Center')
        self.set_default_size(380, 600)
        self.set_resizable(False)
        self.set_decorated(False)
        
        self._settings = Gio.Settings.new('org.gnome.desktop.interface')
        self._network_settings = Gio.Settings.new('org.gnome.settings-daemon.plugins.power')
        
        self._build_ui()
    
    def _build_ui(self):
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # Header
        header = Adw.HeaderBar()
        header.set_show_title(False)
        header.set_show_end_title_buttons(False)
        main_box.append(header)
        
        # Scrollable content
        scroll = Gtk.ScrolledWindow()
        scroll.set_vexpand(True)
        main_box.append(scroll)
        
        content = Adw.PreferencesPage()
        scroll.set_child(content)
        
        # Quick toggles
        self._build_quick_toggles(content)
        
        # Sliders
        self._build_sliders(content)
        
        # Media controls
        self._build_media_controls(content)
        
        # Output device
        self._build_output_device(content)
        
        # Footer buttons
        self._build_footer(main_box)
    
    def _build_quick_toggles(self, page):
        group = Adw.PreferencesGroup()
        
        # Grid for toggles
        grid = Gtk.Grid()
        grid.set_column_spacing(12)
        grid.set_row_spacing(12)
        grid.set_margin_top(12)
        grid.set_margin_bottom(12)
        
        toggles = [
            ('Wi-Fi', 'network-wireless-signal-excellent-symbolic', True, 0, 0),
            ('Bluetooth', 'bluetooth-active-symbolic', True, 1, 0),
            ('Airplane', 'airplane-mode-symbolic', False, 2, 0),
            ('Night Light', 'night-light-symbolic', False, 0, 1),
            ('DND', 'notifications-disabled-symbolic', False, 1, 1),
            ('Dark Mode', 'display-brightness-symbolic', True, 2, 1),
        ]
        
        for label, icon, active, col, row in toggles:
            toggle_box = self._create_toggle(label, icon, active)
            grid.attach(toggle_box, col, row, 1, 1)
        
        group.add(grid)
        page.add(group)
    
    def _create_toggle(self, label, icon_name, active):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_hexpand(True)
        
        # Button
        button = Gtk.ToggleButton()
        button.set_active(active)
        button.set_size_request(80, 80)
        
        if active:
            button.add_css_class('suggested-action')
        
        button.connect('toggled', self._on_toggle_toggled, label)
        
        # Icon
        icon = Gtk.Image.new_from_icon_name(icon_name)
        icon.set_pixel_size(24)
        button.set_child(icon)
        
        box.append(button)
        
        # Label
        label_widget = Gtk.Label(label=label)
        label_widget.add_css_class('caption')
        box.append(label_widget)
        
        return box
    
    def _on_toggle_toggled(self, button, label):
        if button.get_active():
            button.add_css_class('suggested-action')
        else:
            button.remove_css_class('suggested-action')
        
        # Handle toggle actions
        if label == 'Dark Mode':
            if button.get_active():
                self._settings.set_string('color-scheme', 'prefer-dark')
            else:
                self._settings.set_string('color-scheme', 'default')
    
    def _build_sliders(self, page):
        group = Adw.PreferencesGroup()
        
        # Brightness
        brightness_row = Adw.ActionRow()
        brightness_row.set_title('Brightness')
        brightness_row.set_icon_name('display-brightness-symbolic')
        
        brightness_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        brightness_scale.set_range(0, 100)
        brightness_scale.set_value(75)
        brightness_scale.set_digits(0)
        brightness_scale.set_hexpand(True)
        brightness_scale.add_mark(50, Gtk.PositionType.BOTTOM, None)
        brightness_scale.add_mark(100, Gtk.PositionType.BOTTOM, None)
        brightness_row.add_suffix(brightness_scale)
        brightness_row.set_activatable_widget(brightness_scale)
        group.add(brightness_row)
        
        # Volume
        volume_row = Adw.ActionRow()
        volume_row.set_title('Volume')
        volume_row.set_icon_name('audio-volume-high-symbolic')
        
        volume_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        volume_scale.set_range(0, 100)
        volume_scale.set_value(65)
        volume_scale.set_digits(0)
        volume_scale.set_hexpand(True)
        volume_scale.add_mark(50, Gtk.PositionType.BOTTOM, None)
        volume_scale.add_mark(100, Gtk.PositionType.BOTTOM, None)
        volume_row.add_suffix(volume_scale)
        volume_row.set_activatable_widget(volume_scale)
        group.add(volume_row)
        
        page.add(group)
    
    def _build_media_controls(self, page):
        group = Adw.PreferencesGroup()
        group.set_title('Now Playing')
        
        # Player info
        player_row = Adw.ActionRow()
        player_row.set_title('No media playing')
        player_row.set_subtitle('Play something to see controls')
        player_row.set_icon_name('audio-x-generic-symbolic')
        group.add(player_row)
        
        # Transport controls
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        controls_box.set_halign(Gtk.Align.CENTER)
        controls_box.set_margin_top(8)
        controls_box.set_margin_bottom(8)
        
        prev_button = Gtk.Button.new_from_icon_name('media-skip-backward-symbolic')
        prev_button.set_has_frame(False)
        controls_box.append(prev_button)
        
        play_button = Gtk.Button.new_from_icon_name('media-playback-start-symbolic')
        play_button.set_has_frame(False)
        play_button.add_css_class('circular')
        play_button.add_css_class('suggested-action')
        controls_box.append(play_button)
        
        next_button = Gtk.Button.new_from_icon_name('media-skip-forward-symbolic')
        next_button.set_has_frame(False)
        controls_box.append(next_button)
        
        group.add(controls_box)
        page.add(group)
    
    def _build_output_device(self, page):
        group = Adw.PreferencesGroup()
        group.set_title('Output')
        
        device_row = Adw.ComboRow()
        device_row.set_title('Output Device')
        
        model = Gtk.StringList()
        model.append('Built-in Speakers')
        model.append('Headphones')
        model.append('Bluetooth Device')
        device_row.set_model(model)
        group.add(device_row)
        
        page.add(group)
    
    def _build_footer(self, main_box):
        footer_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        footer_box.set_margin_top(8)
        footer_box.set_margin_bottom(12)
        footer_box.set_margin_start(12)
        footer_box.set_margin_end(12)
        
        # Settings button
        settings_button = Gtk.Button(label='Settings')
        settings_button.set_hexpand(True)
        settings_button.connect('clicked', self._on_settings_clicked)
        footer_box.append(settings_button)
        
        # Lock button
        lock_button = Gtk.Button.new_from_icon_name('system-lock-symbolic')
        lock_button.set_has_frame(False)
        lock_button.connect('clicked', self._on_lock_clicked)
        footer_box.append(lock_button)
        
        # Power button
        power_button = Gtk.Button.new_from_icon_name('system-shutdown-symbolic')
        power_button.set_has_frame(False)
        power_button.add_css_class('destructive-action')
        power_button.connect('clicked', self._on_power_clicked)
        footer_box.append(power_button)
        
        main_box.append(footer_box)
    
    def _on_settings_clicked(self, button):
        # Open settings app
        subprocess.Popen(['ultron-settings'])
    
    def _on_lock_clicked(self, button):
        # Lock screen
        subprocess.Popen(['loginctl', 'lock-session'])
    
    def _on_power_clicked(self, button):
        # Show power menu
        pass


class ControlCenterApplication(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        win = ControlCenterWindow(application=app)
        win.present()


def main(version):
    app = ControlCenterApplication(application_id='org.ultron.control-center')
    return app.run(sys.argv)


if __name__ == '__main__':
    main('1.0.0')
