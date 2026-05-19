import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class SoundPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Sound')
        self.set_icon_name('audio-speakers-symbolic')
        
        self._build_output()
        self._build_input()
        self._build_alerts()
        self._build_advanced()
    
    def _build_output(self):
        group = Adw.PreferencesGroup()
        group.set_title('Output')
        
        # Volume
        volume_row = Adw.ActionRow()
        volume_row.set_title('System Volume')
        
        volume_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        volume_scale.set_range(0, 100)
        volume_scale.set_value(75)
        volume_scale.set_digits(0)
        volume_scale.set_hexpand(True)
        volume_scale.add_mark(50, Gtk.PositionType.BOTTOM, None)
        volume_scale.add_mark(100, Gtk.PositionType.BOTTOM, None)
        volume_row.add_suffix(volume_scale)
        volume_row.set_activatable_widget(volume_scale)
        group.add(volume_row)
        
        # Output device
        output_row = Adw.ComboRow()
        output_row.set_title('Output Device')
        
        output_model = Gtk.StringList()
        output_model.append('Built-in Speakers')
        output_model.append('AirPods Pro')
        output_model.append('HDMI Monitor')
        output_row.set_model(output_model)
        group.add(output_row)
        
        # Balance
        balance_row = Adw.ActionRow()
        balance_row.set_title('Balance')
        
        balance_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        balance_scale.set_range(-1, 1)
        balance_scale.set_value(0)
        balance_scale.set_digits(2)
        balance_scale.set_hexpand(True)
        balance_row.add_suffix(balance_scale)
        balance_row.set_activatable_widget(balance_scale)
        group.add(balance_row)
        
        self.add(group)
    
    def _build_input(self):
        group = Adw.PreferencesGroup()
        group.set_title('Input')
        
        # Input volume
        input_volume_row = Adw.ActionRow()
        input_volume_row.set_title('Input Volume')
        
        input_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        input_scale.set_range(0, 100)
        input_scale.set_value(50)
        input_scale.set_digits(0)
        input_scale.set_hexpand(True)
        input_volume_row.add_suffix(input_scale)
        input_volume_row.set_activatable_widget(input_scale)
        group.add(input_volume_row)
        
        # Input device
        input_row = Adw.ComboRow()
        input_row.set_title('Input Device')
        
        input_model = Gtk.StringList()
        input_model.append('Built-in Microphone')
        input_model.append('USB Microphone')
        input_row.set_model(input_model)
        group.add(input_row)
        
        self.add(group)
    
    def _build_alerts(self):
        group = Adw.PreferencesGroup()
        group.set_title('Alerts')
        
        # Alert volume
        alert_row = Adw.ActionRow()
        alert_row.set_title('Alert Volume')
        
        alert_scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL)
        alert_scale.set_range(0, 100)
        alert_scale.set_value(50)
        alert_scale.set_digits(0)
        alert_scale.set_hexpand(True)
        alert_row.add_suffix(alert_scale)
        alert_row.set_activatable_widget(alert_scale)
        group.add(alert_row)
        
        # Sound effects
        effects_row = Adw.SwitchRow()
        effects_row.set_title('Sound Effects')
        effects_row.set_subtitle('Play sounds for system events')
        effects_row.set_active(True)
        group.add(effects_row)
        
        self.add(group)
    
    def _build_advanced(self):
        group = Adw.PreferencesGroup()
        group.set_title('Advanced')
        
        # Audio profile
        profile_row = Adw.ComboRow()
        profile_row.set_title('Audio Profile')
        
        profile_model = Gtk.StringList()
        profile_model.append('Analog Stereo Output')
        profile_model.append('Analog Stereo Duplex')
        profile_model.append('Digital Stereo Output')
        profile_model.append('Off')
        profile_row.set_model(profile_model)
        group.add(profile_row)
        
        self.add(group)
