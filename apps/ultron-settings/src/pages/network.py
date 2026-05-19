import gi
import os

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib


class NetworkPage(Adw.PreferencesPage):
    def __init__(self):
        super().__init__()
        self.set_title('Network')
        self.set_icon_name('network-wireless-symbolic')
        
        self._nm_client = None
        
        self._build_wifi()
        self._build_ethernet()
        self._build_proxy()
        self._build_network_tools()
    
    def _build_wifi(self):
        group = Adw.PreferencesGroup()
        group.set_title('Wi-Fi')
        group.set_description('Connect to wireless networks')
        
        # Wi-Fi toggle
        wifi_row = Adw.SwitchRow()
        wifi_row.set_title('Wi-Fi')
        wifi_row.set_subtitle('Enable wireless networking')
        wifi_row.set_active(True)
        wifi_row.connect('notify::active', self._on_wifi_toggled)
        group.add(wifi_row)
        
        # Available networks
        networks = [
            ('Home Network', 'Connected', 'network-wireless-signal-excellent-symbolic'),
            ('Office WiFi', 'Saved', 'network-wireless-signal-good-symbolic'),
            ('Coffee Shop', '', 'network-wireless-signal-ok-symbolic'),
            ('Neighbor', '', 'network-wireless-signal-weak-symbolic'),
        ]
        
        for name, status, icon in networks:
            row = Adw.ActionRow()
            row.set_title(name)
            row.set_subtitle(status)
            row.set_icon_name(icon)
            row.set_activatable(True)
            
            if status == 'Connected':
                check = Gtk.Image.new_from_icon_name('object-select-symbolic')
                check.set_css_classes(['success'])
                row.add_suffix(check)
            
            row.connect('activated', self._on_network_clicked, name)
            group.add(row)
        
        self.add(group)
    
    def _build_ethernet(self):
        group = Adw.PreferencesGroup()
        group.set_title('Wired')
        group.set_description('Ethernet connection settings')
        
        # Ethernet status
        eth_row = Adw.ActionRow()
        eth_row.set_title('Ethernet')
        eth_row.set_subtitle('Connected - 1 Gbps')
        eth_row.set_icon_name('network-wired-symbolic')
        
        eth_check = Gtk.Image.new_from_icon_name('object-select-symbolic')
        eth_check.set_css_classes(['success'])
        eth_row.add_suffix(eth_check)
        group.add(eth_row)
        
        # MAC address
        mac_row = Adw.ActionRow()
        mac_row.set_title('MAC Address')
        mac_row.set_subtitle('00:1A:2B:3C:4D:5E')
        group.add(mac_row)
        
        self.add(group)
    
    def _build_proxy(self):
        group = Adw.PreferencesGroup()
        group.set_title('Proxy')
        group.set_description('Network proxy configuration')
        
        # Proxy mode
        proxy_row = Adw.ComboRow()
        proxy_row.set_title('Proxy Mode')
        
        proxy_model = Gtk.StringList()
        proxy_model.append('None')
        proxy_model.append('Manual')
        proxy_model.append('Automatic')
        proxy_row.set_model(proxy_model)
        group.add(proxy_row)
        
        self.add(group)
    
    def _build_network_tools(self):
        group = Adw.PreferencesGroup()
        group.set_title('Network Tools')
        
        # IP address
        ip_row = Adw.ActionRow()
        ip_row.set_title('IP Address')
        ip_row.set_subtitle('192.168.1.100')
        group.add(ip_row)
        
        # DNS
        dns_row = Adw.ActionRow()
        dns_row.set_title('DNS')
        dns_row.set_subtitle('8.8.8.8, 8.8.4.4')
        group.add(dns_row)
        
        # Network info button
        info_row = Adw.ActionRow()
        info_row.set_title('Network Information')
        info_row.set_subtitle('View detailed network settings')
        
        info_button = Gtk.Button()
        info_button.set_icon_name('go-next-symbolic')
        info_row.add_suffix(info_button)
        info_row.set_activatable_widget(info_button)
        group.add(info_row)
        
        self.add(group)
    
    def _on_wifi_toggled(self, row, param):
        active = row.get_active()
        # Toggle Wi-Fi via NetworkManager
        pass
    
    def _on_network_clicked(self, row, network_name):
        # Show network connection dialog
        pass
