import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class AccountsPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Accounts')
        self.set_icon_name('system-users-symbolic')
        
        self._build_user_account()
        self._build_online_accounts()
        self._build_login_options()
    
    def _build_user_account(self):
        group = Adw.PreferencesGroup()
        group.set_title('User Account')
        
        # User profile
        profile_row = Adw.ActionRow()
        profile_row.set_title('Current User')
        profile_row.set_subtitle('Administrator')
        
        # Avatar
        avatar = Gtk.Image.new_from_icon_name('avatar-default-symbolic')
        avatar.set_pixel_size(48)
        profile_row.add_prefix(avatar)
        
        # Edit button
        edit_button = Gtk.Button()
        edit_button.set_label('Edit')
        profile_row.add_suffix(edit_button)
        profile_row.set_activatable_widget(edit_button)
        group.add(profile_row)
        
        # Username
        username_row = Adw.ActionRow()
        username_row.set_title('Username')
        username_row.set_subtitle('ultron-user')
        group.add(username_row)
        
        # Account type
        type_row = Adw.ComboRow()
        type_row.set_title('Account Type')
        
        type_model = Gtk.StringList()
        type_model.append('Administrator')
        type_model.append('Standard')
        type_row.set_model(type_model)
        type_row.set_selected(0)
        group.add(type_row)
        
        # Change password
        password_row = Adw.ActionRow()
        password_row.set_title('Password')
        password_row.set_subtitle('Change your login password')
        
        password_button = Gtk.Button()
        password_button.set_label('Change...')
        password_row.add_suffix(password_button)
        password_row.set_activatable_widget(password_button)
        group.add(password_row)
        
        # Auto login
        auto_login_row = Adw.SwitchRow()
        auto_login_row.set_title('Automatic Login')
        auto_login_row.set_subtitle('Log in automatically on startup')
        group.add(auto_login_row)
        
        self.add(group)
    
    def _build_online_accounts(self):
        group = Adw.PreferencesGroup()
        group.set_title('Online Accounts')
        group.set_description('Connect your cloud and social accounts')
        
        accounts = [
            ('Google', 'user@gmail.com', 'google-symbolic', True),
            ('Microsoft', 'user@outlook.com', 'microsoft-symbolic', True),
            ('Nextcloud', 'cloud.ultron.org', 'network-server-symbolic', False),
            ('GitHub', 'github.com', 'git-symbolic', True),
        ]
        
        for name, detail, icon, connected in accounts:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(detail)
            row.set_icon_name(icon)
            row.set_activatable(True)
            
            if connected:
                check = Gtk.Image.new_from_icon_name('object-select-symbolic')
                check.set_css_classes(['success'])
                row.add_suffix(check)
            
            group.add(row)
        
        # Add account button
        add_row = Adw.ActionRow()
        add_row.set_title('Add Account')
        add_row.set_subtitle('Connect a new online account')
        add_row.set_icon_name('list-add-symbolic')
        add_row.set_activatable(True)
        group.add(add_row)
        
        self.add(group)
    
    def _build_login_options(self):
        group = Adw.PreferencesGroup()
        group.set_title('Login Options')
        
        # Fingerprint
        fingerprint_row = Adw.ActionRow()
        fingerprint_row.set_title('Fingerprint Login')
        fingerprint_row.set_subtitle('Not set up')
        
        setup_button = Gtk.Button()
        setup_button.set_label('Set Up')
        fingerprint_row.add_suffix(setup_button)
        fingerprint_row.set_activatable_widget(setup_button)
        group.add(fingerprint_row)
        
        # Face recognition
        face_row = Adw.ActionRow()
        face_row.set_title('Face Recognition')
        face_row.set_subtitle('Not available')
        face_row.set_sensitive(False)
        group.add(face_row)
        
        # PIN
        pin_row = Adw.ActionRow()
        pin_row.set_title('PIN Login')
        pin_row.set_subtitle('Use a PIN instead of password')
        
        pin_button = Gtk.Button()
        pin_button.set_label('Set Up')
        pin_row.add_suffix(pin_button)
        pin_row.set_activatable_widget(pin_button)
        group.add(pin_row)
        
        self.add(group)
