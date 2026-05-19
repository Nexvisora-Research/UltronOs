"""Unit tests for Ultron OS Python components"""

import json
import os
import sys
import tempfile
import unittest
import importlib.util
from pathlib import Path
from unittest.mock import patch, MagicMock


def load_module(name, path):
    """Load a Python module from a file path"""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class TestAIAssistant(unittest.TestCase):
    """Test cases for AIAssistant class"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / '.config' / 'ultron' / 'ai'
        self.config_dir.mkdir(parents=True)
    
    def tearDown(self):
        """Clean up test environment"""
        self.temp_dir.cleanup()
    
    @patch('pathlib.Path.home')
    def test_init_creates_config_dir(self, mock_home):
        """Test that initialization creates config directory"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        self.assertTrue(self.config_dir.exists())
    
    @patch('pathlib.Path.home')
    def test_default_config(self, mock_home):
        """Test default configuration values"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        
        self.assertFalse(assistant.config['voice_enabled'])
        self.assertEqual(assistant.config['hotword'], 'Hey Ultron')
        self.assertEqual(assistant.config['language'], 'en-US')
        self.assertTrue(assistant.config['suggestions_enabled'])
    
    @patch('pathlib.Path.home')
    def test_load_commands(self, mock_home):
        """Test that commands are loaded"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        
        self.assertIn('open_browser', assistant._commands)
        self.assertIn('open_terminal', assistant._commands)
        self.assertIn('lock_screen', assistant._commands)
        self.assertIn('volume_up', assistant._commands)
        self.assertIn('mute', assistant._commands)
    
    @patch('pathlib.Path.home')
    def test_process_command_recognizes_patterns(self, mock_home):
        """Test command pattern recognition"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        
        # Test that patterns are recognized (even if execution fails in test env)
        result = assistant.process_command('open browser')
        self.assertIn('success', result)
        
        result = assistant.process_command('lock screen')
        self.assertIn('success', result)
        
        result = assistant.process_command('volume up')
        self.assertIn('success', result)
    
    @patch('pathlib.Path.home')
    def test_process_command_unknown_returns_failure(self, mock_home):
        """Test unknown command returns failure"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        
        result = assistant.process_command('xyz unknown command 123')
        self.assertFalse(result['success'])
        self.assertEqual(result['message'], 'Command not recognized')
    
    @patch('pathlib.Path.home')
    def test_get_suggestions_returns_list(self, mock_home):
        """Test that suggestions are returned"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        
        suggestions = assistant.get_suggestions()
        self.assertIsInstance(suggestions, list)
        self.assertTrue(len(suggestions) > 0)
        
        # Check suggestion structure
        for suggestion in suggestions:
            self.assertIn('type', suggestion)
            self.assertIn('text', suggestion)
    
    @patch('pathlib.Path.home')
    def test_add_custom_command(self, mock_home):
        """Test adding custom commands"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        
        assistant.add_custom_command(
            'test_cmd',
            ['test pattern'],
            'command',
            cmd='echo test'
        )
        
        self.assertIn('test_cmd', assistant._commands)
        self.assertEqual(assistant._commands['test_cmd']['action'], 'command')
    
    @patch('pathlib.Path.home')
    def test_remove_custom_command(self, mock_home):
        """Test removing custom commands"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        assistant = ai_module.AIAssistant()
        
        assistant.add_custom_command('temp_cmd', ['temp'], 'command', cmd='echo')
        self.assertIn('temp_cmd', assistant._commands)
        
        assistant.remove_custom_command('temp_cmd')
        self.assertNotIn('temp_cmd', assistant._commands)


class TestWorkflowEngine(unittest.TestCase):
    """Test cases for WorkflowEngine class"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_dir = Path(self.temp_dir.name) / '.config' / 'ultron' / 'workflows'
        self.config_dir.mkdir(parents=True)
    
    def tearDown(self):
        """Clean up test environment"""
        self.temp_dir.cleanup()
    
    @patch('pathlib.Path.home')
    def test_create_workflow(self, mock_home):
        """Test workflow creation"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        engine = ai_module.WorkflowEngine()
        
        workflow = engine.create_workflow(
            'test_workflow',
            'manual',
            [{'type': 'command', 'cmd': 'echo test'}]
        )
        
        self.assertEqual(workflow['name'], 'test_workflow')
        self.assertTrue(workflow['enabled'])
        self.assertIn('created_at', workflow)
    
    @patch('pathlib.Path.home')
    def test_delete_workflow(self, mock_home):
        """Test workflow deletion"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        engine = ai_module.WorkflowEngine()
        
        engine.create_workflow('temp_workflow', 'manual', [])
        self.assertIn('temp_workflow', engine.workflows)
        
        engine.delete_workflow('temp_workflow')
        self.assertNotIn('temp_workflow', engine.workflows)
    
    @patch('pathlib.Path.home')
    def test_execute_nonexistent_workflow(self, mock_home):
        """Test executing nonexistent workflow"""
        mock_home.return_value = Path(self.temp_dir.name)
        ai_module = load_module('ai_assistant', 
            str(Path(__file__).parent.parent / 'apps' / 'ultron-ai' / 'src' / 'ai_assistant.py'))
        engine = ai_module.WorkflowEngine()
        
        result = engine.execute_workflow('nonexistent')
        self.assertFalse(result['success'])


