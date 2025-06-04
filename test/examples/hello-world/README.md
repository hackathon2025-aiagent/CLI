# Hello World Task

A simple hello world example demonstrating basic TaskHub task structure.

## Description

This task provides a basic "Hello, World!" implementation in Python, demonstrating:
- Basic task structure
- Configuration setup
- Documentation standards
- Error handling

## Usage

1. Run the task:
```bash
taskhub run hello-world
```

2. Run with custom name:
```bash
taskhub run hello-world --name "Alice"
```

## Implementation

The task consists of:
- `hello.py` - Main implementation
- `taskhub.yaml` - Task configuration
- `README.md` - This documentation

### Code Example

```python
def greet(name: str = "World") -> str:
    """Generate a greeting message."""
    return f"Hello, {name}!"
```

## Configuration

The task uses minimal configuration:

```yaml
name: hello-world
version: 1.0.0
author: Test User
description: Simple hello world example
```

## Testing

Run the tests:
```bash
python -m pytest test_hello.py
```

## License

MIT License - See LICENSE file for details 