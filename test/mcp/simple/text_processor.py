"""
Simple text processing MCP example.
"""
from typing import Any, Dict
from instant_mcp import ServerProtocol

# Define the server
ServerProtocol(
    name="text_processor",
    instructions="A simple text processing server with basic operations",
    tools=[
        "reverse_text",
        "count_words",
        "to_uppercase"
    ]
)

async def reverse_text(text: str) -> Dict[str, Any]:
    """
    Reverse the input text.
    
    Args:
        text: Input text to reverse
        
    Returns:
        Dictionary with original and reversed text
    """
    try:
        return {
            "original": text,
            "reversed": text[::-1],
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to reverse text: {str(e)}",
            "status": "error"
        }

async def count_words(text: str) -> Dict[str, Any]:
    """
    Count words in the input text.
    
    Args:
        text: Input text to analyze
        
    Returns:
        Dictionary with word count statistics
    """
    try:
        words = text.split()
        return {
            "text": text,
            "word_count": len(words),
            "character_count": len(text),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to count words: {str(e)}",
            "status": "error"
        }

async def to_uppercase(text: str) -> Dict[str, Any]:
    """
    Convert text to uppercase.
    
    Args:
        text: Input text to convert
        
    Returns:
        Dictionary with original and uppercase text
    """
    try:
        return {
            "original": text,
            "uppercase": text.upper(),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to convert to uppercase: {str(e)}",
            "status": "error"
        } 