import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class AboutPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('About')
        self.set_icon_name('dialog-information-symbolic')
        
        self._build_system_info()
        self._build_specifications()
        self._build_ultron_info()
    
    def _build_system_info(self):
        group = Adw.PreferencesGroup()
        
        # Logo
        logo_row = Adw.ActionRow()
        
        logo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        logo_box.set_margin_top(24)
        logo_box.set_margin_bottom(24)
        
        logo = Gtk.Image.new_from_icon_name('org.ultron.settings')
        logo.set_pixel_size(128)
        logo_box.append(logo)
        
        name_label = Gtk.Label(label='Ultron OS')
        name_label.add_css_class('title-1')
        logo_box.append(name_label)
        
        version_label = Gtk.Label(label='Version 1.0.0')
        version_label.add_css_class('caption')
        logo_box.append(version_label)
        
        logo_row.set_child(logo_box)
        group.add(logo_row)
        
        self.add(group)
    
    def _build_specifications(self):
        group = Adw.PreferencesGroup()
        group.set_title('Specifications')
        
        specs = [
            ('Device Name', 'ultron-pc'),
            ('Processor', 'AMD Ryzen 7 5800X × 16'),
            ('Memory', '32.0 GiB'),
            ('Graphics', 'AMD Radeon RX 6800 XT'),
            ('Disk Capacity', '512.1 GB'),
            ('OS Type', '64-bit'),
            ('GNOME Version', '46'),
            ('Windowing System', 'Wayland'),
            ('Kernel Version', '6.8.0-ultron'),
        ]
        
        for name, value in specs:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(value)
            group.add(row)
        
        # Copy button
        copy_row = Adw.ActionRow()
        copy_row.set_title('Copy Specifications')
        copy_row.set_subtitle('Copy system info to clipboard')
        
        copy_button = Gtk.Button()
        copy_button.set_label('Copy')
        copy_row.add_suffix(copy_button)
        copy_row.set_activatable_widget(copy_button)
        copy_button.connect('clicked', self._on_copy_specs)
        group.add(copy_row)
        
        self.add(group)
    
    def _build_ultron_info(self):
        group = Adw.PreferencesGroup()
        group.set_title('Ultron OS')
        
        # Website
        website_row = Adw.ActionRow()
        website_row.set_title('Website')
        website_row.set_subtitle('https://ultron.org')
        website_row.set_activatable(True)
        group.add(website_row)
        
        # Support
        support_row = Adw.ActionRow()
        support_row.set_title('Support')
        support_row.set_subtitle('https://ultron.org/support')
        support_row.set_activatable(True)
        group.add(support_row)
        
        # Documentation
        docs_row = Adw.ActionRow()
        docs_row.set_title('Documentation')
        docs_row.set_subtitle('https://ultron.org/docs')
        docs_row.set_activatable(True)
        group.add(docs_row)
        
        # Report bug
        bug_row = Adw.ActionRow()
        bug_row.set_title('Report a Bug')
        bug_row.set_subtitle('https://ultron.org/bugs')
        bug_row.set_activatable(True)
        group.add(bug_row)
        
        # Credits
        credits_row = Adw.ActionRow()
        credits_row.set_title('Credits')
        credits_row.set_subtitle('View contributors and acknowledgments')
        credits_row.set_activatable(True)
        group.add(credits_row)
        
        # Legal
        legal_row = Adw.ActionRow()
        legal_row.set_title('Legal')
        legal_row.set_subtitle('License and legal information')
        legal_row.set_activatable(True)
        group.add(legal_row)
        
        self.add(group)
    
    def _on_copy_specs(self, button):
        specs = """Ultron OS 1.0.0
Device: ultron-pc
Processor: AMD Ryzen 7 5800X × 16
Memory: 32.0 GiB
Graphics: AMD Radeon RX 6800 XT
Disk: 512.1 GB
OS Type: 64-bit
GNOME: 46
Windowing: Wayland
Kernel: 6.8.0-ultron"""
        
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        clipboard.set_text(specs, -1)
