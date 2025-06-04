"""
Simple hello world implementation.
"""
from typing import Dict, Any

def greet(name: str = "World") -> str:
    """
    Generate a greeting message.
    
    Args:
        name: Name to greet (default: "World")
        
    Returns:
        Greeting message string
    """
    if not isinstance(name, str):
        raise TypeError("Name must be a string")
    if not name:
        raise ValueError("Name cannot be empty")
        
    return f"Hello, {name}!"

def run(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Task entry point.
    
    Args:
        params: Optional parameters dictionary
        
    Returns:
        Dictionary with task results
    """
    try:
        # Get name parameter or use default
        params = params or {}
        name = params.get("name", "World")
        
        # Generate greeting
        message = greet(name)
        
        return {
            "message": message,
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        } 