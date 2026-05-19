"""
Ultron OS - AI Assistant
Voice commands, smart suggestions, and workflow automation
"""

import os
import json
import subprocess
import threading
from pathlib import Path
from datetime import datetime


class AIAssistant:
    """Main AI assistant service"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'ultron' / 'ai'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'config.json'
        self.config = self._load_config()
        
        self._listening = False
        self._commands = self._load_commands()
    
    def _load_config(self):
        """Load AI configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'voice_enabled': False,
            'hotword': 'Hey Ultron',
            'language': 'en-US',
            'suggestions_enabled': True,
        }
    
    def save_config(self):
        """Save AI configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _load_commands(self):
        """Load custom commands"""
        commands_file = self.config_dir / 'commands.json'
        if commands_file.exists():
            with open(commands_file, 'r') as f:
                return json.load(f)
        
        return {
            'open_browser': {
                'patterns': ['open browser', 'launch firefox', 'start browser'],
                'action': 'launch',
                'app': 'firefox',
            },
            'open_terminal': {
                'patterns': ['open terminal', 'launch terminal', 'start terminal'],
                'action': 'launch',
                'app': 'ultron-terminal',
            },
            'open_settings': {
                'patterns': ['open settings', 'system settings', 'preferences'],
                'action': 'launch',
                'app': 'ultron-settings',
            },
            'take_screenshot': {
                'patterns': ['take screenshot', 'screenshot', 'capture screen'],
                'action': 'command',
                'cmd': 'gnome-screenshot',
            },
            'lock_screen': {
                'patterns': ['lock screen', 'lock computer', 'lock my pc'],
                'action': 'command',
                'cmd': 'loginctl lock-session',
            },
            'volume_up': {
                'patterns': ['volume up', 'increase volume', 'louder'],
                'action': 'command',
                'cmd': 'pactl set-sink-volume @DEFAULT_SINK@ +5%',
            },
            'volume_down': {
                'patterns': ['volume down', 'decrease volume', 'quieter'],
                'action': 'command',
                'cmd': 'pactl set-sink-volume @DEFAULT_SINK@ -5%',
            },
            'mute': {
                'patterns': ['mute', 'mute audio', 'silence'],
                'action': 'command',
                'cmd': 'pactl set-sink-mute @DEFAULT_SINK@ toggle',
            },
            'brightness_up': {
                'patterns': ['brightness up', 'increase brightness', 'brighter'],
                'action': 'command',
                'cmd': 'brightnessctl set +10%',
            },
            'brightness_down': {
                'patterns': ['brightness down', 'decrease brightness', 'dimmer'],
                'action': 'command',
                'cmd': 'brightnessctl set 10%-',
            },
        }
    
    def process_command(self, text):
        """Process a text command"""
        text = text.lower().strip()
        
        for cmd_name, cmd in self._commands.items():
            for pattern in cmd['patterns']:
                if pattern in text:
                    return self._execute_command(cmd)
        
        return {'success': False, 'message': 'Command not recognized'}
    
    def _execute_command(self, cmd):
        """Execute a command"""
        action = cmd.get('action')
        
        if action == 'launch':
            return self._launch_app(cmd['app'])
        elif action == 'command':
            return self._run_shell_command(cmd['cmd'])
        
        return {'success': False, 'message': 'Unknown action'}
    
    def _launch_app(self, app_id):
        """Launch an application"""
        try:
            subprocess.Popen([app_id])
            return {'success': True, 'message': f'Launched {app_id}'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _run_shell_command(self, cmd):
        """Run a shell command"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return {
                'success': result.returncode == 0,
                'message': result.stdout if result.returncode == 0 else result.stderr,
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def start_voice_listening(self):
        """Start voice recognition"""
        if self._listening:
            return
        
        self._listening = True
        thread = threading.Thread(target=self._voice_loop)
        thread.start()
    
    def stop_voice_listening(self):
        """Stop voice recognition"""
        self._listening = False
    
    def _voice_loop(self):
        """Voice recognition loop"""
        # This would use speech_recognition or similar
        # For now, it's a placeholder
        while self._listening:
            import time
            time.sleep(1)
    
    def get_suggestions(self):
        """Get smart suggestions based on usage"""
        suggestions = []
        
        # Time-based suggestions
        hour = datetime.now().hour
        
        if hour < 12:
            suggestions.append({
                'type': 'greeting',
                'text': 'Good morning! Would you like to check your calendar?',
                'action': 'open_calendar',
            })
        elif hour < 18:
            suggestions.append({
                'type': 'greeting',
                'text': 'Good afternoon! Need help with anything?',
                'action': None,
            })
        else:
            suggestions.append({
                'type': 'greeting',
                'text': 'Good evening! Time to wind down?',
                'action': 'enable_night_light',
            })
        
        # Usage-based suggestions
        suggestions.append({
            'type': 'tip',
            'text': 'Try saying "Hey Ultron, open browser" to launch Firefox',
            'action': None,
        })
        
        return suggestions
    
    def add_custom_command(self, name, patterns, action, **kwargs):
        """Add a custom command"""
        self._commands[name] = {
            'patterns': patterns,
            'action': action,
            **kwargs,
        }
        
        commands_file = self.config_dir / 'commands.json'
        with open(commands_file, 'w') as f:
            json.dump(self._commands, f, indent=2)
    
    def remove_custom_command(self, name):
        """Remove a custom command"""
        if name in self._commands:
            del self._commands[name]
            
            commands_file = self.config_dir / 'commands.json'
            with open(commands_file, 'w') as f:
                json.dump(self._commands, f, indent=2)


