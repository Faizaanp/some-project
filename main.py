"""
Main transpiler application.

Provides core transpilation functionality from Python to JavaScript
with file output capabilities.
"""

import os
from datetime import datetime
from parser import parse_python_to_ir
from codegen_js import transpile_to_js


def save_js_output(js_code: str, filename: str, description: str = "") -> str:
    """Save JavaScript output to a file in the outputs directory"""
    # Ensure outputs directory exists
    outputs_dir = "outputs"
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
    
    # Create filename with timestamp to avoid conflicts
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = filename.replace(".py", "")
    js_filename = f"{base_name}_{timestamp}.js"
    js_filepath = os.path.join(outputs_dir, js_filename)
    
    # Add header comment to the JavaScript file
    header = f"""// Generated JavaScript from {filename}
// Transpiled on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
// Description: {description}

"""
    
    # Write JavaScript code to file
    with open(js_filepath, "w") as f:
        f.write(header + js_code)
    
    return js_filepath


def transpile_python_to_js(python_code: str) -> str:
    """Complete transpilation pipeline from Python source to JavaScript"""
    try:
        # Step 1: Parse Python to IR
        ir_program = parse_python_to_ir(python_code)
        
        # Step 2: Generate JavaScript from IR
        js_code = transpile_to_js(ir_program)
        
        return js_code
    except Exception as e:
        raise RuntimeError(f"Transpilation failed: {str(e)}")


def transpile_examples():
    """all file in examples directory"""
    examples_dir = "examples"
    
    if not os.path.exists(examples_dir):
        print(f"Examples directory '{examples_dir}' not found.")
        return []
    
    transpiled_files = []
    
    print("Transpiling example files...")
    for filename in os.listdir(examples_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(examples_dir, filename)
            
            try:
                with open(filepath, "r") as file:
                    python_code = file.read()
                
                js_code = transpile_python_to_js(python_code)
                js_filepath = save_js_output(js_code, filename, f"Transpiled from {filename}")
                transpiled_files.append(js_filepath)
                
                print(f"{filename} -> {os.path.basename(js_filepath)}")
            except Exception as e:
                print(f" Error transpiling {filename}: {e}")
    
    return transpiled_files


def transpile_file(input_filepath: str, output_dir: str = "outputs") -> str:
    """single file transpilation"""
    if not os.path.exists(input_filepath):
        raise FileNotFoundError(f"Input file not found: {input_filepath}")
    
    filename = os.path.basename(input_filepath)
    
    with open(input_filepath, "r") as f:
        python_code = f.read()
    
    js_code = transpile_python_to_js(python_code)
    js_filepath = save_js_output(js_code, filename, f"Transpiled from {input_filepath}")
    
    return js_filepath


def main():
    """Main entry point"""
    print("Python to JavaScript Transpiler")
    print("=" * 40)

    transpiled_files = transpile_examples()

    if transpiled_files:
        print(f"\nSuccessfully transpiled {len(transpiled_files)} files:")
        for filepath in transpiled_files:
            print(f"   {filepath}")
        print(f"\nAll files saved in 'outputs/' directory")
    else:
        print("\nNo files were transpiled.")


if __name__ == "__main__":
    main()
