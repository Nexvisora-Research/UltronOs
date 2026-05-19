"""
Ultron OS - Smart Workflow Engine
Task automation, context-aware suggestions, and productivity enhancements
"""

import os
import json
import subprocess
import threading
import time
from pathlib import Path
from datetime import datetime, timedelta


class WorkflowEngine:
    """Smart workflow automation engine"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'ultron' / 'workflows'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.workflows_file = self.config_dir / 'workflows.json'
        self.workflows = self._load_workflows()
        
        self._running = False
        self._monitor_thread = None
    
    def _load_workflows(self):
        """Load workflows"""
        if self.workflows_file.exists():
            with open(self.workflows_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_workflows(self):
        """Save workflows"""
        with open(self.workflows_file, 'w') as f:
            json.dump(self.workflows, f, indent=2)
    
    def create_workflow(self, name, trigger, actions, enabled=True):
        """Create a new workflow"""
        workflow = {
            'id': len(self.workflows) + 1,
            'name': name,
            'trigger': trigger,
            'actions': actions,
            'enabled': enabled,
            'created_at': datetime.now().isoformat(),
            'last_triggered': None,
            'trigger_count': 0,
        }
        
        self.workflows.append(workflow)
        self.save_workflows()
        
        return workflow
    
    def delete_workflow(self, workflow_id):
        """Delete a workflow"""
        self.workflows = [w for w in self.workflows if w['id'] != workflow_id]
        self.save_workflows()
    
    def enable_workflow(self, workflow_id):
        """Enable a workflow"""
        for workflow in self.workflows:
            if workflow['id'] == workflow_id:
                workflow['enabled'] = True
                self.save_workflows()
                return True
        return False
    
    def disable_workflow(self, workflow_id):
        """Disable a workflow"""
        for workflow in self.workflows:
            if workflow['id'] == workflow_id:
                workflow['enabled'] = False
                self.save_workflows()
                return True
        return False
    
    def execute_workflow(self, workflow_id):
        """Execute a workflow"""
        workflow = None
        for w in self.workflows:
            if w['id'] == workflow_id:
                workflow = w
                break
        
        if not workflow or not workflow['enabled']:
            return {'success': False, 'message': 'Workflow not found or disabled'}
        
        results = []
        for action in workflow['actions']:
            result = self._execute_action(action)
            results.append(result)
            
            if not result['success']:
                break
        
        # Update workflow stats
        workflow['last_triggered'] = datetime.now().isoformat()
        workflow['trigger_count'] += 1
        self.save_workflows()
        
        return {'success': True, 'results': results}
    
    def _execute_action(self, action):
        """Execute a single action"""
        action_type = action.get('type')
        
        if action_type == 'launch':
            return self._launch_app(action['app'])
        elif action_type == 'command':
            return self._run_command(action['cmd'])
        elif action_type == 'notification':
            return self._show_notification(action.get('title', ''), action.get('message', ''))
        elif action_type == 'wait':
            time.sleep(action.get('seconds', 1))
            return {'success': True}
        elif action_type == 'open_url':
            return self._open_url(action['url'])
        elif action_type == 'type_text':
            return self._type_text(action['text'])
        
        return {'success': False, 'message': 'Unknown action type'}
    
    def _launch_app(self, app_id):
        """Launch an application"""
        try:
            subprocess.Popen([app_id])
            return {'success': True, 'message': f'Launched {app_id}'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _run_command(self, cmd):
        """Run a shell command"""
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return {
                'success': result.returncode == 0,
                'message': result.stdout if result.returncode == 0 else result.stderr,
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _show_notification(self, title, message):
        """Show a desktop notification"""
        try:
            subprocess.run(['notify-send', title, message])
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _open_url(self, url):
        """Open a URL in default browser"""
        try:
            subprocess.run(['xdg-open', url])
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def _type_text(self, text):
        """Type text using xdotool"""
        try:
            subprocess.run(['xdotool', 'type', '--clearmodifiers', text])
            return {'success': True}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def start_monitoring(self):
        """Start monitoring for workflow triggers"""
        if self._running:
            return
        
        self._running = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop)
        self._monitor_thread.daemon = True
        self._monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self._running = False
    
    def _monitor_loop(self):
        """Monitor for workflow triggers"""
        while self._running:
            for workflow in self.workflows:
                if not workflow['enabled']:
                    continue
                
                trigger = workflow['trigger']
                
                if self._check_trigger(trigger):
                    self.execute_workflow(workflow['id'])
            
            time.sleep(10)  # Check every 10 seconds
    
    def _check_trigger(self, trigger):
        """Check if a trigger condition is met"""
        trigger_type = trigger.get('type')
        
        if trigger_type == 'time':
            return self._check_time_trigger(trigger)
        elif trigger_type == 'app_launch':
            return self._check_app_launch_trigger(trigger)
        elif trigger_type == 'location':
            return self._check_location_trigger(trigger)
        elif trigger_type == 'network':
            return self._check_network_trigger(trigger)
        
        return False
    
    def _check_time_trigger(self, trigger):
        """Check time-based trigger"""
        now = datetime.now()
        
        if 'time' in trigger:
            trigger_time = datetime.strptime(trigger['time'], '%H:%M').time()
            if now.time().hour == trigger_time.hour and now.time().minute == trigger_time.minute:
                return True
        
        if 'days' in trigger:
            if now.strftime('%A').lower() in [d.lower() for d in trigger['days']]:
                if 'time' in trigger:
                    return self._check_time_trigger(trigger)
        
        return False
    
    def _check_app_launch_trigger(self, trigger):
        """Check app launch trigger"""
        app_name = trigger.get('app')
        
        # Check if app is running
        try:
            result = subprocess.run(
                ['pgrep', '-f', app_name],
                capture_output=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def _check_location_trigger(self, trigger):
        """Check location-based trigger"""
        # This would use geoclue or similar
        return False
    
    def _check_network_trigger(self, trigger):
        """Check network-based trigger"""
        network_name = trigger.get('network')
        
        try:
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'NAME', 'connection', 'show', '--active'],
                capture_output=True, text=True
            )
            
            active_networks = result.stdout.strip().split('\n')
            return network_name in active_networks
        except Exception:
            return False


class ContextAwareSuggestions:
    """Provides context-aware suggestions"""
    
    def __init__(self):
        self.history_file = Path.home() / '.config' / 'ultron' / 'suggestions' / 'history.json'
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.history = self._load_history()
    
    def _load_history(self):
        """Load usage history"""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {'apps': [], 'times': [], 'locations': []}
    
    def save_history(self):
        """Save usage history"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def record_app_usage(self, app_name):
        """Record app usage"""
        self.history['apps'].append({
            'name': app_name,
            'time': datetime.now().isoformat(),
        })
        
        # Keep only last 100 entries
        self.history['apps'] = self.history['apps'][-100:]
        self.save_history()
    
    def get_suggestions(self):
        """Get context-aware suggestions"""
        suggestions = []
        
        # Time-based suggestions
        hour = datetime.now().hour
        
        if 8 <= hour < 10:
            suggestions.append({
                'type': 'morning',
                'text': 'Good morning! Check your email?',
                'action': 'open_email',
                'confidence': 0.8,
            })
        elif 12 <= hour < 14:
            suggestions.append({
                'type': 'lunch',
                'text': 'Lunch time! Order food?',
                'action': 'open_food_app',
                'confidence': 0.7,
            })
        elif 17 <= hour < 19:
            suggestions.append({
                'type': 'evening',
                'text': 'Wrap up work?',
                'action': 'close_work_apps',
                'confidence': 0.75,
            })
        
        # Usage-based suggestions
        if self.history['apps']:
            last_app = self.history['apps'][-1]['name']
            
            # Suggest related apps
            related_apps = {
                'firefox': ['thunderbird', 'vscode'],
                'vscode': ['terminal', 'git'],
                'libreoffice': ['calculator', 'pdf-viewer'],
            }
            
            if last_app in related_apps:
                for app in related_apps[last_app]:
                    suggestions.append({
                        'type': 'related',
                        'text': f'Open {app}?',
                        'action': f'open_{app}',
                        'confidence': 0.6,
                    })
        
        # Sort by confidence
        suggestions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return suggestions[:5]  # Return top 5
