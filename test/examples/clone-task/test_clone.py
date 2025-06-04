"""
Test cases for task cloning functionality.
"""
import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from clone import parse_task_url, create_task_directory, write_task_files, run

def test_parse_task_url_valid():
    """Test URL parsing with valid input."""
    user_id, task_name = parse_task_url("user123/task-name")
    assert user_id == "user123"
    assert task_name == "task-name"
    
def test_parse_task_url_invalid():
    """Test URL parsing with invalid input."""
    with pytest.raises(ValueError):
        parse_task_url("invalid-url")
        
def test_create_task_directory(tmp_path):
    """Test task directory creation."""
    task_name = "test-task"
    with patch("pathlib.Path.cwd", return_value=tmp_path):
        task_dir = create_task_directory(task_name)
        assert task_dir.exists()
        assert task_dir.name == task_name
        
def test_write_task_files(tmp_path):
    """Test writing task files."""
    task_dir = tmp_path / "test-task"
    task_dir.mkdir()
    
    task_data = {
        "metadata": {
            "task_name": "test-task",
            "version": "1.0.0",
            "description": "Test task",
            "author_name": "Test User",
            "license": "MIT",
            "tags": "test,example",
            "dependencies": "package1,package2",
            "readme": "# Test Task\n\nDescription"
        },
        "files": {
            "main.py": "print('Hello, World!')",
            "utils/helper.py": "def help(): pass"
        }
    }
    
    write_task_files(task_dir, task_data)
    
    # Check README.md
    assert (task_dir / "README.md").exists()
    assert (task_dir / "README.md").read_text() == task_data["metadata"]["readme"]
    
    # Check taskhub.yaml
    assert (task_dir / "taskhub.yaml").exists()
    
    # Check other files
    assert (task_dir / "main.py").exists()
    assert (task_dir / "utils/helper.py").exists()
    
def test_run_success():
    """Test successful task cloning."""
    mock_task_data = {
        "metadata": {
            "task_name": "test-task",
            "version": "1.0.0",
            "description": "Test task",
            "author_name": "Test User",
            "license": "MIT",
            "tags": "",
            "dependencies": "",
            "readme": "# Test Task"
        },
        "files": {}
    }
    
    with patch("agent_task.api.TaskHubAPI.get_task", return_value=mock_task_data), \
         patch("clone.create_task_directory"), \
         patch("clone.write_task_files"):
        
        result = run({"url": "user123/test-task"})
        assert result["status"] == "success"
        assert "test-task" in result["message"]
        
def test_run_missing_url():
    """Test running without URL parameter."""
    result = run({})
    assert result["status"] == "error"
    assert "URL parameter is required" in result["error"]
    
def test_run_api_error():
    """Test handling API errors."""
    with patch("agent_task.api.TaskHubAPI.get_task", side_effect=Exception("API Error")):
        result = run({"url": "user123/test-task"})
        assert result["status"] == "error"
        assert "API Error" in result["error"] 