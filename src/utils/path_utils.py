"""
Path utilities for docs2md project.

This module provides utility functions for robust path handling
across different operating systems and environments.
"""

import os
from pathlib import Path
from typing import Union, Optional


def get_project_root() -> Path:
    """
    Get the project root directory.
    
    Returns:
        Path: The absolute path to the project root directory.
    """
    return Path(__file__).parent.parent.parent


def resolve_path(path: Union[str, Path], base_dir: Optional[Union[str, Path]] = None) -> Path:
    """
    Resolve a path relative to the base directory or project root.
    
    Args:
        path: The path to resolve (can be absolute or relative).
        base_dir: The base directory to resolve relative paths against.
                 If None, uses the project root.
    
    Returns:
        Path: The resolved absolute path.
    """
    path = Path(path)
    
    if path.is_absolute():
        return path
    
    if base_dir is None:
        base_dir = get_project_root()
    else:
        base_dir = Path(base_dir)
    
    return (base_dir / path).resolve()


def ensure_directory_exists(path: Union[str, Path]) -> Path:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        path: The directory path to create.
    
    Returns:
        Path: The absolute path to the directory.
    
    Raises:
        OSError: If the directory cannot be created.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def get_file_extension(path: Union[str, Path]) -> str:
    """
    Get the file extension from a path.
    
    Args:
        path: The file path.
    
    Returns:
        str: The file extension (without the dot).
    """
    return Path(path).suffix.lower().lstrip('.')


def get_filename_without_extension(path: Union[str, Path]) -> str:
    """
    Get the filename without extension from a path.
    
    Args:
        path: The file path.
    
    Returns:
        str: The filename without extension.
    """
    return Path(path).stem