import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class SystemPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('System')
        self.set_icon_name('system-run-symbolic')
        
        self._build_storage()
        self._build_power()
        self._build_date_time()
        self._build_language()
        self._build_updates()
    
    def _build_storage(self):
        group = Adw.PreferencesGroup()
        group.set_title('Storage')
        
        # Storage usage
        storage_row = Adw.ActionRow()
        storage_row.set_title('Storage Usage')
        storage_row.set_subtitle('128 GB used of 512 GB')
        
        # Progress bar
        progress = Gtk.ProgressBar()
        progress.set_fraction(0.25)
        progress.set_hexpand(True)
        storage_row.add_suffix(progress)
        group.add(storage_row)
        
        # Temporary files
        temp_row = Adw.ActionRow()
        temp_row.set_title('Temporary Files')
        temp_row.set_subtitle('2.3 GB')
        
        clear_button = Gtk.Button()
        clear_button.set_label('Clear')
        clear_button.add_css_class('destructive-action')
        temp_row.add_suffix(clear_button)
        temp_row.set_activatable_widget(clear_button)
        group.add(temp_row)
        
        # Trash
        trash_row = Adw.ActionRow()
        trash_row.set_title('Trash')
        trash_row.set_subtitle('450 MB')
        
        empty_button = Gtk.Button()
        empty_button.set_label('Empty')
        empty_button.add_css_class('destructive-action')
        trash_row.add_suffix(empty_button)
        trash_row.set_activatable_widget(empty_button)
        group.add(trash_row)
        
        self.add(group)
    
    def _build_power(self):
        group = Adw.PreferencesGroup()
        group.set_title('Power')
        
        # Battery status
        battery_row = Adw.ActionRow()
        battery_row.set_title('Battery')
        battery_row.set_subtitle('85% - 4 hours remaining')
        battery_row.set_icon_name('battery-good-symbolic')
        group.add(battery_row)
        
        # Power mode
        power_row = Adw.ComboRow()
        power_row.set_title('Power Mode')
        
        power_model = Gtk.StringList()
        power_model.append('Performance')
        power_model.append('Balanced')
        power_model.append('Power Saver')
        power_row.set_model(power_model)
        power_row.set_selected(1)
        group.add(power_row)
        
        # Screen blank
        blank_row = Adw.ComboRow()
        blank_row.set_title('Screen Blank')
        
        blank_model = Gtk.StringList()
        blank_model.append('1 minute')
        blank_model.append('2 minutes')
        blank_model.append('5 minutes')
        blank_model.append('10 minutes')
        blank_model.append('Never')
        blank_row.set_model(blank_model)
        blank_row.set_selected(2)
        group.add(blank_row)
        
        # Automatic suspend
        suspend_row = Adw.ComboRow()
        suspend_row.set_title('Automatic Suspend')
        
        suspend_model = Gtk.StringList()
        suspend_model.append('5 minutes')
        suspend_model.append('10 minutes')
        suspend_model.append('15 minutes')
        suspend_model.append('30 minutes')
        suspend_model.append('Never')
        suspend_row.set_model(suspend_model)
        suspend_row.set_selected(1)
        group.add(suspend_row)
        
        # Lid close action
        lid_row = Adw.ComboRow()
        lid_row.set_title('Lid Close Action')
        
        lid_model = Gtk.StringList()
        lid_model.append('Suspend')
        lid_model.append('Do Nothing')
        lid_model.append('Shut Down')
        lid_row.set_model(lid_model)
        lid_row.set_selected(0)
        group.add(lid_row)
        
        self.add(group)
    
    def _build_date_time(self):
        group = Adw.PreferencesGroup()
        group.set_title('Date & Time')
        
        # Automatic date/time
        auto_dt_row = Adw.SwitchRow()
        auto_dt_row.set_title('Automatic Date & Time')
        auto_dt_row.set_subtitle('Set time automatically via network')
        auto_dt_row.set_active(True)
        group.add(auto_dt_row)
        
        # Timezone
        tz_row = Adw.ActionRow()
        tz_row.set_title('Time Zone')
        tz_row.set_subtitle('UTC')
        
        tz_button = Gtk.Button()
        tz_button.set_icon_name('go-next-symbolic')
        tz_button.set_has_frame(False)
        tz_row.add_suffix(tz_button)
        tz_row.set_activatable_widget(tz_button)
        group.add(tz_row)
        
        # 24-hour time
        time_format_row = Adw.SwitchRow()
        time_format_row.set_title('24-Hour Time')
        time_format_row.set_subtitle('Use 24-hour clock format')
        time_format_row.set_active(True)
        group.add(time_format_row)
        
        self.add(group)
    
    def _build_language(self):
        group = Adw.PreferencesGroup()
        group.set_title('Language & Region')
        
        # Language
        lang_row = Adw.ActionRow()
        lang_row.set_title('Language')
        lang_row.set_subtitle('English (United States)')
        
        lang_button = Gtk.Button()
        lang_button.set_icon_name('go-next-symbolic')
        lang_button.set_has_frame(False)
        lang_row.add_suffix(lang_button)
        lang_row.set_activatable_widget(lang_button)
        group.add(lang_row)
        
        # Region
        region_row = Adw.ActionRow()
        region_row.set_title('Region')
        region_row.set_subtitle('United States')
        region_row.set_activatable(True)
        group.add(region_row)
        
        self.add(group)
    
    def _build_updates(self):
        group = Adw.PreferencesGroup()
        group.set_title('Software Updates')
        
        # Check for updates
        update_row = Adw.ActionRow()
        update_row.set_title('Check for Updates')
        update_row.set_subtitle('System is up to date')
        
        check_button = Gtk.Button()
        check_button.set_label('Check')
        update_row.add_suffix(check_button)
        update_row.set_activatable_widget(check_button)
        group.add(update_row)
        
        # Automatic updates
        auto_update_row = Adw.SwitchRow()
        auto_update_row.set_title('Automatic Updates')
        auto_update_row.set_subtitle('Download and install updates automatically')
        auto_update_row.set_active(True)
        group.add(auto_update_row)
        
        # Update history
        history_row = Adw.ActionRow()
        history_row.set_title('Update History')
        history_row.set_subtitle('View past updates')
        history_row.set_activatable(True)
        group.add(history_row)
        
        self.add(group)
