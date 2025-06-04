"""
Task cloning implementation.
"""
from pathlib import Path
from typing import Dict, Any, Tuple
import os
import yaml
from agent_task.api import TaskHubAPI

def parse_task_url(url: str) -> Tuple[str, str]:
    """
    Parse user ID and task name from URL.
    
    Args:
        url: Task URL or path (e.g., "user123/task-name")
        
    Returns:
        Tuple of (user_id, task_name)
        
    Raises:
        ValueError: If URL format is invalid
    """
    parts = url.strip("/").split("/")
    if len(parts) != 2:
        raise ValueError("Invalid task URL. Expected format: user-id/task-name")
        
    return parts[0], parts[1]

def create_task_directory(task_name: str) -> Path:
    """
    Create and return task directory.
    
    Args:
        task_name: Name of the task
        
    Returns:
        Path to created directory
    """
    task_dir = Path.cwd() / task_name
    task_dir.mkdir(parents=True, exist_ok=True)
    return task_dir

def write_task_files(task_dir: Path, task_data: Dict[str, Any]) -> None:
    """
    Write task files to directory.
    
    Args:
        task_dir: Target directory path
        task_data: Task data from API
    """
    metadata = task_data["metadata"]
    
    # Write README.md
    readme_path = task_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(metadata["readme"])
        
    # Write taskhub.yaml
    taskhub_config = {
        "name": metadata["task_name"],
        "version": metadata["version"],
        "description": metadata["description"],
        "author": metadata["author_name"],
        "license": metadata["license"],
        "tags": metadata["tags"].split(",") if metadata["tags"] else [],
        "dependencies": metadata["dependencies"].split(",") if metadata["dependencies"] else []
    }
    
    taskhub_path = task_dir / "taskhub.yaml"
    with open(taskhub_path, "w", encoding="utf-8") as f:
        yaml.dump(taskhub_config, f, sort_keys=False)
        
    # Write other files
    if "files" in task_data:
        for file_path, content in task_data["files"].items():
            full_path = task_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

def run(params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Task entry point.
    
    Args:
        params: Parameters dictionary with:
            - url: Task URL to clone
            - version: Optional version to clone
            
    Returns:
        Dictionary with task results
    """
    try:
        params = params or {}
        url = params.get("url")
        if not url:
            raise ValueError("URL parameter is required")
            
        # Parse URL and fetch task
        user_id, task_name = parse_task_url(url)
        api = TaskHubAPI()
        task_data = api.get_task(user_id, task_name, include_files=True)
        
        # Create directory and write files
        task_dir = create_task_directory(task_name)
        write_task_files(task_dir, task_data)
        
        return {
            "status": "success",
            "message": f"Successfully cloned task to {task_dir}",
            "task_name": task_name,
            "task_dir": str(task_dir)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        } 