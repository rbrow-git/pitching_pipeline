# Utilities

This directory contains general-purpose utility functions that can be used across different parts of the application.

## Purpose

The `utils` package is intended for:

- Helper functions that don't fit into a specific module
- Shared functionality used by multiple parts of the codebase
- General-purpose tools and utilities

## Usage

Import utilities from this package as needed:

```python
from src.utils import some_utility_function
```

## Guidelines

When adding utilities to this directory:

1. Keep functions focused and single-purpose
2. Add proper documentation and type hints
3. Consider writing tests for utility functions
4. Avoid creating dependencies on specific business logic 