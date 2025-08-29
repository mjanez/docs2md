"""
Logging utilities for docs2md project.

This module provides utilities for setting up and managing logging
across the application with proper file rotation and cleanup.
"""

import os
import logging
import logging.handlers
from datetime import datetime
from pathlib import Path
from typing import Optional
from utils.path_utils import ensure_directory_exists


class LogManager:
    """
    Manager for application logging with automatic file rotation and cleanup.
    """
    
    def __init__(self, log_folder: Path, output_file_base: str, max_log_files: int = 10):
        """
        Initialize the log manager.
        
        Args:
            log_folder: Directory where log files will be stored.
            output_file_base: Base name for the log file.
            max_log_files: Maximum number of log files to keep (default: 10).
        """
        self.log_folder = ensure_directory_exists(log_folder)
        self.output_file_base = output_file_base
        self.max_log_files = max_log_files
        self._setup_logging()
        self._cleanup_old_logs()
    
    def _setup_logging(self) -> None:
        """
        Set up the logging configuration.
        """
        # Clear existing handlers
        logger = logging.getLogger()
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # Create log filename with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d')
        log_filename = self.log_folder / f"{self.output_file_base}_{timestamp}.log"
        
        # Configure logging
        logging.basicConfig(
            handlers=[
                logging.FileHandler(
                    filename=log_filename, 
                    encoding='utf-8', 
                    mode='a+'
                )
            ],
            format="%(asctime)s %(levelname)s::%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S", 
            level=logging.INFO
        )
    
    def _cleanup_old_logs(self) -> None:
        """
        Clean up old log files, keeping only the most recent ones.
        """
        if not self.log_folder.exists():
            return
        
        # Find all log files
        log_files = [
            f for f in self.log_folder.iterdir() 
            if f.is_file() and f.suffix == '.log'
        ]
        
        # Sort by modification time (newest first)
        log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        # Remove old log files beyond the limit
        for log_file in log_files[self.max_log_files:]:
            try:
                log_file.unlink()
                logging.info(f"Cleaned up old log file: {log_file}")
            except OSError as e:
                logging.warning(f"Failed to remove old log file {log_file}: {e}")


def setup_logging(log_folder: Path, output_file_base: str, max_log_files: int = 10) -> LogManager:
    """
    Set up logging for the application.
    
    Args:
        log_folder: Directory where log files will be stored.
        output_file_base: Base name for the log file.
        max_log_files: Maximum number of log files to keep.
    
    Returns:
        LogManager: The configured log manager.
    """
    return LogManager(log_folder, output_file_base, max_log_files)