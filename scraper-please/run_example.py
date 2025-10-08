#!/usr/bin/env python
"""
Launcher script for example_usage.py
This ensures the package is imported correctly as a module.
"""
import runpy
import sys
from pathlib import Path

# Remove current directory from path to avoid local import conflicts
project_root = str(Path(__file__).parent)
if project_root in sys.path:
    sys.path.remove(project_root)
if '' in sys.path:
    sys.path.remove('')
if '.' in sys.path:
    sys.path.remove('.')

# Now run the example
if __name__ == "__main__":
    runpy.run_path("example_usage.py", run_name="__main__")
