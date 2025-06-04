# Clone Task Example

This example demonstrates how to clone a task from the TaskHub marketplace.

## Description

The clone task functionality:
- Fetches task metadata and files from the API
- Creates local directory structure
- Writes task files with proper content
- Maintains original metadata

## Usage

1. Clone a task by URL:
```bash
taskhub clone user123/hello-world
```

2. Clone with specific version:
```bash
taskhub clone user123/hello-world --version 1.0.0
```

## Implementation

The task consists of:
- `clone.py` - Main implementation
- `taskhub.yaml` - Task configuration
- `README.md` - This documentation

### Code Example

```python
def clone_task(url: str) -> str:
    """Clone a task from TaskHub marketplace."""
    # Parse user ID and task name from URL
    user_id, task_name = parse_task_url(url)
    
    # Fetch task data
    task_data = api.get_task(user_id, task_name)
    
    # Create local task directory
    task_dir = create_task_directory(task_name)
    
    # Write task files
    write_task_files(task_dir, task_data)
    
    return task_name
```

## Configuration

```yaml
name: clone-task
version: 1.0.0
author: Test User
description: Task cloning example
```

## Testing

Run the tests:
```bash
python -m pytest test_clone.py
```

## License

MIT License - See LICENSE file for details 