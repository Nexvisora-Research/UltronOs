"""
Ultron OS - Security Hardening Framework
Sandboxing, permission management, and firewall integration
"""

import os
import subprocess
import json
from pathlib import Path
from datetime import datetime


class SecurityHardener:
    """Main security hardening engine"""
    
    def __init__(self):
        self.config_dir = Path('/etc/ultron/security')
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'security.json'
        self.config = self._load_config()
    
    def _load_config(self):
        """Load security configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'firewall_enabled': True,
            'apparmor_enabled': True,
            'sandbox_level': 'standard',
            'auto_updates': True,
            'sudo_timeout': 5,
            'max_login_attempts': 5,
        }
    
    def save_config(self):
        """Save security configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def audit_system(self):
        """Perform security audit"""
        return {
            'firewall_status': self._check_firewall(),
            'apparmor_status': self._check_apparmor(),
            'open_ports': self._get_open_ports(),
            'user_accounts': self._get_user_accounts(),
            'sudo_config': self._check_sudo_config(),
            'file_permissions': self._check_file_permissions(),
            'kernel_params': self._check_kernel_params(),
        }
    
    def _check_firewall(self):
        """Check firewall status"""
        try:
            result = subprocess.run(
                ['ufw', 'status'],
                capture_output=True, text=True
            )
            return {
                'enabled': 'active' in result.stdout.lower(),
                'rules': result.stdout,
            }
        except Exception:
            return {'enabled': False, 'rules': 'UFW not installed'}
    
    def _check_apparmor(self):
        """Check AppArmor status"""
        try:
            result = subprocess.run(
                ['systemctl', 'is-active', 'apparmor'],
                capture_output=True, text=True
            )
            return {
                'enabled': result.stdout.strip() == 'active',
            }
        except Exception:
            return {'enabled': False}
    
    def _get_open_ports(self):
        """Get list of open ports"""
        try:
            result = subprocess.run(
                ['ss', '-tlnp'],
                capture_output=True, text=True
            )
            ports = []
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 5:
                        ports.append({
                            'port': parts[4],
                            'process': parts[5] if len(parts) > 5 else 'unknown',
                        })
            return ports
        except Exception:
            return []
    
    def _get_user_accounts(self):
        """Get user account information"""
        users = []
        
        with open('/etc/passwd', 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) >= 7:
                    uid = int(parts[2])
                    if uid >= 1000:  # Regular users
                        users.append({
                            'username': parts[0],
                            'uid': uid,
                            'home': parts[5],
                            'shell': parts[6],
                        })
        
        return users
    
    def _check_sudo_config(self):
        """Check sudo configuration"""
        config = {
            'timeout': 15,
            'max_attempts': 3,
        }
        
        sudoers_file = Path('/etc/sudoers')
        if sudoers_file.exists():
            content = sudoers_file.read_text()
            if 'timestamp_timeout' in content:
                for line in content.split('\n'):
                    if 'timestamp_timeout' in line:
                        try:
                            config['timeout'] = int(line.split('=')[1].strip())
                        except Exception:
                            pass
        
        return config
    
    def _check_file_permissions(self):
        """Check critical file permissions"""
        checks = []
        
        critical_files = [
            ('/etc/passwd', '644'),
            ('/etc/shadow', '640'),
            ('/etc/sudoers', '440'),
            ('/etc/ssh/sshd_config', '600'),
        ]
        
        for file_path, expected_perms in critical_files:
            path = Path(file_path)
            if path.exists():
                stat = path.stat()
                actual_perms = oct(stat.st_mode)[-3:]
                checks.append({
                    'file': file_path,
                    'expected': expected_perms,
                    'actual': actual_perms,
                    'secure': actual_perms == expected_perms,
                })
        
        return checks
    
    def _check_kernel_params(self):
        """Check kernel security parameters"""
        params = {}
        
        security_params = [
            'kernel.randomize_va_space',
            'kernel.exec-shield',
            'kernel.dmesg_restrict',
            'kernel.kptr_restrict',
            'net.ipv4.conf.all.accept_redirects',
            'net.ipv4.conf.all.send_redirects',
            'net.ipv4.icmp_echo_ignore_broadcasts',
        ]
        
        for param in security_params:
            param_file = Path(f'/proc/sys/{param.replace(".", "/")}')
            if param_file.exists():
                params[param] = param_file.read_text().strip()
        
        return params
    
    def harden_firewall(self):
        """Configure and harden firewall"""
        results = []
        
        # Install UFW if not present
        try:
            subprocess.run(['apt', 'install', '-y', 'ufw'], capture_output=True)
            results.append('Installed UFW')
        except Exception as e:
            results.append(f'Failed to install UFW: {str(e)}')
        
        # Set default policies
        try:
            subprocess.run(['ufw', 'default', 'deny', 'incoming'], capture_output=True)
            subprocess.run(['ufw', 'default', 'allow', 'outgoing'], capture_output=True)
            results.append('Set default firewall policies')
        except Exception as e:
            results.append(f'Failed to set policies: {str(e)}')
        
        # Allow essential services
        essential_services = [
            ('22/tcp', 'SSH'),
            ('80/tcp', 'HTTP'),
            ('443/tcp', 'HTTPS'),
            ('53/udp', 'DNS'),
        ]
        
        for port, name in essential_services:
            try:
                subprocess.run(['ufw', 'allow', port], capture_output=True)
                results.append(f'Allowed {name} ({port})')
            except Exception:
                pass
        
        # Enable firewall
        try:
            subprocess.run(['ufw', '--force', 'enable'], capture_output=True)
            results.append('Enabled firewall')
        except Exception as e:
            results.append(f'Failed to enable firewall: {str(e)}')
        
        return results
    
    def harden_apparmor(self):
        """Configure AppArmor profiles"""
        results = []
        
        # Install AppArmor utilities
        try:
            subprocess.run(['apt', 'install', '-y', 'apparmor-utils'], capture_output=True)
            results.append('Installed AppArmor utilities')
        except Exception as e:
            results.append(f'Failed to install AppArmor utils: {str(e)}')
        
        # Create Ultron-specific profiles
        ultron_profiles_dir = Path('/etc/apparmor.d/ultron')
        ultron_profiles_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate profile for Ultron apps
        apps = [
            'ultron-settings',
            'ultron-store',
            'ultron-control-center',
        ]
        
        for app in apps:
            profile_path = ultron_profiles_dir / app
            if not profile_path.exists():
                profile_content = f"""#include <tunables/global>

/usr/bin/{app} {{
  #include <abstractions/base>
  #include <abstractions/nameservice>

  network inet stream,
  network inet6 stream,

  /usr/share/ultron/** r,
  /home/*/.config/ultron/** rw,
  /home/*/.local/share/ultron/** rw,
  /tmp/ rw,
  /tmp/** rw,
}}
"""
                profile_path.write_text(profile_content)
                results.append(f'Created AppArmor profile for {app}')
        
        # Enable AppArmor
        try:
            subprocess.run(['systemctl', 'enable', 'apparmor'], capture_output=True)
            subprocess.run(['systemctl', 'start', 'apparmor'], capture_output=True)
            results.append('Enabled AppArmor service')
        except Exception as e:
            results.append(f'Failed to enable AppArmor: {str(e)}')
        
        return results
    
    def configure_sandbox(self):
        """Configure application sandboxing"""
        results = []
        
        # Configure Flatpak sandbox permissions
        try:
            subprocess.run(
                ['flatpak', 'override', '--user', '--nosocket=x11', '--socket=wayland'],
                capture_output=True
            )
            results.append('Configured Flatpak sandbox defaults')
        except Exception as e:
            results.append(f'Failed to configure Flatpak: {str(e)}')
        
        # Configure Firejail if available
        try:
            subprocess.run(['apt', 'install', '-y', 'firejail'], capture_output=True)
            results.append('Installed Firejail sandbox')
        except Exception:
            pass
        
        return results
    
    def harden_kernel(self):
        """Apply kernel security parameters"""
        results = []
        
        sysctl_config = Path('/etc/sysctl.d/99-ultron-security.conf')
        
        config_content = """# Ultron OS Security Hardening

# Enable ASLR
kernel.randomize_va_space = 2

# Restrict kernel pointer exposure
kernel.kptr_restrict = 2

# Restrict dmesg access
kernel.dmesg_restrict = 1

# Disable IP source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0

# Disable ICMP redirect acceptance
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0

# Disable ICMP redirect sending
net.ipv4.conf.all.send_redirects = 0

# Enable SYN flood protection
net.ipv4.tcp_syncookies = 1

# Ignore ICMP broadcast requests
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Log suspicious packets
net.ipv4.conf.all.log_martians = 1
"""
        
        try:
            sysctl_config.write_text(config_content)
            subprocess.run(['sysctl', '-p', str(sysctl_config)], capture_output=True)
            results.append('Applied kernel security parameters')
        except Exception as e:
            results.append(f'Failed to apply kernel params: {str(e)}')
        
        return results
    
    def apply_all_hardening(self):
        """Apply all security hardening measures"""
        results = {
            'firewall': self.harden_firewall(),
            'apparmor': self.harden_apparmor(),
            'sandbox': self.configure_sandbox(),
            'kernel': self.harden_kernel(),
        }
        
        # Save timestamp
        self.config['last_hardened'] = datetime.now().isoformat()
        self.save_config()
        
        return results
