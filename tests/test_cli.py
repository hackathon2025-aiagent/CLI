import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from cleo.application import Application
from cleo.testers.command_tester import CommandTester

from agent_task.cli import ImportCommand
from agent_task.task_manager import TaskManager

def test_import_command_success(tmp_path):
    """Test successful task import."""
    # Mock TaskManager.load_task
    with patch.object(TaskManager, 'load_task') as mock_load:
        # Create application and command
        app = Application()
        command = ImportCommand()
        app.add(command)
        
        # Create command tester
        tester = CommandTester(command)
        
        # Execute command
        tester.execute("mytask")
        
        # Verify
        assert tester.status_code == 0
        mock_load.assert_called_once_with('mytask')

def test_import_command_nonexistent_task(tmp_path):
    """Test importing a non-existent task."""
    # Mock TaskManager.load_task to raise error
    with patch.object(TaskManager, 'load_task') as mock_load:
        mock_load.side_effect = ValueError("Task 'nonexistent' not found")
        
        # Create application and command
        app = Application()
        command = ImportCommand()
        app.add(command)
        
        # Create command tester
        tester = CommandTester(command)
        
        # Execute command
        tester.execute("nonexistent")
        
        # Verify
        assert tester.status_code == 1
        mock_load.assert_called_once_with('nonexistent')

def test_import_command_invalid_target(tmp_path):
    """Test importing to an invalid target directory."""
    # Mock TaskManager.load_task to raise error for invalid target
    with patch.object(TaskManager, 'load_task') as mock_load:
        mock_load.side_effect = OSError("Permission denied")
        
        # Create application and command
        app = Application()
        command = ImportCommand()
        app.add(command)
        
        # Create command tester
        tester = CommandTester(command)
        
        # Execute command
        tester.execute("test-task")
        
        # Verify
        assert tester.status_code == 1
        mock_load.assert_called_once_with('test-task') 