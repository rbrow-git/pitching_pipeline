#!/usr/bin/env python3
"""
Centralized logging configuration for Baseball Pitching Pipeline.

This module provides a unified logging setup that should be used
by all other modules in the application instead of configuring 
logging individually in each module.
"""

import logging
import re
import sys
import os

class EssentialMessagesFilter(logging.Filter):
    """Filter that only allows important messages in non-verbose mode."""
    
    def __init__(self, verbose_mode=False):
        super().__init__()
        self.verbose_mode = verbose_mode
        
    def filter(self, record):
        # Always show warnings and errors regardless of mode
        if record.levelno >= logging.WARNING:
            return True
            
        # In verbose mode, show everything
        if self.verbose_mode:
            return True
            
        # In minimal mode, only show messages with [ESSENTIAL] prefix
        # and strip the prefix before displaying
        msg = record.getMessage()
        if "[ESSENTIAL]" in msg:
            # Remove the prefix so it's not displayed
            record.msg = record.msg.replace("[ESSENTIAL] ", "")
            record.msg = record.msg.replace("[ESSENTIAL]", "")
            return True
                
        # Filter out other INFO messages
        return False

class MinimalLogHandler(logging.Handler):
    """Custom log handler that provides minimal output formatting."""
    
    def __init__(self, level=logging.INFO):
        super().__init__(level)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', 
                                          '%Y-%m-%d %H:%M:%S'))
        
    def emit(self, record):
        # Only emit if this record passes our filters
        if self.filter(record):
            message = self.format(record)
            print(message)

class LoggingManager:
    """Centralized logging configuration manager."""
    
    _instance = None
    
    def __new__(cls):
        # Singleton pattern to ensure only one logging configuration exists
        if cls._instance is None:
            cls._instance = super(LoggingManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        # Only initialize once
        if self._initialized:
            return
        
        # Get the root logger
        self.root_logger = logging.getLogger()
        
        # Check environment variable for log level
        env_log_level = os.environ.get("BASEBALL_LOG_LEVEL", "INFO")
        default_level = self._get_log_level_from_string(env_log_level)
        
        self.root_logger.setLevel(default_level)
        
        # Clear existing handlers to avoid duplicates
        for handler in self.root_logger.handlers[:]:
            self.root_logger.removeHandler(handler)
        
        # Create the filter
        self.filter = EssentialMessagesFilter(verbose_mode=(default_level <= logging.DEBUG))
        
        # Add our custom handler for normal logs
        self.handler = MinimalLogHandler(default_level)
        self.handler.addFilter(self.filter)
        self.root_logger.addHandler(self.handler)
        
        # Special handler for error logging
        self.error_handler = logging.StreamHandler(sys.stderr)
        self.error_handler.setLevel(logging.ERROR)
        self.error_handler.setFormatter(logging.Formatter(
            '%(asctime)s - ERROR - %(name)s - %(message)s',
            '%Y-%m-%d %H:%M:%S'))
        self.root_logger.addHandler(self.error_handler)
        
        # Configure default log levels for third-party loggers
        self._configure_third_party_loggers()
        
        self._initialized = True
    
    def _configure_third_party_loggers(self):
        """Configure default log levels for known third-party libraries."""
        # Set most third-party loggers to WARNING to reduce noise
        for logger_name in logging.root.manager.loggerDict:
            if not logger_name.startswith('src.'):
                logging.getLogger(logger_name).setLevel(logging.WARNING)
        
        # Preserve specific logger settings
        scrapling_logger = logging.getLogger('scrapling')
        if scrapling_logger:
            scrapling_logger.setLevel(logging.WARNING)  # Keep scrapling quiet
    
    def _get_log_level_from_string(self, level_str):
        """Convert a string log level to a logging level constant."""
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        return level_map.get(level_str.upper(), logging.INFO)
    
    def set_verbose(self, verbose):
        """Set the verbosity level for all loggers."""
        if verbose:
            # In verbose mode, show more logs
            self.root_logger.setLevel(logging.DEBUG)
            self.filter.verbose_mode = True
            
            # Project modules get DEBUG level
            for logger_name in logging.root.manager.loggerDict:
                if logger_name.startswith('src.'):
                    logging.getLogger(logger_name).setLevel(logging.DEBUG)
        else:
            # Check environment variable first
            env_log_level = os.environ.get("BASEBALL_LOG_LEVEL", "INFO")
            default_level = self._get_log_level_from_string(env_log_level)
            
            # In minimal mode, be selective about what to show
            self.root_logger.setLevel(default_level)
            self.filter.verbose_mode = False
            
            # Project modules get default level, third-party gets WARNING
            for logger_name in logging.root.manager.loggerDict:
                if logger_name.startswith('src.'):
                    logging.getLogger(logger_name).setLevel(default_level)
                else:
                    logging.getLogger(logger_name).setLevel(logging.WARNING)

# Create a singleton instance of the logging manager
_logging_manager = LoggingManager()

def setup_logging(verbose=False):
    """
    Set up logging configuration for the application.
    
    This is the main entry point for all modules to use the centralized logging.
    
    Args:
        verbose (bool): Whether to enable verbose logging
    """
    _logging_manager.set_verbose(verbose)
    return _logging_manager

def get_logger(name):
    """
    Get a logger with the specified name.
    
    This function should be used instead of logging.getLogger() directly.
    
    Args:
        name (str): The name of the logger
        
    Returns:
        logging.Logger: A properly configured logger
    """
    return logging.getLogger(name) 