class WorkflowEngine:
    """Workflow automation engine"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'ultron' / 'workflows'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.workflows = self._load_workflows()
    
    def _load_workflows(self):
        """Load workflows"""
        workflows = {}
        
        for file in self.config_dir.glob('*.json'):
            with open(file, 'r') as f:
                workflow = json.load(f)
                workflows[workflow['name']] = workflow
        
        return workflows
    
    def create_workflow(self, name, trigger, actions):
        """Create a new workflow"""
        workflow = {
            'name': name,
            'trigger': trigger,
            'actions': actions,
            'enabled': True,
            'created_at': datetime.now().isoformat(),
        }
        
        file_path = self.config_dir / f'{name}.json'
        with open(file_path, 'w') as f:
            json.dump(workflow, f, indent=2)
        
        self.workflows[name] = workflow
        return workflow
    
    def delete_workflow(self, name):
        """Delete a workflow"""
        if name in self.workflows:
            file_path = self.config_dir / f'{name}.json'
            if file_path.exists():
                file_path.unlink()
            del self.workflows[name]
    
    def execute_workflow(self, name):
        """Execute a workflow"""
        workflow = self.workflows.get(name)
        if not workflow or not workflow.get('enabled'):
            return {'success': False, 'message': 'Workflow not found or disabled'}
        
        results = []
        for action in workflow['actions']:
            result = self._execute_action(action)
            results.append(result)
            
            if not result['success']:
                break
        
        return {'success': True, 'results': results}
    
    def _execute_action(self, action):
        """Execute a single action"""
        action_type = action.get('type')
        
        if action_type == 'launch':
            return self._launch_app(action['app'])
        elif action_type == 'command':
            return self._run_command(action['cmd'])
        elif action_type == 'wait':
            import time
            time.sleep(action['seconds'])
            return {'success': True}
        elif action_type == 'notification':
            return self._show_notification(action['title'], action['message'])
        
        return {'success': False, 'message': 'Unknown action type'}
    
    def _launch_app(self, app_id):
        """Launch an application"""
        try:
            subprocess.Popen([app_id])
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _run_command(self, cmd):
        """Run a shell command"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return {'success': result.returncode == 0}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _show_notification(self, title, message):
        """Show a desktop notification"""
        try:
            subprocess.run(['notify-send', title, message])
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
