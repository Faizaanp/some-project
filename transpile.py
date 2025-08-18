#!/usr/bin/env python3
"""
Command-line transpiler utility.

Usage:
    python transpile.py <input_file.py> [output_dir]
    
Examples:
    python transpile.py examples/example1.py
    python transpile.py my_script.py custom_output_dir
"""

import sys
import os
from main import transpile_file


def main():
    if len(sys.argv) < 2:
        print("Usage: python transpile.py <input_file.py> [output_dir]")
        print("Example: python transpile.py examples/example1.py")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "outputs"
    
    try:
        js_filepath = transpile_file(input_file, output_dir)
        print(f"✅ Successfully transpiled {input_file}")
        print(f"📁 Output saved to: {js_filepath}")
        
        # Show preview of generated file
        with open(js_filepath, "r") as f:
            content = f.read()
        
        print("\n" + "="*50)
        print("GENERATED JAVASCRIPT:")
        print("="*50)
        print(content)
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Transpilation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
