import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class DisplayPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Display')
        self.set_icon_name('display-symbolic')
        
        self._build_monitors()
        self._build_resolution()
        self._build_night_light()
        self._build_scaling()
    
    def _build_monitors(self):
        group = Adw.PreferencesGroup()
        group.set_title('Display')
        
        # Monitor arrangement preview
        preview_row = Adw.ActionRow()
        preview_row.set_title('Display Arrangement')
        preview_row.set_subtitle('Drag to rearrange displays')
        group.add(preview_row)
        
        # Primary display
        primary_row = Adw.ComboRow()
        primary_row.set_title('Primary Display')
        
        primary_model = Gtk.StringList()
        primary_model.append('Built-in Display')
        primary_model.append('External Monitor')
        primary_row.set_model(primary_model)
        group.add(primary_row)
        
        self.add(group)
    
    def _build_resolution(self):
        group = Adw.PreferencesGroup()
        group.set_title('Resolution & Refresh Rate')
        
        # Resolution
        res_row = Adw.ComboRow()
        res_row.set_title('Resolution')
        
        res_model = Gtk.StringList()
        res_model.append('1920 x 1080 (16:9)')
        res_model.append('2560 x 1440 (16:9)')
        res_model.append('3840 x 2160 (16:9)')
        res_row.set_model(res_model)
        res_row.set_selected(0)
        group.add(res_row)
        
        # Refresh rate
        refresh_row = Adw.ComboRow()
        refresh_row.set_title('Refresh Rate')
        
        refresh_model = Gtk.StringList()
        refresh_model.append('60 Hz')
        refresh_model.append('75 Hz')
        refresh_model.append('120 Hz')
        refresh_model.append('144 Hz')
        refresh_row.set_model(refresh_model)
        refresh_row.set_selected(0)
        group.add(refresh_row)
        
        # Auto refresh rate
        auto_refresh_row = Adw.SwitchRow()
        auto_refresh_row.set_title('Auto Refresh Rate')
        auto_refresh_row.set_subtitle('Dynamically adjust refresh rate for power saving')
        group.add(auto_refresh_row)
        
        self.add(group)
    
    def _build_night_light(self):
        group = Adw.PreferencesGroup()
        group.set_title('Night Light')
        group.set_description('Reduce blue light for better sleep')
        
        # Night light toggle
        night_row = Adw.SwitchRow()
        night_row.set_title('Night Light')
        night_row.set_subtitle('Warm the display colors')
        group.add(night_row)
        
        # Schedule
        schedule_row = Adw.ComboRow()
        schedule_row.set_title('Schedule')
        
        schedule_model = Gtk.StringList()
        schedule_model.append('Sunset to Sunrise')
        schedule_model.append('Custom Schedule')
        schedule_row.set_model(schedule_model)
        group.add(schedule_row)
        
        # Temperature
        temp_row = Adw.ActionRow()
        temp_row.set_title('Temperature')
        
        temp_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        temp_scale.set_range(2000, 6500)
        temp_scale.set_value(3500)
        temp_scale.set_digits(0)
        temp_scale.set_hexpand(True)
        temp_scale.add_mark(2700, Gtk.PositionType.BOTTOM, 'Warm')
        temp_scale.add_mark(6500, Gtk.PositionType.BOTTOM, 'Cool')
        temp_row.add_suffix(temp_scale)
        temp_row.set_activatable_widget(temp_scale)
        group.add(temp_row)
        
        self.add(group)
    
    def _build_scaling(self):
        group = Adw.PreferencesGroup()
        group.set_title('Scaling')
        
        # Scale factor
        scale_row = Adw.ComboRow()
        scale_row.set_title('Scale')
        
        scale_model = Gtk.StringList()
        scale_model.append('100%')
        scale_model.append('125%')
        scale_model.append('150%')
        scale_model.append('200%')
        scale_row.set_model(scale_model)
        scale_row.set_selected(0)
        group.add(scale_row)
        
        # Fractional scaling
        fractional_row = Adw.SwitchRow()
        fractional_row.set_title('Fractional Scaling')
        fractional_row.set_subtitle('Allow non-integer scaling factors')
        group.add(fractional_row)
        
        self.add(group)
