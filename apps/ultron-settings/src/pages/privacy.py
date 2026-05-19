import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class PrivacyPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Privacy & Security')
        self.set_icon_name('system-lock-symbolic')
        
        self._build_screen_lock()
        self._build_location()
        self._build_diagnostics()
        self._build_app_permissions()
        self._build_firewall()
    
    def _build_screen_lock(self):
        group = Adw.PreferencesGroup()
        group.set_title('Screen Lock')
        
        # Automatic lock
        auto_lock_row = Adw.SwitchRow()
        auto_lock_row.set_title('Automatic Screen Lock')
        auto_lock_row.set_subtitle('Lock screen after inactivity')
        auto_lock_row.set_active(True)
        group.add(auto_lock_row)
        
        # Lock delay
        delay_row = Adw.ComboRow()
        delay_row.set_title('Lock Delay')
        
        delay_model = Gtk.StringList()
        delay_model.append('30 seconds')
        delay_model.append('1 minute')
        delay_model.append('2 minutes')
        delay_model.append('5 minutes')
        delay_model.append('Never')
        delay_row.set_model(delay_model)
        delay_row.set_selected(1)
        group.add(delay_row)
        
        # Lock on suspend
        suspend_row = Adw.SwitchRow()
        suspend_row.set_title('Lock on Suspend')
        suspend_row.set_subtitle('Require password when waking from sleep')
        suspend_row.set_active(True)
        group.add(suspend_row)
        
        self.add(group)
    
    def _build_location(self):
        group = Adw.PreferencesGroup()
        group.set_title('Location Services')
        
        # Location toggle
        location_row = Adw.SwitchRow()
        location_row.set_title('Location Services')
        location_row.set_subtitle('Allow apps to access your location')
        group.add(location_row)
        
        # Location apps
        apps_row = Adw.ActionRow()
        apps_row.set_title('Apps Using Location')
        apps_row.set_subtitle('2 apps')
        
        apps_button = Gtk.Button()
        apps_button.set_icon_name('go-next-symbolic')
        apps_button.set_has_frame(False)
        apps_row.add_suffix(apps_button)
        apps_row.set_activatable_widget(apps_button)
        group.add(apps_row)
        
        self.add(group)
    
    def _build_diagnostics(self):
        group = Adw.PreferencesGroup()
        group.set_title('Diagnostics & Feedback')
        
        # Error reporting
        error_row = Adw.SwitchRow()
        error_row.set_title('Automatic Error Reporting')
        error_row.set_subtitle('Send crash reports to help improve Ultron OS')
        error_row.set_active(True)
        group.add(error_row)
        
        # Usage statistics
        usage_row = Adw.SwitchRow()
        usage_row.set_title('Usage Statistics')
        usage_row.set_subtitle('Share anonymous usage data')
        group.add(usage_row)
        
        # Clear data
        clear_row = Adw.ActionRow()
        clear_row.set_title('Clear Usage Data')
        clear_row.set_subtitle('Remove all collected statistics')
        
        clear_button = Gtk.Button()
        clear_button.set_label('Clear')
        clear_button.add_css_class('destructive-action')
        clear_row.add_suffix(clear_button)
        clear_row.set_activatable_widget(clear_button)
        group.add(clear_row)
        
        self.add(group)
    
    def _build_app_permissions(self):
        group = Adw.PreferencesGroup()
        group.set_title('App Permissions')
        
        permissions = [
            ('Camera', '3 apps'),
            ('Microphone', '2 apps'),
            ('Screen Recording', '1 app'),
            ('Removable Media', '4 apps'),
        ]
        
        for name, count in permissions:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(count)
            row.set_activatable(True)
            row.add_suffix(Gtk.Button.new_from_icon_name('go-next-symbolic'))
            group.add(row)
        
        self.add(group)
    
    def _build_firewall(self):
        group = Adw.PreferencesGroup()
        group.set_title('Firewall')
        
        # Firewall toggle
        firewall_row = Adw.SwitchRow()
        firewall_row.set_title('Firewall')
        firewall_row.set_subtitle('Block unauthorized network connections')
        firewall_row.set_active(True)
        group.add(firewall_row)
        
        # Firewall settings
        fw_settings_row = Adw.ActionRow()
        fw_settings_row.set_title('Firewall Settings')
        fw_settings_row.set_subtitle('Configure rules and exceptions')
        
        fw_button = Gtk.Button()
        fw_button.set_icon_name('go-next-symbolic')
        fw_button.set_has_frame(False)
        fw_settings_row.add_suffix(fw_button)
        fw_settings_row.set_activatable_widget(fw_button)
        group.add(fw_settings_row)
        
        self.add(group)
