"""
Base classes and utilities for markdown adjustment functions.
"""

import re
import logging
from pathlib import Path
from typing import Callable, List, Match, Optional
from abc import ABC, abstractmethod


class MarkdownAdjuster(ABC):
    """
    Abstract base class for markdown adjustment operations.
    """
    
    @abstractmethod
    def adjust(self, file_path: Path) -> None:
        """
        Apply adjustments to the markdown file.
        
        Args:
            file_path: Path to the markdown file to adjust.
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this adjuster."""
        pass


class PatternBasedAdjuster(MarkdownAdjuster):
    """
    Base class for pattern-based markdown adjusters.
    """
    
    def __init__(self, pattern: str, replacement_func: Callable[[Match, List[str], int], str]):
        """
        Initialize the pattern-based adjuster.
        
        Args:
            pattern: Regular expression pattern to match.
            replacement_func: Function to generate replacement text.
        """
        self.pattern = re.compile(pattern)
        self.replacement_func = replacement_func
    
    def adjust(self, file_path: Path) -> None:
        """
        Apply pattern-based adjustments to the file.
        
        Args:
            file_path: Path to the markdown file to adjust.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            adjusted_lines = []
            for i, line in enumerate(lines):
                match = self.pattern.search(line)
                if match:
                    replacement = self.replacement_func(match, lines, i)
                    if replacement:
                        adjusted_lines.append(replacement)
                else:
                    adjusted_lines.append(line)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(adjusted_lines)
            
            logging.info(f"Applied {self.name} adjustment to {file_path}")
            
        except Exception as e:
            logging.error(f"Error applying {self.name} adjustment: {e}")
            raise


def apply_adjustments(file_path: Path, adjusters: List[MarkdownAdjuster]) -> None:
    """
    Apply a list of adjustments to a markdown file.
    
    Args:
        file_path: Path to the markdown file.
        adjusters: List of adjuster instances to apply.
    """
    for adjuster in adjusters:
        try:
            adjuster.adjust(file_path)
        except Exception as e:
            logging.error(f"Failed to apply {adjuster.name}: {e}")
            # Continue with other adjusters