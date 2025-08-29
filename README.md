# docs2md - Document to Markdown Converter

A robust Python tool that converts various document formats (PDF, Word, Excel, Images, Audio, HTML, PowerPoint, text-based files like CSV/JSON/XML, ZIP, YouTube URLs, EPUBs) to Markdown format with customizable post-processing adjustments.

## Features

- **Multi-format support**: PDF, DOCX, XLSX, images, audio, HTML, PowerPoint, CSV, JSON, XML, ZIP, YouTube URLs, EPUBs
- **Customizable adjustments**: Built-in markdown post-processing functions for tables, headers, and formatting
- **Robust path handling**: Cross-platform path resolution and validation
- **Comprehensive logging**: Detailed logs with automatic rotation and cleanup
- **YAML configuration**: Easy-to-use configuration system
- **Modular architecture**: Clean, maintainable codebase with separation of concerns

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mjanez/docs2md.git
   cd docs2md
   ```

2. **Install dependencies using PDM:**
   ```bash
   pdm install
   ```

   > **Note**: This project uses [PDM](https://pdm-project.org/) for dependency management. If you don't have PDM installed, install it first:
   > ```bash
   > pip install pdm
   > ```

## Configuration

Create a configuration file by copying the example template:

```bash
cp config.yml.example config.yml
```

Edit `config.yml` to specify your input file and output directory:

```yaml
# docs2md configuration
input_file: "input/docx/your-document.docx"
output_dir: "output"

# Optional: markdown adjustment functions
adjust_functions:
  - adjust_markdown_tables
  - remove_index_texts
  - convert_usage_notes
  - remove_bug_double_header_tables
  - adjust_double_header_tables
  - remove_exact_empty_cells_in_tables
  - adjust_complex_double_header_tables
```

### Configuration Options

- **`input_file`**: Path to your input document (relative to project root)
- **`output_dir`**: Directory where converted files will be saved
- **`adjust_functions`**: List of post-processing functions to apply (optional)

### Available Adjustment Functions

The adjustment functions are now organized in specialized modules:

#### Table Adjustments
- `adjust_markdown_tables`: Improves table formatting by splitting applicability information
- `remove_bug_double_header_tables`: Fixes tables with duplicate headers
- `adjust_double_header_tables`: Merges double header rows into proper single headers
- `remove_exact_empty_cells_in_tables`: Cleans up empty table cells
- `adjust_complex_double_header_tables`: Handles complex table structures with proper sectioning

#### Content Adjustments
- `adjust_markdown_headers`: Adjusts header structure (placeholder for future implementation)
- `remove_index_texts`: Removes stray index references like "Tabla . 1 - Description"
- `convert_usage_notes`: Converts usage notes to proper markdown note blocks
- `remove_empty_lines_excess`: Reduces excessive empty lines while preserving structure
- `normalize_whitespace`: Standardizes whitespace usage throughout the document

## Usage

### Basic Usage

Convert a document using your configuration file:

```bash
pdm run python src/main.py config.yml
```

### Advanced Usage

You can create multiple configuration files for different documents:

```bash
# Create specific config files
cp config.yml config-document1.yml
cp config.yml config-document2.yml

# Convert different documents
pdm run python src/main.py config-document1.yml
pdm run python src/main.py config-document2.yml
```

### Example Workflow

1. **Place your document** in the `input/` directory (create subdirectories as needed)
2. **Update config.yml** with the correct input file path
3. **Run the converter**:
   ```bash
   pdm run python src/main.py config.yml
   ```
4. **Check the output** in your specified output directory

## Output

The tool generates two files:
- `[filename].md`: The raw converted markdown
- `[filename]_adjusted.md`: The markdown with applied adjustments

Logs are automatically saved in the output directory with timestamps and automatic cleanup (keeps 10 most recent log files).

## Modular Adjustment System

The adjustment functions have been organized into specialized modules for better maintainability and traceability:

### Table Adjustments (`adjustments/table_adjustments.py`)
- `adjust_markdown_tables`: Split applicability into separate rows
- `remove_bug_double_header_tables`: Remove duplicate header rows
- `adjust_double_header_tables`: Fix malformed headers
- `remove_exact_empty_cells_in_tables`: Clean empty table cells
- `adjust_complex_double_header_tables`: Handle complex table structures

### Content Adjustments (`adjustments/content_adjustments.py`)
- `adjust_markdown_headers`: Header structure improvements
- `remove_index_texts`: Remove table references and indices
- `convert_usage_notes`: Convert notes to markdown note blocks
- `remove_empty_lines_excess`: Reduce excessive empty lines
- `normalize_whitespace`: Standardize whitespace usage

### Using Specific Adjustment Categories

You can now apply only specific types of adjustments:

```bash
# Apply only table adjustments
python demo_adjustments.py table output/document.md

