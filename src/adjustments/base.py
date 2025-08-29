"""
Base utilities for markdown adjustments.

This module provides common functionality shared across all adjustment modules.
"""

import re
import logging
from pathlib import Path
from typing import Callable, List, Match, Any


def apply_pattern_to_file(file_path: Path, pattern: re.Pattern, replacement_func: Callable) -> None:
    """
    Apply a regex pattern to each line in the given file and use a replacement function to modify matching lines.

    Args:
        file_path: Path to the Markdown file.
        pattern: Compiled regex pattern to search for.
        replacement_func: Function that takes a regex match object and returns the replacement string.
        
    Raises:
        Exception: If file operations fail.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        adjusted_lines = []
        for i, line in enumerate(lines):
            match = pattern.search(line)
            if match:
                replacement = replacement_func(match, lines, i)
                if replacement is not None:
                    adjusted_lines.append(replacement)
            else:
                adjusted_lines.append(line)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(adjusted_lines)
            
        logging.info(f"Applied pattern adjustment to {file_path}")
        
    except Exception as e:
        logging.error(f"Error applying pattern to file {file_path}: {e}")
        raise


def apply_line_replacements(file_path: Path, replacement_func: Callable[[str], str]) -> None:
    """
    Apply line-by-line replacements to a file.
    
    Args:
        file_path: Path to the Markdown file.
        replacement_func: Function that takes a line and returns the modified line.
        
    Raises:
        Exception: If file operations fail.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        adjusted_lines = [replacement_func(line) for line in lines]

        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(adjusted_lines)
            
        logging.info(f"Applied line replacements to {file_path}")
        
    except Exception as e:
        logging.error(f"Error applying line replacements to {file_path}: {e}")
        raise


def validate_file_path(file_path: str) -> Path:
    """
    Validate and convert file path to Path object.
    
    Args:
        file_path: String path to validate.
        
    Returns:
        Path object.
        
    Raises:
        ValueError: If file doesn't exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")
    return path