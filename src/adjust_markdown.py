"""
Markdown adjustment functions for docs2md project.

This module now serves as a compatibility layer and main entry point
for the modularized adjustment functions. The actual implementations
have been moved to specialized modules in the adjustments package.

DEPRECATED: Import functions directly from adjustments package for new code.
"""

import logging
from adjustments import (
    get_adjustment_function,
    list_available_adjustments,
    get_adjustments_by_category,
    ADJUSTMENT_FUNCTIONS
)

# Re-export all adjustment functions for backward compatibility
from adjustments.table_adjustments import (
    adjust_markdown_tables,
    remove_bug_double_header_tables,
    adjust_double_header_tables,
    remove_exact_empty_cells_in_tables,
    adjust_complex_double_header_tables
)

from adjustments.content_adjustments import (
    adjust_markdown_headers,
    remove_index_texts,
    convert_usage_notes
)

# Backward compatibility - maintain the original interface
def get_adjustment_function(name: str):
    """
    Get an adjustment function by name.
    
    Args:
        name: Name of the adjustment function.
        
    Returns:
        The adjustment function or None if not found.
        
    Note:
        This function is maintained for backward compatibility.
        Consider importing directly from adjustments package.
    """
    from adjustments import get_adjustment_function as _get_func
    return _get_func(name)


def show_available_adjustments():
    """
    Display information about available adjustment functions organized by category.
    
    This is a utility function for developers to see what adjustments are available.
    """
    categories = get_adjustments_by_category()
    
    print("📋 Available Markdown Adjustments:")
    print("=" * 50)
    
    for category, functions in categories.items():
        print(f"\n🔧 {category.replace('_', ' ').title()}:")
        for func_name in functions:
            func = ADJUSTMENT_FUNCTIONS.get(func_name)
            if func and func.__doc__:
                # Extract first line of docstring as summary
                summary = func.__doc__.strip().split('\n')[0]
                print(f"  • {func_name}: {summary}")
            else:
                print(f"  • {func_name}: No description available")
    
    print(f"\n📊 Total functions available: {len(list_available_adjustments())}")


if __name__ == "__main__":
    # Show available adjustments when module is run directly
    show_available_adjustments()