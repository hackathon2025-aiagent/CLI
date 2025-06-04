"""
Basic README.md validator for TaskHub tasks.
"""
from pathlib import Path
import re

def validate_readme(task_dir: Path) -> tuple[bool, list[str]]:
    """
    Validate the README.md file in a task directory.
    
    Args:
        task_dir: Path to the task directory
        
    Returns:
        (is_valid, errors) tuple where is_valid is a boolean and errors is a list of error messages
    """
    errors = []
    readme_path = task_dir / "README.md"
    
    # Check if README exists
    if not readme_path.exists():
        errors.append("README.md file is missing")
        return False, errors
        
    # Read README content
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        errors.append(f"Failed to read README.md: {str(e)}")
        return False, errors
        
    # Check minimum length
    if len(content) < 50:
        errors.append("README.md is too short (minimum 50 characters)")
        
    # Check for required sections
    required_sections = [
        "# ",           # Title
        "## ",          # At least one subsection
        "```",          # Code example
        "Usage",        # Usage section
        "Description",  # Description section
    ]
    
    for section in required_sections:
        if section not in content:
            errors.append(f"Missing required section: {section}")
            
    # Check for broken links
    links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
    for text, url in links:
        if not url.startswith(("http", "#", "/")):
            errors.append(f"Invalid link URL: {url}")
            
    return len(errors) == 0, errors 