# Apply only content adjustments  
python demo_adjustments.py content output/document.md

# Apply custom pipeline
python demo_adjustments.py custom output/document.md "adjust_markdown_tables,remove_index_texts"

# Show available adjustments
python demo_adjustments.py info
```

### Advanced Configuration

Create targeted configuration files for different adjustment needs:

```yaml
# config-tables-only.yml
input_file: "input/docx/document.docx"
output_dir: "output"
adjust_functions:
  - adjust_markdown_tables
  - remove_exact_empty_cells_in_tables
  - adjust_double_header_tables
```

```yaml
# config-content-only.yml  
input_file: "input/docx/document.docx"
output_dir: "output"
adjust_functions:
  - remove_index_texts
  - convert_usage_notes
  - normalize_whitespace
```

## Development

If you want to add a new adjustment (e.g., to fix a specific table pattern or normalize specific text), follow these steps to maintain consistency with the modular architecture:

1. Create the adjustment module

    - Create a file in `src/adjustments/`, for example `src/adjustments/my_adjustments.py` or group by category (`table_*`, `content_*`).
    - Import base utilities from `src/adjustments/base.py`:

```python
from .base import validate_file_path, apply_pattern_to_file, apply_line_replacements
import re
import logging

def my_new_adjustment(file_path: str) -> None:
    """Describe what the adjustment does.

    Args:
        file_path: Path to the markdown file to modify.
    """
    file_path = validate_file_path(file_path)

    # Example: replace by pattern in each line
    pat = re.compile(r"PATTERN_TO_SEARCH")

    def repl(match, lines, i):
        # Build and return the replacement string for the line
        return match.group(0).replace('old', 'new')

    apply_pattern_to_file(file_path, pat, repl)
    logging.info(f"Applied my_new_adjustment to {file_path}")
```

2. Register the adjustment in the adjustments package

    - Open `src/adjustments/__init__.py` and add an import and an entry in `ADJUSTMENT_FUNCTIONS`:

```python
from .my_adjustments import my_new_adjustment

ADJUSTMENT_FUNCTIONS['my_new_adjustment'] = my_new_adjustment
```

3. Add tests

    - Create a test in `tests/test_my_adjustment.py` that creates a temporary file, runs the function, and validates the output (using `pytest`):

```python
import tempfile
from adjustments.my_adjustments import my_new_adjustment

def test_my_new_adjustment():
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.md', delete=False) as tmp:
        tmp.write('| **Applicability** | old. 1 |\n')
        tmp.flush()
        my_new_adjustment(tmp.name)
        tmp.seek(0)
        content = tmp.read()
    assert 'new' in content
```

    - Run the tests:

```bash
pdm run pytest tests/test_my_adjustment.py
```

4. Hot test / dry-run

    - Use the demo script to apply and check the adjustment without modifying the global configuration:

```bash
python demo_adjustments.py custom output/document.md "my_new_adjustment"
```

General Best Practices for Adjustments:
- Add clear docstrings describing inputs/outputs and side effects.
- Ensure idempotency: running the adjustment multiple times should not break the document.
- Handle errors with logging and avoid silent exceptions.
- Optimize regex patterns to avoid unnecessary iteration over large lines.
- If the adjustment is costly, consider processing in chunks or using a `max_rows` parameter in the function for testing.

With this template, you can create specialized adjustments and easily register them in the modular system.

## Troubleshooting

### Common Issues

1. **"Configuration file not found"**
   - Ensure `config.yml` exists in the project root
   - Check that the path to your config file is correct

2. **"Input file not found"**
   - Verify the `input_file` path in your config.yml
   - Ensure the file exists and is accessible

3. **Python import errors**
   - Make sure you're running from the project root: `pdm run python src/main.py config.yml`
   - Verify all dependencies are installed: `pdm install`

4. **Permission errors**
   - Ensure you have read access to input files
   - Verify write permissions for the output directory

### Getting Help

- Check the logs in your output directory for detailed error information
- Review the configuration file format against the example
- Ensure all required fields are present in your config.yml

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License. See the [LICENSE](/LICENSE) file for details.
