"""
Ultron OS - Voice Assistant Integration
Speech recognition, text-to-speech, and voice commands
"""

import os
import json
import subprocess
import threading
import queue
from pathlib import Path
from datetime import datetime


class VoiceAssistant:
    """Main voice assistant engine"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.config' / 'ultron' / 'voice'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / 'voice.json'
        self.config = self._load_config()
        
        self._listening = False
        self._command_queue = queue.Queue()
        self._handlers = {}
    
    def _load_config(self):
        """Load voice configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            'hotword': 'Hey Ultron',
            'language': 'en-US',
            'voice': 'default',
            'hotword_enabled': True,
            'feedback_sound': True,
            'continuous_listening': False,
        }
    
    def save_config(self):
        """Save voice configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def register_handler(self, command_pattern, handler):
        """Register a command handler"""
        self._handlers[command_pattern] = handler
    
    def start_listening(self):
        """Start voice recognition"""
        if self._listening:
            return
        
        self._listening = True
        
        if self.config.get('hotword_enabled'):
            thread = threading.Thread(target=self._hotword_loop)
            thread.daemon = True
            thread.start()
        else:
            thread = threading.Thread(target=self._continuous_listening)
            thread.daemon = True
            thread.start()
    
    def stop_listening(self):
        """Stop voice recognition"""
        self._listening = False
    
    def _hotword_loop(self):
        """Listen for hotword"""
        while self._listening:
            # Simulate hotword detection
            # In production, this would use PocketSphinx or similar
            import time
            time.sleep(1)
            
            # Check if hotword detected (simulated)
            if self._check_hotword():
                self._play_feedback_sound()
                self._listen_for_command()
    
    def _continuous_listening(self):
        """Continuously listen for commands"""
        while self._listening:
            self._listen_for_command()
    
    def _check_hotword(self):
        """Check if hotword was detected"""
        # This would use actual speech recognition
        return False
    
    def _play_feedback_sound(self):
        """Play feedback sound"""
        if self.config.get('feedback_sound'):
            try:
                subprocess.run(
                    ['paplay', '/usr/share/sounds/ultron/feedback.wav'],
                    capture_output=True
                )
            except Exception:
                pass
    
    def _listen_for_command(self):
        """Listen for voice command"""
        # This would use speech_recognition library
        # For now, simulate command recognition
        import time
        time.sleep(2)
        
        # Simulated command
        command = "open browser"
        self._process_command(command)
    
    def _process_command(self, command):
        """Process recognized command"""
        command = command.lower().strip()
        
        # Check registered handlers
        for pattern, handler in self._handlers.items():
            if pattern.lower() in command:
                handler(command)
                return
        
        # Default handlers
        self._handle_default_command(command)
    
    def _handle_default_command(self, command):
        """Handle default commands"""
        commands = {
            'open browser': lambda: subprocess.Popen(['firefox']),
            'open terminal': lambda: subprocess.Popen(['ultron-terminal']),
            'open settings': lambda: subprocess.Popen(['ultron-settings']),
            'take screenshot': lambda: subprocess.Popen(['gnome-screenshot']),
            'lock screen': lambda: subprocess.run(['loginctl', 'lock-session']),
            'volume up': lambda: subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '+5%']),
            'volume down': lambda: subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', '-5%']),
            'mute': lambda: subprocess.run(['pactl', 'set-sink-mute', '@DEFAULT_SINK@', 'toggle']),
            'what time is it': lambda: self._speak(datetime.now().strftime('It is %I:%M %p')),
            'what is the date': lambda: self._speak(datetime.now().strftime('Today is %B %d, %Y')),
        }
        
        for pattern, action in commands.items():
            if pattern in command:
                try:
                    action()
                except Exception as e:
                    self._speak(f"Sorry, I couldn't do that: {str(e)}")
                return
        
        self._speak("I didn't understand that command")
    
    def speak(self, text):
        """Speak text using TTS"""
        self._speak(text)
    
    def _speak(self, text):
        """Internal TTS method"""
        try:
            # Use espeak or festival
            subprocess.run(
                ['espeak', '-v', self.config.get('voice', 'en'), text],
                capture_output=True
            )
        except Exception:
            # Fallback to festival
            try:
                subprocess.run(
                    ['festival', '--tts'],
                    input=text.encode(),
                    capture_output=True
                )
            except Exception:
                pass
    
    def get_available_voices(self):
        """Get list of available TTS voices"""
        voices = []
        
        try:
            result = subprocess.run(
                ['espeak', '--voices'],
                capture_output=True, text=True
            )
            
            for line in result.stdout.split('\n')[1:]:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 4:
                        voices.append({
                            'id': parts[3],
                            'language': parts[1],
                            'name': parts[2],
                        })
        except Exception:
            pass
        
        return voices
    
    def test_microphone(self):
        """Test microphone input"""
        try:
            # Record 2 seconds of audio
            subprocess.run(
                ['arecord', '-d', '2', '-f', 'cd', '/tmp/ultron-mic-test.wav'],
                capture_output=True
            )
            
            # Play it back
            subprocess.run(
                ['aplay', '/tmp/ultron-mic-test.wav'],
                capture_output=True
            )
            
            # Cleanup
            Path('/tmp/ultron-mic-test.wav').unlink()
            
            return {'success': True, 'message': 'Microphone test complete'}
        except Exception as e:
            return {'success': False, 'message': str(e)}


class VoiceCommandBuilder:
    """Builder for custom voice commands"""
    
    def __init__(self):
        self.commands_file = Path.home() / '.config' / 'ultron' / 'voice' / 'custom_commands.json'
        self.commands = self._load_commands()
    
    def _load_commands(self):
        """Load custom commands"""
        if self.commands_file.exists():
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_commands(self):
        """Save custom commands"""
        with open(self.commands_file, 'w') as f:
            json.dump(self.commands, f, indent=2)
    
    def add_command(self, patterns, action, **kwargs):
        """Add a custom voice command"""
        command = {
            'patterns': patterns,
            'action': action,
            **kwargs,
        }
        
        self.commands.append(command)
        self.save_commands()
        
        return command
    
    def remove_command(self, index):
        """Remove a custom command"""
        if 0 <= index < len(self.commands):
            del self.commands[index]
            self.save_commands()
    
    def get_commands(self):
        """Get all custom commands"""
        return self.commands
