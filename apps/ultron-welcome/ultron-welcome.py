#!/usr/bin/env python3
"""
Ultron OS - Welcome Wizard
First-time user setup and system tour application
"""

import gi
import sys
import os
import json

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class WelcomeWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("Welcome to Ultron OS")
        self.set_default_size(800, 600)
        self.set_resizable(False)
        
        # Create main layout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)
        
        # Header bar
        self.header = Adw.HeaderBar()
        self.header.set_show_title(False)
        self.main_box.append(self.header)
        
        # Stack for pages
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_box.append(self.stack)
        
        # Add pages
        self.add_welcome_page()
        self.add_features_page()
        self.add_theme_page()
        self.add_accounts_page()
        self.add_finish_page()
        
        # Navigation buttons
        self.nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.nav_box.set_margin_top(12)
        self.nav_box.set_margin_bottom(12)
        self.nav_box.set_margin_start(24)
        self.nav_box.set_margin_end(24)
        
        self.back_button = Gtk.Button(label="Back")
        self.back_button.connect("clicked", self.on_back_clicked)
        self.back_button.set_sensitive(False)
        self.nav_box.append(self.back_button)
        
        self.next_button = Gtk.Button(label="Next")
        self.next_button.connect("clicked", self.on_next_clicked)
        self.next_button.add_css_class("suggested-action")
        self.nav_box.append(self.next_button)
        
        self.main_box.append(self.nav_box)
        
        # Track current page
        self.current_page = 0
        self.total_pages = 5
    
    def add_welcome_page(self):
        """Welcome page with introduction"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        page.set_margin_top(40)
        page.set_margin_bottom(40)
        page.set_margin_start(40)
        page.set_margin_end(40)
        
        # Logo
        logo = Gtk.Image.new_from_file("/usr/share/ultron/artwork/logo.svg")
        logo.set_pixel_size(120)
        page.append(logo)
        
        # Title
        title = Gtk.Label(label="Welcome to Ultron OS")
        title.add_css_class("title-1")
        page.append(title)
        
        # Description
        desc = Gtk.Label(label="A modern Linux distribution designed for polish, performance, and beginner-friendliness.")
        desc.add_css_class("body")
        desc.set_wrap(True)
        page.append(desc)
        
        self.stack.add_named(page, "welcome")
    
    def add_features_page(self):
        """Features overview page"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        page.set_margin_top(40)
        page.set_margin_bottom(40)
        page.set_margin_start(40)
        page.set_margin_end(40)
        
        title = Gtk.Label(label="Key Features")
        title.add_css_class("title-2")
        page.append(title)
        
        features = [
            ("Modern Design", "Clean aesthetics with rounded corners and smooth animations"),
            ("GTK4 + Libadwaita", "Native look and feel with the latest GTK toolkit"),
            ("Wayland First", "Enhanced security and performance with Wayland display server"),
            ("Flatpak Support", "Access thousands of applications through Flathub")
        ]
        
        for icon_name, desc in features:
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
            row.set_margin_start(12)
            row.set_margin_end(12)
            
            icon = Gtk.Image.new_from_icon_name("emblem-default")
            icon.set_pixel_size(32)
            row.append(icon)
            
            text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            
            name_label = Gtk.Label(label=icon_name)
            name_label.add_css_class("heading")
            name_label.set_halign(Gtk.Align.START)
            text_box.append(name_label)
            
            desc_label = Gtk.Label(label=desc)
            desc_label.add_css_class("caption")
            desc_label.set_halign(Gtk.Align.START)
            desc_label.set_wrap(True)
            text_box.append(desc_label)
            
            row.append(text_box)
            page.append(row)
        
        self.stack.add_named(page, "features")
    
    def add_theme_page(self):
        """Theme selection page"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        page.set_margin_top(40)
        page.set_margin_bottom(40)
        page.set_margin_start(40)
        page.set_margin_end(40)
        
        title = Gtk.Label(label="Choose Your Theme")
        title.add_css_class("title-2")
        page.append(title)
        
        desc = Gtk.Label(label="Select your preferred appearance")
        desc.add_css_class("body")
        page.append(desc)
        
        # Theme options
        themes_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=24)
        themes_box.set_halign(Gtk.Align.CENTER)
        
        # Dark theme
        dark_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        dark_preview = Gtk.Box()
        dark_preview.set_size_request(200, 150)
        dark_preview.add_css_class("card")
        dark_preview.set_css_classes(["card"])
        dark_preview.set_css_properties([("background-color", "#1C1C1E")])
        dark_box.append(dark_preview)
        
        dark_label = Gtk.Label(label="Dark")
        dark_box.append(dark_label)
        
        dark_radio = Gtk.ToggleButton()
        dark_radio.set_active(True)
        dark_radio.connect("toggled", self.on_theme_changed, "dark")
        dark_box.append(dark_radio)
        
        themes_box.append(dark_box)
        
        # Light theme
        light_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        light_preview = Gtk.Box()
        light_preview.set_size_request(200, 150)
        light_preview.set_css_classes(["card"])
        light_preview.set_css_properties([("background-color", "#F5F5F7")])
        light_box.append(light_preview)
        
        light_label = Gtk.Label(label="Light")
        light_box.append(light_label)
        
        light_radio = Gtk.ToggleButton(group=dark_radio)
        light_radio.connect("toggled", self.on_theme_changed, "light")
        light_box.append(light_radio)
        
        themes_box.append(light_box)
        
        page.append(themes_box)
        
        self.stack.add_named(page, "theme")
    
    def add_accounts_page(self):
        """Online accounts setup page"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        page.set_margin_top(40)
        page.set_margin_bottom(40)
        page.set_margin_start(40)
        page.set_margin_end(40)
        
        title = Gtk.Label(label="Connect Your Accounts")
        title.add_css_class("title-2")
        page.append(title)
        
        desc = Gtk.Label(label="Optionally connect your online accounts for a personalized experience")
        desc.add_css_class("body")
        desc.set_wrap(True)
        page.append(desc)
        
        # Account options
        accounts = ["Google", "Microsoft", "Nextcloud", "GitHub"]
        
        for account in accounts:
            row = Adw.ActionRow()
            row.set_title(account)
            row.set_subtitle("Connect for sync and integration")
            
            switch = Gtk.Switch()
            row.add_suffix(switch)
            row.set_activatable_widget(switch)
            
            page.append(row)
        
        self.stack.add_named(page, "accounts")
    
    def add_finish_page(self):
        """Completion page"""
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        page.set_margin_top(40)
        page.set_margin_bottom(40)
        page.set_margin_start(40)
        page.set_margin_end(40)
        page.set_halign(Gtk.Align.CENTER)
        page.set_valign(Gtk.Align.CENTER)
        
        # Checkmark icon
        icon = Gtk.Image.new_from_icon_name("object-select-symbolic")
        icon.set_pixel_size(120)
        icon.add_css_class("success")
        page.append(icon)
        
        title = Gtk.Label(label="You're All Set!")
        title.add_css_class("title-1")
        page.append(title)
        
        desc = Gtk.Label(label="Enjoy your new Ultron OS experience")
        desc.add_css_class("body")
        page.append(desc)
        
        self.stack.add_named(page, "finish")
    
    def on_theme_changed(self, button, theme):
        """Handle theme selection"""
        if button.get_active():
            # Apply theme immediately
            settings = Gtk.Settings.get_default()
            if theme == "dark":
                settings.set_property("gtk-application-prefer-dark-theme", True)
            else:
                settings.set_property("gtk-application-prefer-dark-theme", False)
    
    def on_back_clicked(self, button):
        """Navigate to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_navigation()
    
    def on_next_clicked(self, button):
        """Navigate to next page or finish"""
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.update_navigation()
        else:
            self.finish_wizard()
    
    def update_navigation(self):
        """Update stack and button states"""
        pages = ["welcome", "features", "theme", "accounts", "finish"]
        self.stack.set_visible_child_name(pages[self.current_page])
        
        self.back_button.set_sensitive(self.current_page > 0)
        
        if self.current_page == self.total_pages - 1:
            self.next_button.set_label("Finish")
        else:
            self.next_button.set_label("Next")
    
    def finish_wizard(self):
        """Complete wizard and mark as done"""
        # Mark wizard as completed
        config_dir = os.path.expanduser("~/.config/ultron")
        os.makedirs(config_dir, exist_ok=True)
        
        config_file = os.path.join(config_dir, "welcome-completed")
        with open(config_file, 'w') as f:
            f.write("completed")
        
        self.close()


class WelcomeApplication(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
    
    def on_activate(self, app):
        # Check if wizard was already completed
        config_file = os.path.expanduser("~/.config/ultron/welcome-completed")
        if os.path.exists(config_file):
            print("Welcome wizard already completed")
            return
        
        win = WelcomeWindow(application=app)
        win.present()


def main(version):
    app = WelcomeApplication(application_id="org.ultron.welcome")
    return app.run(sys.argv)


if __name__ == "__main__":
    main("1.0.0")
