import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class NotificationsPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Notifications')
        self.set_icon_name('preferences-system-notifications-symbolic')
        
        self._build_general()
        self._build_app_notifications()
        self._build_focus()
    
    def _build_general(self):
        group = Adw.PreferencesGroup()
        group.set_title('General')
        
        # Do Not Disturb
        dnd_row = Adw.SwitchRow()
        dnd_row.set_title('Do Not Disturb')
        dnd_row.set_subtitle('Silence all notifications')
        group.add(dnd_row)
        
        # Show notifications on lock screen
        lock_row = Adw.SwitchRow()
        lock_row.set_title('Show on Lock Screen')
        lock_row.set_subtitle('Display notifications when the screen is locked')
        lock_row.set_active(True)
        group.add(lock_row)
        
        # Notification sound
        sound_row = Adw.SwitchRow()
        sound_row.set_title('Notification Sound')
        sound_row.set_subtitle('Play a sound for new notifications')
        sound_row.set_active(True)
        group.add(sound_row)
        
        # Badge count
        badge_row = Adw.SwitchRow()
        badge_row.set_title('Show Badge Count')
        badge_row.set_subtitle('Display notification count on app icons')
        badge_row.set_active(True)
        group.add(badge_row)
        
        self.add(group)
    
    def _build_app_notifications(self):
        group = Adw.PreferencesGroup()
        group.set_title('Application Notifications')
        
        apps = [
            ('Ultron Store', True, True),
            ('Messages', True, True),
            ('Email', True, False),
            ('Calendar', True, True),
            ('Terminal', False, False),
        ]
        
        for name, enabled, sound in apps:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle('Notifications' if enabled else 'Notifications disabled')
            
            # Enable switch
            enable_switch = Gtk.Switch()
            enable_switch.set_active(enabled)
            row.add_suffix(enable_switch)
            row.set_activatable_widget(enable_switch)
            
            group.add(row)
        
        self.add(group)
    
    def _build_focus(self):
        group = Adw.PreferencesGroup()
        group.set_title('Focus Mode')
        group.set_description('Automatically silence notifications during specific times')
        
        # Focus mode toggle
        focus_row = Adw.SwitchRow()
        focus_row.set_title('Focus Mode')
        focus_row.set_subtitle('Automatically enable Do Not Disturb')
        group.add(focus_row)
        
        # Schedule
        schedule_row = Adw.ActionRow()
        schedule_row.set_title('Schedule')
        schedule_row.set_subtitle('10:00 PM - 7:00 AM')
        
        schedule_button = Gtk.Button()
        schedule_button.set_icon_name('go-next-symbolic')
        schedule_button.set_has_frame(False)
        schedule_row.add_suffix(schedule_button)
        schedule_row.set_activatable_widget(schedule_button)
        group.add(schedule_row)
        
        # Allowed apps
        allowed_row = Adw.ActionRow()
        allowed_row.set_title('Allowed Apps')
        allowed_row.set_subtitle('0 apps can interrupt')
        
        allowed_button = Gtk.Button()
        allowed_button.set_icon_name('go-next-symbolic')
        allowed_button.set_has_frame(False)
        allowed_row.add_suffix(allowed_button)
        allowed_row.set_activatable_widget(allowed_button)
        group.add(allowed_row)
        
        self.add(group)
