"""
Test cases for hello world task.
"""
import pytest
from hello import greet, run

def test_greet_default():
    """Test default greeting."""
    assert greet() == "Hello, World!"
    
def test_greet_custom_name():
    """Test greeting with custom name."""
    assert greet("Alice") == "Hello, Alice!"
    
def test_greet_invalid_type():
    """Test greeting with invalid name type."""
    with pytest.raises(TypeError):
        greet(123)
        
def test_greet_empty_name():
    """Test greeting with empty name."""
    with pytest.raises(ValueError):
        greet("")
        
def test_run_default():
    """Test run function with default parameters."""
    result = run()
    assert result["status"] == "success"
    assert result["message"] == "Hello, World!"
    
def test_run_custom_params():
    """Test run function with custom parameters."""
    result = run({"name": "Bob"})
    assert result["status"] == "success"
    assert result["message"] == "Hello, Bob!"
    
def test_run_invalid_params():
    """Test run function with invalid parameters."""
    result = run({"name": 123})
    assert result["status"] == "error"
    assert "error" in result 