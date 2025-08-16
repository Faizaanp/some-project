"""
Main transpiler application.

This demonstrates the complete pipeline from Python source to JavaScript output
using the modular transpiler architecture.
"""

import os
from lexer import tokenize
from parser import parse_python_to_ir
from codegen_js import transpile_to_js


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


def demo_lexer():
    """Demonstrate the lexer functionality"""
    print("=== LEXER DEMO ===")
    code = """
def greet(name):
    print("Hello")
    print("World")
    if condition:
        print("Condition is true")
    else:
        print("Condition is false")
    # This is a comment
"""

    print("Input Python code:")
    print(code)
    print("\nTokens:")
    tokens = tokenize(code)
    for t in tokens:
        print(t)
    print()


def demo_transpiler():
    """Demonstrate the complete transpilation pipeline"""
    print("=== TRANSPILER DEMO ===")
    python_code = """
def greet(name):
    print("Hello, " + name)

x = 5
y = 10

if x < y:
    print("x is less than y")
elif x == y:
    print("x equals y")
else:
    print("x is greater than y")

for i in range(3):
    print("Iteration", i)

numbers = [1, 2, 3, 4, 5]
if x in numbers:
    print("x is in the list")

greet("World")
"""
    
    print("Input Python code:")
    print(python_code)
    
    try:
        js_code = transpile_python_to_js(python_code)
        print("\nGenerated JavaScript:")
        print(js_code)
    except Exception as e:
        print(f"Error: {e}")
    print()


def run_examples():
    """Run examples from the examples directory"""
    print("=== EXAMPLES DEMO ===")
    examples_dir = "examples"
    
    if not os.path.exists(examples_dir):
        print(f"Examples directory '{examples_dir}' not found.")
        return
    
    for filename in os.listdir(examples_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(examples_dir, filename)
            print(f"\n--- {filename} ---")
            
            with open(filepath, "r") as file:
                python_code = file.read()
            
            print("Python code:")
            print(python_code)
            
            try:
                js_code = transpile_python_to_js(python_code)
                print("\nJavaScript output:")
                print(js_code)
            except Exception as e:
                print(f"Error transpiling {filename}: {e}")
            
            print("-" * 40)


def main():
    """Main entry point"""
    print("Python to JavaScript Transpiler")
    print("=" * 50)
    
    # Demo lexer
    demo_lexer()
    
    # Demo complete transpilation
    demo_transpiler()
    
    # Run examples
    run_examples()


if __name__ == "__main__":
    main()
