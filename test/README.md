# Test Task Structure

This directory contains example tasks and configurations for the TaskHub CLI tool. The structure demonstrates best practices for creating, organizing, and publishing tasks.

## Directory Structure

```
test/
├── README.md           # This documentation file
├── rules/             # Task validation rules and schemas
│   ├── basic/        # Basic validation rules
│   └── advanced/     # Advanced validation rules
├── mcp/              # MCP (Model Control Protocol) examples
│   ├── simple/       # Simple MCP configurations
│   └── complex/      # Complex MCP configurations
└── examples/         # Complete task examples
    ├── hello-world/  # Basic hello world example
    └── calculator/   # More complex calculator example
```

## Task Components

Each task should include the following components:

1. **README.md** - Task documentation and instructions
2. **taskhub.yaml** - Task configuration and metadata
3. **Source Files** - Implementation files
4. **Tests** (optional) - Test files for validation

### taskhub.yaml Structure

```yaml
name: task-name
version: 1.0.0
author: Author Name
description: Task description
license: MIT
tags:
  - example
  - demo
dependencies:
  - package1>=1.0.0
  - package2~=2.0.0
```

## Rules

The `rules/` directory contains validation rules for tasks:

### Basic Rules
- Valid README.md file
- Valid taskhub.yaml configuration
- Required files present
- Proper file structure

### Advanced Rules
- Code quality checks
- Security validation
- Performance benchmarks
- Dependency validation

## MCP Examples

The `mcp/` directory contains Model Control Protocol examples:

### Simple MCP
- Basic task execution
- Single model interaction
- Simple input/output handling

### Complex MCP
- Multi-model orchestration
- Advanced state management
- Error handling and recovery
- Custom validation rules

## Usage Examples

1. **Creating a New Task**
```bash
taskhub create my-task
cd my-task
# Edit README.md and taskhub.yaml
```

2. **Validating a Task**
```bash
taskhub validate my-task
```

3. **Publishing a Task**
```bash
taskhub publish my-task --user-id your-user-id
```

4. **Running a Task**
```bash
taskhub run my-task
```

## Best Practices

1. **Documentation**
   - Clear and concise README
   - Well-documented code
   - Usage examples

2. **Configuration**
   - Minimal dependencies
   - Specific version constraints
   - Clear metadata

3. **Implementation**
   - Modular code structure
   - Error handling
   - Input validation

4. **Testing**
   - Unit tests
   - Integration tests
   - Example inputs/outputs

## Contributing

1. Fork the repository
2. Create your feature branch
3. Add your task or improvements
4. Submit a pull request

## License

MIT License - See LICENSE file for details
