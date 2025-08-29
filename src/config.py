"""
Configuration management for docs2md project.

This module handles loading and validation of configuration files,
providing a robust interface for application settings.
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from utils.path_utils import get_project_root, resolve_path


class ConfigError(Exception):
    """Exception raised for configuration-related errors."""
    pass


class Config:
    """
    Configuration manager for docs2md.
    
    This class handles loading, validation, and access to configuration
    settings from YAML files.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file. If None, looks for
                        config.yml in the project root.
        
        Raises:
            ConfigError: If the configuration file cannot be loaded or is invalid.
        """
        self._config = {}
        self._config_path = self._resolve_config_path(config_path)
        self._load_config()
        self._validate_config()
    
    def _resolve_config_path(self, config_path: Optional[str]) -> Path:
        """
        Resolve the configuration file path.
        
        Args:
            config_path: The provided configuration path.
        
        Returns:
            Path: The resolved configuration file path.
        
        Raises:
            ConfigError: If the configuration file doesn't exist.
        """
        if config_path is None:
            config_path = get_project_root() / "config.yml"
        else:
            config_path = resolve_path(config_path)
        
        if not config_path.exists():
            raise ConfigError(f"Configuration file not found: {config_path}")
        
        return config_path
    
    def _load_config(self) -> None:
        """
        Load configuration from the YAML file.
        
        Raises:
            ConfigError: If the file cannot be parsed.
        """
        try:
            with open(self._config_path, 'r', encoding='utf-8') as file:
                self._config = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            raise ConfigError(f"Error parsing configuration file: {e}")
        except IOError as e:
            raise ConfigError(f"Error reading configuration file: {e}")
    
    def _validate_config(self) -> None:
        """
        Validate the loaded configuration.
        
        Raises:
            ConfigError: If required fields are missing or invalid.
        """
        required_fields = ['input_file', 'output_dir']
        
        for field in required_fields:
            if field not in self._config:
                raise ConfigError(f"Required configuration field missing: {field}")
        
        # Validate that input file exists
        input_file = resolve_path(self._config['input_file'])
        if not input_file.exists():
            raise ConfigError(f"Input file not found: {input_file}")
    
    @property
    def input_file(self) -> Path:
        """Get the resolved input file path."""
        return resolve_path(self._config['input_file'])
    
    @property
    def output_dir(self) -> Path:
        """Get the resolved output directory path."""
        return resolve_path(self._config['output_dir'])
    
    @property
    def adjust_functions(self) -> List[str]:
        """Get the list of adjustment functions to apply."""
        return self._config.get('adjust_functions', [])
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key: The configuration key.
            default: Default value if key is not found.
        
        Returns:
            The configuration value or default.
        """
        return self._config.get(key, default)


def load_config(config_path: Optional[str] = None) -> Config:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file.
    
    Returns:
        Config: The configuration object.
    
    Raises:
        ConfigError: If the configuration cannot be loaded.
    """
    return Config(config_path)