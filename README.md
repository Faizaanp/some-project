# Python to JavaScript Transpiler

A modular transpiler that converts Python code to JavaScript, featuring lexical analysis, parsing, intermediate representation (IR), and code generation with file output capabilities.

## Features

- **Complete Python-to-JavaScript transpilation**
- **Modular architecture** (lexer, parser, IR, codegen)
- **File output** - Generated JavaScript is saved to `.js` files
- **Command-line interface** for individual file transpilation
- **Comprehensive testing** with unit tests
- **Support for**: 
  - Functions, variables, conditionals, loops
  - Arithmetic and logical expressions
  - **NEW**: Unary operators (`-x`, `+x`, `not x`)
  - **NEW**: Augmented assignments (`x += 1`, `x *= 2`, etc.)
  - **NEW**: While loops
  - **NEW**: List indexing (`arr[0]`)
  - **NEW**: Better error messages
  - Lists, comparisons, boolean operations

## Quick Start

### Run Full Demo
```bash
python main.py
```
This will:
- Demo the lexer functionality
- Transpile example code and save to `outputs/` directory
- Process all files in the `examples/` directory

### Transpile Individual Files
```bash
# Transpile a single file
python transpile.py examples/example1.py

# Transpile to custom output directory
python transpile.py my_script.py custom_output
```

### Programmatic Usage
```python
from main import transpile_python_to_js, save_js_output

# Transpile Python code
python_code = """
def greet(name):
    print("Hello, " + name)
greet("World")
"""

js_code = transpile_python_to_js(python_code)
filepath = save_js_output(js_code, "my_script.py", "Example script")
print(f"Saved to: {filepath}")
```

## Output Files

Generated JavaScript files are saved in the `outputs/` directory with:
- **Timestamp-based naming** to avoid conflicts
- **Header comments** with metadata (source file, transpilation date, description)
- **Clean, readable JavaScript** with proper formatting and indentation

Example output file: `outputs/example1_20250816_200719.js`

## Architecture

- `lexer.py` - Tokenization with INDENT/DEDENT support
- `ir.py` - Intermediate representation nodes
- `parser.py` - AST-to-IR transformation
- `codegen_js.py` - JavaScript code generation
- `main.py` - Main application with file output
- `transpile.py` - Command-line utility

## Language Support

| Python Feature | JavaScript Output | Status |
|---------------|------------------|---------|
| `def func():` | `function func() {}` | ✅ |
| `x = 5` | `let x = 5;` | ✅ |
| `x += 1` | `x += 1;` | ✅ **NEW** |
| `x //= 2` | `x = Math.floor(x / 2);` | ✅ **NEW** |
| `if/elif/else` | `if/else if/else` | ✅ |
| `while condition:` | `while (condition) {}` | ✅ **NEW** |
| `for i in range(n):` | `for (let i = 0; i < n; i++)` | ✅ |
| `print("hello")` | `console.log("hello")` | ✅ |
| `x == y` | `x === y` | ✅ |
| `x in list` | `x in list` | ✅ |
| `not x` | `!x` | ✅ **NEW** |
| `-x`, `+x` | `-x`, `+x` | ✅ **NEW** |
| `arr[0]` | `arr[0]` | ✅ **NEW** |
| `[1, 2, 3]` | `[1, 2, 3]` | ✅ |
| `True`, `False` | `true`, `false` | ✅ **NEW** |

## Testing

```bash
python test_transpiler.py     # Run integration tests
python test_new_features.py   # Test new features (unary ops, while loops, etc.)
python main.py                # Run full demo with file output
```