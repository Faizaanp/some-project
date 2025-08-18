# Python to JavaScript Transpiler

A comprehensive, modular transpiler that converts Python code to JavaScript with advanced language feature support, featuring lexical analysis, parsing, intermediate representation (IR), and clean code generation with file output capabilities.

## 🚀 Features

- **Complete Python-to-JavaScript transpilation** with modern syntax support
- **Modular architecture** (lexer, parser, IR, codegen) for extensibility
- **File output system** - Generated JavaScript saved to timestamped `.js` files
- **Command-line interface** for individual file transpilation
- **Comprehensive testing suite** with unit and integration tests
- **Advanced language support**: 
  - ✅ Functions, variables, conditionals, loops
  - ✅ Arithmetic and logical expressions
  - ✅ **Unary operators** (`-x`, `+x`, `not x`)
  - ✅ **Augmented assignments** (`x += 1`, `x *= 2`, `x //= 3`, etc.)
  - ✅ **While loops** with proper condition handling
  - ✅ **List indexing** (`arr[0]`, `matrix[i][j]`)
  - ✅ **Boolean literals** (`True`/`False` → `true`/`false`)
  - ✅ **Improved error reporting** with helpful messages
  - ✅ Lists, comparisons, nested expressions

## 🎯 Quick Start

### Full Demo & Examples
```bash
python main.py
```
**What this does:**
- Transpiles all example files in the `examples/` directory
- Saves generated JavaScript to `outputs/` with timestamps
- Shows transpilation status and file locations
- Demonstrates all supported language features

### Individual File Transpilation
```bash
# Transpile a single file
python transpile.py examples/example1.py

# Transpile to custom output directory
python transpile.py my_script.py custom_output

# View help
python transpile.py --help
```

### Programmatic API
```python
from main import transpile_python_to_js, save_js_output

# Basic transpilation
python_code = """
def calculate(x, y):
    result = x * y
    while result > 100:
        result //= 2
    return result

print("Result:", calculate(15, 8))
"""

js_code = transpile_python_to_js(python_code)
filepath = save_js_output(js_code, "calculation.py", "Math example")
print(f"✅ Saved to: {filepath}")
```
```

## 📁 Output Files

Generated JavaScript files are saved in the `outputs/` directory with:
- **Timestamp-based naming** (`example1_20250818_121657.js`) to prevent conflicts
- **Header comments** with metadata (source file, transpilation date, description)
- **Clean, readable JavaScript** with proper formatting and indentation
- **Working code** that can be executed with Node.js or in browsers

**Example output structure:**
```
outputs/
├── example1_20250818_121657.js
├── example2_20250818_121657.js
├── example5_20250818_121657.js  // Advanced features demo
└── my_custom_script_20250818_121700.js
```

## 🏗️ Architecture

| Component | Purpose | Key Features |
|-----------|---------|-------------|
| `lexer.py` | Tokenization | INDENT/DEDENT support, multi-line strings |
| `ir.py` | Intermediate Representation | Type-safe AST nodes |
| `parser.py` | AST→IR transformation | Python AST to custom IR |
| `codegen_js.py` | JavaScript generation | Clean, readable output |
| `main.py` | Main application | File output, batch processing |
| `transpile.py` | CLI utility | Single-file transpilation |

## 📋 Language Support Matrix

| Python Feature | JavaScript Output | Status | Notes |
|---------------|------------------|---------|-------|
| **Basic Constructs** |
| `def func():` | `function func() {}` | ✅ | Full function support |
| `x = 5` | `let x = 5;` | ✅ | Variable declarations |
| `return value` | `return value;` | ✅ | Return statements |
| **Operators** |
| `x += 1` | `x += 1;` | ✅ | All augmented assignments |
| `x //= 2` | `x = Math.floor(x / 2);` | ✅ | Floor division conversion |
| `x **= 3` | `x = Math.pow(x, 3);` | ✅ | Power operator conversion |
| `not x` | `!x` | ✅ | Logical negation |
| `-x`, `+x` | `-x`, `+x` | ✅ | Unary operators |
| **Control Flow** |
| `if/elif/else` | `if/else if/else` | ✅ | Conditional statements |
| `while condition:` | `while (condition) {}` | ✅ | While loops |
| `for i in range(n):` | `for (let i = 0; i < n; i++)` | ✅ | Range-based for loops |
| **Data Structures** |
| `[1, 2, 3]` | `[1, 2, 3]` | ✅ | List literals |
| `arr[0]` | `arr[0]` | ✅ | List/array indexing |
| `x in list` | `x in list` | ✅ | Membership testing |
| **Built-ins** |
| `print("hello")` | `console.log("hello")` | ✅ | Print function |
| `True`, `False` | `true`, `false` | ✅ | Boolean literals |
| `None` | `null` | ✅ | Null values |
| **Comparisons** |
| `x == y` | `x === y` | ✅ | Equality (strict) |
| `x != y` | `x !== y` | ✅ | Inequality (strict) |
| `x < y` | `x < y` | ✅ | All comparison operators |

## 🧪 Testing & Validation

```bash
# Run all test suites
python test_transpiler.py         # Core integration tests (8 tests)
python test_new_features.py       # Advanced features tests (6 tests)

# Test individual examples
python transpile.py examples/example1.py  # Basic functions
python transpile.py examples/example2.py  # Conditionals
python transpile.py examples/example3.py  # Loops
python transpile.py examples/example4.py  # Complex functions
python transpile.py examples/example5.py  # Advanced features

# Full demo with all examples
python main.py

# Verify generated JavaScript works
node outputs/example1_TIMESTAMP.js
```

**Test Coverage:**
- ✅ **14 total tests** across all features
- ✅ **5 example files** demonstrating real-world usage
- ✅ **JavaScript execution validation** - all outputs run in Node.js
- ✅ **Error handling** with helpful messages

## 🔄 Example Transpilation

### Input (Python)
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

numbers = [5, 8, 13]
for num in numbers:
    result = fibonacci(num)
    if result > 50:
        print("Large result:", result)
    else:
        print("Small result:", result)
```

### Output (JavaScript)
```javascript
function fibonacci(n) {
    if ((n <= 1)) {
        return n;
    }
    return (fibonacci((n - 1)) + fibonacci((n - 2)));
}
let numbers = [5, 8, 13];
for (let num of numbers) {
    let result = fibonacci(num);
    if ((result > 50)) {
        console.log("Large result:", result);
    } else {
        console.log("Small result:", result);
    }
}
```

## 🚧 Future Roadmap

### Planned Features
- **Function defaults** - `def func(x=10):`
- **Tuples** - `(1, 2, 3)`
- **Dictionaries** - `{"key": "value"}`
- **Method calls** - `obj.method()`
- **Classes** - Basic OOP support
- **Exception handling** - `try/except`
- **List comprehensions** - `[x*2 for x in range(10)]`
- **Lambda functions** - `lambda x: x*2`

### Contributing
This is an educational transpiler project perfect for:
- Learning compiler/transpiler concepts
- Understanding AST transformations
- Exploring language design
- Contributing new language features

## 📊 Project Status: **Production Ready** ✅

The transpiler successfully handles a **comprehensive subset of Python** and produces **clean, executable JavaScript**. Perfect for educational use, simple scripts, and demonstrating transpilation concepts.

**Statistics:**
- 🎯 **20+ Python language features** supported
- 📝 **5 comprehensive examples** included
- 🧪 **14 automated tests** ensuring reliability
- 📁 **Modular architecture** for easy extension