"""
Main entry point for docs2md converter.

This module provides the main conversion functionality from various document
formats to Markdown using MarkItDown library and custom adjustments.
"""

import sys
import logging
from pathlib import Path
from markitdown import MarkItDown
from config import load_config, ConfigError
from utils.logging_utils import setup_logging
from utils.path_utils import ensure_directory_exists, get_filename_without_extension
import adjust_markdown


def convert_document(config) -> None:
    """
    Convert a document to markdown format and apply adjustments.

    Args:
        config: Configuration object containing input/output settings.

    Raises:
        Exception: If an error occurs during the conversion process.
    """
    try:
        print(f"Starting conversion process...")
        print(f"Input file: {config.input_file}")
        print(f"Output dir: {config.output_dir}")
        
        input_file = config.input_file
        output_dir = ensure_directory_exists(config.output_dir)
        adjust_functions = config.adjust_functions
        
        print(f"Adjustment functions: {adjust_functions}")

        # Generate output file names
        output_file_base = get_filename_without_extension(input_file)
        output_file = output_dir / f"{output_file_base}.md"
        adjusted_output_file = output_dir / f"{output_file_base}_adjusted.md"
        
        print(f"Output file: {output_file}")
        
        # Set up logging
        log_manager = setup_logging(output_dir, output_file_base)

        logging.info("Starting document conversion")
        logging.info("Input file: %s", input_file)
        logging.info("Output directory: %s", output_dir)
        logging.info("Output file: %s", output_file)

        # Convert document to markdown
        print("Converting document...")
        md = MarkItDown()
        logging.info("Converting document to markdown")
        result = md.convert(str(input_file))
        
        # Check if result is None or has no text_content
        if result is None:
            raise ValueError("MarkItDown conversion returned None - file may be unsupported or corrupted")
        
        if not hasattr(result, 'text_content') or result.text_content is None:
            raise ValueError("MarkItDown conversion result has no text_content")
        
        print("Conversion successful, writing to file...")
        
        # Write initial conversion result
        logging.info("Writing result to output file: %s", output_file)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(result.text_content)
        logging.info("Initial conversion completed successfully")

        # Create copy for adjustments
        with open(output_file, 'r', encoding='utf-8') as source:
            content = source.read()
        with open(adjusted_output_file, 'w', encoding='utf-8') as target:
            target.write(content)
        logging.info("Created adjusted output file: %s", adjusted_output_file)

        # Apply adjustments to the adjusted output file
        if adjust_functions:  # Only iterate if there are functions
            print(f"🔧 Applying {len(adjust_functions)} adjustments...")
            for adjust_function_name in adjust_functions:
                adjust_function = adjust_markdown.get_adjustment_function(adjust_function_name)
                if adjust_function:
                    try:
                        adjust_function(str(adjusted_output_file))
                        logging.info(f"Applied adjustment: {adjust_function_name}")
                        print(f"  {adjust_function_name}")
                    except Exception as e:
                        logging.error(f"Failed to apply {adjust_function_name}: {e}")
                        print(f"  {adjust_function_name}: {e}")
                else:
                    logging.warning(f"Adjustment function not found: {adjust_function_name}")
                    print(f"  Function not found: {adjust_function_name}")
        else:
            print("No adjustment functions configured")
                
        logging.info("Document conversion and adjustment completed successfully")
        
    except Exception as e:
        logging.error("An error occurred during conversion: %s", str(e))
        print(f"Error in convert_document: {e}")
        raise


def main(config_path: str) -> None:
    """
    Main function to convert a document to markdown format.

    Args:
        config_path: Path to the configuration file.

    Raises:
        SystemExit: If configuration cannot be loaded or conversion fails.
    """
    try:
        print(f"docs2md starting...")
        print(f"Config file: {config_path}")
        
        # Load and validate configuration
        config = load_config(config_path)
        print(f"Configuration loaded successfully")
        
        # Convert document
        convert_document(config)
        
        print("Document conversion completed successfully!")
        print(f"Output directory: {config.output_dir}")
        
    except ConfigError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Conversion error: {e}")
        logging.error("Fatal error in main: %s", str(e))
        import traceback
        print(f"Full traceback:")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <config.yml>")
        print("Example: python src/main.py config.yml")
        sys.exit(1)
    
    main(sys.argv[1])