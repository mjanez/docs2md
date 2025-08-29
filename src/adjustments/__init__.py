"""
Markdown adjustments package.

This package contains modular markdown adjustment functions organized by functionality.
Each adjustment module contains related functions for specific document formatting tasks.
"""

from .table_adjustments import (
    adjust_markdown_tables,
    remove_bug_double_header_tables,
    adjust_double_header_tables,
    remove_exact_empty_cells_in_tables,
    adjust_complex_double_header_tables
)

from .content_adjustments import (
    adjust_markdown_headers,
    remove_index_texts,
    convert_usage_notes
)

# Registry of all available adjustment functions
ADJUSTMENT_FUNCTIONS = {
    # Table adjustments
    'adjust_markdown_tables': adjust_markdown_tables,
    'remove_bug_double_header_tables': remove_bug_double_header_tables,
    'adjust_double_header_tables': adjust_double_header_tables,
    'remove_exact_empty_cells_in_tables': remove_exact_empty_cells_in_tables,
    'adjust_complex_double_header_tables': adjust_complex_double_header_tables,
    
    # Content adjustments
    'adjust_markdown_headers': adjust_markdown_headers,
    'remove_index_texts': remove_index_texts,
    'convert_usage_notes': convert_usage_notes,
}


def get_adjustment_function(name: str):
    """
    Get an adjustment function by name.
    
    Args:
        name: Name of the adjustment function.
        
    Returns:
        The adjustment function or None if not found.
    """
    return ADJUSTMENT_FUNCTIONS.get(name)


def list_available_adjustments():
    """
    Get a list of all available adjustment function names.
    
    Returns:
        List of available adjustment function names.
    """
    return list(ADJUSTMENT_FUNCTIONS.keys())


def get_adjustments_by_category():
    """
    Get adjustments organized by category.
    
    Returns:
        Dictionary with categories as keys and lists of function names as values.
    """
    return {
        'table_adjustments': [
            'adjust_markdown_tables',
            'remove_bug_double_header_tables', 
            'adjust_double_header_tables',
            'remove_exact_empty_cells_in_tables',
            'adjust_complex_double_header_tables'
        ],
        'content_adjustments': [
            'adjust_markdown_headers',
            'remove_index_texts',
            'convert_usage_notes'
        ]
    }