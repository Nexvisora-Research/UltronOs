import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class BluetoothPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Bluetooth')
        self.set_icon_name('bluetooth-active-symbolic')
        
        self._build_bluetooth()
        self._build_devices()
    
    def _build_bluetooth(self):
        group = Adw.PreferencesGroup()
        group.set_title('Bluetooth')
        
        # Bluetooth toggle
        bt_row = Adw.SwitchRow()
        bt_row.set_title('Bluetooth')
        bt_row.set_subtitle('Enable Bluetooth connectivity')
        bt_row.set_active(True)
        group.add(bt_row)
        
        # Visibility
        visible_row = Adw.SwitchRow()
        visible_row.set_title('Visible to Other Devices')
        visible_row.set_subtitle('Allow other devices to discover this computer')
        group.add(visible_row)
        
        self.add(group)
    
    def _build_devices(self):
        group = Adw.PreferencesGroup()
        group.set_title('Paired Devices')
        
        devices = [
            ('AirPods Pro', 'Connected', 'audio-headphones-symbolic'),
            ('Magic Mouse', 'Connected', 'input-mouse-symbolic'),
            ('Keyboard', 'Paired', 'input-keyboard-symbolic'),
        ]
        
        for name, status, icon in devices:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(status)
            row.set_icon_name(icon)
            row.set_activatable(True)
            
            if status == 'Connected':
                check = Gtk.Image.new_from_icon_name('object-select-symbolic')
                check.set_css_classes(['success'])
                row.add_suffix(check)
            
            # Options button
            options_button = Gtk.Button()
            options_button.set_icon_name('view-more-symbolic')
            options_button.set_has_frame(False)
            row.add_suffix(options_button)
            
            row.connect('activated', self._on_device_clicked, name)
            group.add(row)
        
        # Add device button
        add_row = Adw.ActionRow()
        add_row.set_title('Add Device')
        add_row.set_subtitle('Search for new Bluetooth devices')
        add_row.set_icon_name('list-add-symbolic')
        add_row.set_activatable(True)
        add_row.connect('activated', self._on_add_device)
        group.add(add_row)
        
        self.add(group)
    
    def _on_device_clicked(self, row, device_name):
        pass
    
    def _on_add_device(self, row):
        pass
