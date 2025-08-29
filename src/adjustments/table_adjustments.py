"""
Table-specific markdown adjustments.

This module contains all functions related to adjusting table formatting
in markdown documents, including header fixes, cell cleanup, and structure improvements.
"""

import re
import logging
from pathlib import Path
from .base import apply_pattern_to_file, apply_line_replacements, validate_file_path


def adjust_markdown_tables(file_path: str) -> None:
    """
    Adjust the tables in the given Markdown file by splitting applicability information.
    
    This function looks for tables with "Aplicabilidad" headers and splits the content
    into separate "Aplicabilidad" and "Cardinalidad" rows for better readability.

    Args:
        file_path: Path to the Markdown file.
        
    Example:
        Input:  | **Aplicabilidad** | **Obligatorio. 1** |
        Output: | **Aplicabilidad** | **Obligatorio** |
                | **Cardinalidad** | **1** |
    """
    file_path = validate_file_path(file_path)
    pattern = re.compile(r'\|\s*\*\*Aplicabilidad\*\*\s*\|\s*\*\*(.*?)\*\*\s*\|')

    def replacement_func(match, lines, i):
        applicability = match.group(1)
        if applicability:
            parts = applicability.split('. ')
            if len(parts) == 2:
                return f"| **Aplicabilidad** | **{parts[0]}** |\n| **Cardinalidad** | **{parts[1]}** |\n"
        return match.group(0)

    apply_pattern_to_file(file_path, pattern, replacement_func)
    logging.info(f"Adjusted markdown tables in {file_path}")


def remove_bug_double_header_tables(file_path: str) -> None:
    """
    Remove tables with duplicate header rows.
    
    This function removes the redundant second header row that appears in some
    automatically converted tables.

    Args:
        file_path: Path to the Markdown file.
        
    Example:
        Removes: | Obligatorias | Recomendadas | Opcionales |
    """
    file_path = validate_file_path(file_path)
    pattern = re.compile(r'^\| Obligatorias \| Recomendadas \| Opcionales \|\s*$')

    def replacement_func(match, lines, i):
        return ""

    apply_pattern_to_file(file_path, pattern, replacement_func)
    logging.info(f"Removed duplicate header tables in {file_path}")


def adjust_double_header_tables(file_path: str) -> None:
    """
    Adjust tables with incomplete double header rows into proper single header rows.
    
    This function fixes tables where the header structure is malformed due to
    conversion issues, creating a proper header with all necessary columns.

    Args:
        file_path: Path to the Markdown file.
        
    Example:
        Input:  | Clase | URI de la clase | Propiedades | | |
        Output: | Clase | URI de la clase | Obligatorias | Recomendadas | Opcionales |
                | --- | --- | --- | --- | --- |
    """
    file_path = validate_file_path(file_path)
    pattern = re.compile(r'\| Clase \| URI de la clase \| Propiedades \| \| \|')

    def replacement_func(match, lines, i):
        return f'| Clase | URI de la clase | Obligatorias | Recomendadas | Opcionales |\n| --- | --- | --- | --- | --- |\n'

    apply_pattern_to_file(file_path, pattern, replacement_func)
    logging.info(f"Adjusted double header tables in {file_path}")


def remove_exact_empty_cells_in_tables(file_path: str) -> None:
    """
    Remove empty cells in tables by collapsing consecutive separators.
    
    This function cleans up table formatting by removing empty cells that appear
    as consecutive pipe separators (| |).

    Args:
        file_path: Path to the Markdown file.
        
    Example:
        Input:  | Content | | More content |
        Output: | Content | More content |
    """
    file_path = validate_file_path(file_path)
    
    def clean_empty_cells(line: str) -> str:
        if line.startswith('|'):
            # Replace all occurrences of '| |' with '|'
            while '| |' in line:
                line = line.replace('| |', '|')
        return line

    apply_line_replacements(file_path, clean_empty_cells)
    logging.info(f"Removed empty cells from tables in {file_path}")


def adjust_complex_double_header_tables(file_path: str) -> None:
    """
    Adjust complex tables with double header rows into proper structure.
    
    This function handles complex table structures where the first row should become
    a level 2 header and subsequent rows form a proper table structure.

    Args:
        file_path: Path to the Markdown file.
        
    Example:
        Converts complex header structures to:
        ## Section Header
        
        | Metadato | Descripción | propiedad | T | C | RANGO |
        | --- | --- | --- | --- | --- | --- |
        | content... |
    """
    file_path = validate_file_path(file_path)
    pattern = re.compile(r'^\|.*\|\s*$')

    def replacement_func(match, lines, i):
        header_line = lines[i].strip()
        next_line = lines[i + 1].strip() if i + 1 < len(lines) else ''
        
        if next_line.startswith('| ---'):
            third_line = lines[i + 2].strip() if i + 2 < len(lines) else ''
            if third_line.startswith('| Metadato | Descripción | propiedad | T | C | RANGO |'):
                # Extract header parts and create level 2 header
                header_parts = [part.strip() for part in header_line.split('|') if part.strip()]
                level_2_header = '## ' + ' - '.join(header_parts)
                
                # Calculate number of columns
                num_columns = len(third_line.split('|')) - 2  # Subtract 2 for leading/trailing '|'
                separator_line = '| ' + ' | '.join(['---'] * num_columns) + ' |'
                table_header = third_line
                
                # Collect table content
                table_content = []
                for line in lines[i + 3:]:
                    if line.startswith('|'):
                        table_content.append(line)
                    else:
                        break
                
                # Validate table structure
                for row in table_content:
                    if len(row.split('|')) - 2 != num_columns:
                        logging.warning(f"Row with different number of columns found: {row.strip()}")
                
                return f'{level_2_header}\n\n{table_header}\n{separator_line}\n' + ''.join(table_content)
        
        return match.group(0)

    apply_pattern_to_file(file_path, pattern, replacement_func)
    logging.info(f"Adjusted complex double header tables in {file_path}")