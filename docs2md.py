#!/usr/bin/env python3
"""
Entry point script for docs2md.

This script provides a simple entry point for running the docs2md converter
without needing to specify the full path to the source files.
"""

import sys
import os
from pathlib import Path

def setup_environment():
    """Set up the Python environment for running docs2md."""
    project_root = Path(__file__).parent
    src_dir = project_root / "src"
    
    # Add the src directory to the Python path
    sys.path.insert(0, str(src_dir))
    
    # Change to the project directory to ensure relative paths work correctly
    os.chdir(project_root)
    
    return project_root

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        # Try to import markitdown first as it's the most likely to fail
        import markitdown
        return True
    except ImportError as e:
        print("Missing dependency error:")
        print(f"   {e}")
        print()
        print("Try these solutions:")
        print("   1. Reinstall dependencies: pdm install")
        print("   2. Check your virtual environment: pdm info")
        print("   3. If using system Python: pip install markitdown pyyaml")
        return False
    except Exception as e:
        print(f"Dependency check failed: {e}")
        print("Try reinstalling: pdm install")
        return False

def main():
    """Main entry point for docs2md."""
    if len(sys.argv) != 2:
        print("Usage: python docs2md.py <config.yml>")
        print("Example: python docs2md.py config.yml")
        print()
        print("ℹAlternative usage:")
        print("   pdm run python src/main.py config.yml")
        sys.exit(1)
    
    try:
        # Set up environment
        project_root = setup_environment()
        config_path = sys.argv[1]
        
        # Resolve config path relative to project root
        if not Path(config_path).is_absolute():
            config_path = project_root / config_path
        
        # Check if config file exists
        if not Path(config_path).exists():
            print(f"Configuration file not found: {config_path}")
            print("Create one from the example:")
            print("   cp config.yml.example config.yml")
            sys.exit(1)
        
        # Check dependencies before importing
        print("Checking dependencies...")
        if not check_dependencies():
            sys.exit(1)
        
        print("Dependencies OK")
        
        # Import and run the main function
        try:
            from main import main as docs2md_main
            docs2md_main(str(config_path))
        except ImportError as e:
            print(f"Error importing main module: {e}")
            print("Make sure you're running from the project root directory")
            print("Current directory:", os.getcwd())
            print("Python path:", sys.path[:3])
            sys.exit(1)
        except KeyboardInterrupt:
            print("\nConversion interrupted by user")
            sys.exit(130)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()