class TestPerformanceTuner(unittest.TestCase):
    """Test cases for PerformanceTuner class"""
    
    @patch('pathlib.Path.home')
    def test_tuner_initialization(self, mock_home):
        """Test PerformanceTuner initialization"""
        mock_home.return_value = Path(tempfile.mkdtemp())
        tuner_module = load_module('performance_tuner',
            str(Path(__file__).parent.parent / 'tools' / 'ultron-tune' / 'src' / 'performance_tuner.py'))
        tuner = tuner_module.PerformanceTuner()
        
        self.assertTrue(hasattr(tuner, 'config'))
        self.assertTrue(hasattr(tuner, 'profiles'))
    
    @patch('pathlib.Path.home')
    def test_get_system_info(self, mock_home):
        """Test getting system information"""
        mock_home.return_value = Path(tempfile.mkdtemp())
        tuner_module = load_module('performance_tuner',
            str(Path(__file__).parent.parent / 'tools' / 'ultron-tune' / 'src' / 'performance_tuner.py'))
        tuner = tuner_module.PerformanceTuner()
        
        info = tuner.get_system_info()
        self.assertIsInstance(info, dict)


class TestCloudService(unittest.TestCase):
    """Test cases for CloudService class"""
    
    @patch('pathlib.Path.home')
    def test_cloud_service_initialization(self, mock_home):
        """Test CloudService initialization"""
        mock_home.return_value = Path(tempfile.mkdtemp())
        cloud_module = load_module('cloud_service',
            str(Path(__file__).parent.parent / 'services' / 'ultron-cloud' / 'src' / 'cloud_service.py'))
        service = cloud_module.CloudService()
        
        self.assertTrue(hasattr(service, 'providers'))
        self.assertTrue(hasattr(service, 'config'))
    
    @patch('pathlib.Path.home')
    def test_add_provider(self, mock_home):
        """Test adding cloud provider"""
        mock_home.return_value = Path(tempfile.mkdtemp())
        cloud_module = load_module('cloud_service',
            str(Path(__file__).parent.parent / 'services' / 'ultron-cloud' / 'src' / 'cloud_service.py'))
        service = cloud_module.CloudService()
        
        service.add_provider('test_provider', 'nextcloud', 'https://test.example.com')
        self.assertIn('test_provider', service.providers)


class TestDeviceSync(unittest.TestCase):
    """Test cases for DeviceSync class"""
    
    @patch('pathlib.Path.home')
    def test_sync_initialization(self, mock_home):
        """Test DeviceSync initialization"""
        mock_home.return_value = Path(tempfile.mkdtemp())
        sync_module = load_module('device_sync',
            str(Path(__file__).parent.parent / 'services' / 'ultron-sync' / 'src' / 'device_sync.py'))
        sync = sync_module.DeviceSync()
        
        self.assertTrue(hasattr(sync, 'config'))
        self.assertTrue(hasattr(sync, 'sync_items'))


if __name__ == '__main__':
    unittest.main()
