# Logging Best Practices

This document outlines the logging standards for the Baseball Pitching Pipeline project.

## Overview

The project uses a centralized logging configuration defined in `src/core/logging/config.py`. This ensures consistent logging behavior across all modules.

## Key Principles

1. **Minimal Logging**: Only log what's essential by default
2. **Appropriate Log Levels**: Use the right severity level for each message
3. **Environment-Based Configuration**: Different verbosity in development vs. production

## How to Use Logging

### Getting a Logger

Always get a logger using the centralized configuration:

```python
from src.core.logging.config import get_logger

# Get a logger named after the current module
logger = get_logger(__name__)
```

### Log Levels

Use these log levels appropriately:

| Level | When to Use |
|-------|-------------|
| ERROR | For errors that prevent a feature from working |
| WARNING | For concerning issues that don't block execution |
| INFO | For important tracking events (default visible level) |
| DEBUG | For detailed troubleshooting (only visible in verbose mode) |

### Essential vs. Verbose Logs

For critical messages that should appear even in non-verbose mode, use the `[ESSENTIAL]` prefix:

```python
logger.info(f"[ESSENTIAL] Processing {item_id}: operation successful")
```

### Configuration

The logging verbosity is controlled through the CLI's `--verbose` flag, which can be set when running commands:

```bash
uv run src/cli/main.py pitchers --verbose
```

## Recommendations

1. **Don't Overuse Logging**: Avoid excessive debug logs in the primary code path
2. **Log Exceptions Once**: In exception handling, log the error at a single point
3. **Use Parameters**: Use logger.info("Value: %s", value) instead of string formatting
4. **Include Context**: Log relevant IDs and parameters for troubleshooting 