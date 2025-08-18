"""
JavaScript code generator.

This module generates JavaScript code from our intermediate representation (IR).
"""

from typing import List
from ir import (
    Program, Stmt, Expr,
    VariableAssign, AugAssign, FunctionDef, Return, IfStmt, ForStmt, WhileStmt, ExprStmt,
    Name, Num, Str, Bool, Null, BinOp, UnaryOp, Subscript, Call, Compare, ListExpr
)


def gen_block_js(statements: List[Stmt], indent_level: int = 1) -> str:
    """Generate JavaScript code for a block of statements with proper indentation"""
    indent = '    ' * indent_level  # 4 spaces per indent level
    lines = []
    for stmt in statements:
        stmt_js = gen_stmt_js(stmt)  # Don't pass indent_level - we handle it here
        lines.append(indent + stmt_js)
    return '\n'.join(lines)


def gen_expr_js(expr: Expr) -> str:
    """Generate JavaScript code for expressions"""
    if isinstance(expr, Num):
        return str(expr.value)
    
    elif isinstance(expr, Str):
        # Escape quotes and return properly quoted string
        escaped = expr.value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    
    elif isinstance(expr, Bool):
        return "true" if expr.value else "false"
    
    elif isinstance(expr, Null):
        return "null"
    
    elif isinstance(expr, Name):
        return expr.id
    
    elif isinstance(expr, BinOp):
        left = gen_expr_js(expr.left)
        right = gen_expr_js(expr.right)
        # Convert Python power operator to JavaScript Math.pow
        if expr.op == '**':
            return f"Math.pow({left}, {right})"
        # Convert Python floor division to JavaScript Math.floor
        elif expr.op == '//':
            return f"Math.floor({left} / {right})"
        else:
            return f"({left} {expr.op} {right})"
    
    elif isinstance(expr, Call):
        func_js = gen_expr_js(expr.func)
        args_js = [gen_expr_js(arg) for arg in expr.args]
        # Handle print function specifically
        if isinstance(expr.func, Name) and expr.func.id == 'print':
            return f"console.log({', '.join(args_js)})"
        else:
            return f"{func_js}({', '.join(args_js)})"
    
    elif isinstance(expr, Compare):
        # Handle comparison operations
        if len(expr.ops) == 1 and len(expr.comparators) == 1:
            left_js = gen_expr_js(expr.left)
            op = expr.ops[0]
            right_js = gen_expr_js(expr.comparators[0])
            
            # Special handling for 'not in' operator
            if op == 'not in':
                return f"!({left_js} in {right_js})"
            else:
                return f"({left_js} {op} {right_js})"
        else:
            # Multiple comparisons like a < b < c
            # Convert to (a < b) && (b < c)
            parts = []
            current = expr.left
            for i, (op, comp) in enumerate(zip(expr.ops, expr.comparators)):
                left_js = gen_expr_js(current)
                right_js = gen_expr_js(comp)
                
                # Special handling for 'not in' operator in chained comparisons
                if op == 'not in':
                    parts.append(f"!({left_js} in {right_js})")
                else:
                    parts.append(f"({left_js} {op} {right_js})")
                current = comp
            return f"({' && '.join(parts)})"
    
    elif isinstance(expr, ListExpr):
        # Generate JavaScript array literal
        elts_js = [gen_expr_js(elt) for elt in expr.elts]
        return f"[{', '.join(elts_js)}]"
    
    elif isinstance(expr, UnaryOp):
        operand_js = gen_expr_js(expr.operand)
        # Special handling for 'not' operator
        if expr.op == '!':
            return f"!{operand_js}"
        else:
            return f"{expr.op}{operand_js}"
    
    elif isinstance(expr, Subscript):
        value_js = gen_expr_js(expr.value)
        index_js = gen_expr_js(expr.index)
        return f"{value_js}[{index_js}]"
    
    raise NotImplementedError(f"Unknown expression type: {type(expr)}")


def gen_stmt_js(stmt: Stmt) -> str:
    """Generate JavaScript code for statements """
    if isinstance(stmt, VariableAssign):
        value_js = gen_expr_js(stmt.value)
        return f"let {stmt.name} = {value_js};"
    
    elif isinstance(stmt, AugAssign):
        value_js = gen_expr_js(stmt.value)
        js_op = stmt.op
        if stmt.op == '**=':
            return f"{stmt.target} = Math.pow({stmt.target}, {value_js});"
        elif stmt.op == '//=':
            return f"{stmt.target} = Math.floor({stmt.target} / {value_js});"
        else:
            return f"{stmt.target} {js_op} {value_js};"
    
    elif isinstance(stmt, FunctionDef):
        args_js = ', '.join(stmt.args)
        body_js = gen_block_js(stmt.body, 1)  # Function body gets indent level 1
        return f"function {stmt.name}({args_js}) {{\n{body_js}\n}}"
    
    elif isinstance(stmt, Return):
        if stmt.value:
            value_js = gen_expr_js(stmt.value)
            return f"return {value_js};"
        else:
            return "return;"
    
    elif isinstance(stmt, IfStmt):
        test_js = gen_expr_js(stmt.test)
        body_js = gen_block_js(stmt.body, 1)  # If body gets indent level 1
        
        if stmt.orelse:
            # Check if orelse contains a single IfStmt (elif case)
            if len(stmt.orelse) == 1 and isinstance(stmt.orelse[0], IfStmt):
                # This is an elif - generate as "else if"
                elif_stmt = stmt.orelse[0]
                elif_js = gen_stmt_js(elif_stmt).replace("if", "else if", 1)
                return f"if ({test_js}) {{\n{body_js}\n}} {elif_js}"
            else:
                # Regular else clause
                orelse_js = gen_block_js(stmt.orelse, 1)  # Else body gets indent level 1
                return f"if ({test_js}) {{\n{body_js}\n}} else {{\n{orelse_js}\n}}"
        else:
            return f"if ({test_js}) {{\n{body_js}\n}}"
    
    elif isinstance(stmt, ForStmt):
        # Convert Python for loop to JavaScript for...of loop
        iter_js = gen_expr_js(stmt.iter)
        body_js = gen_block_js(stmt.body, 1)  # For body gets indent level 1
        
        # Handle range() function specifically
        if isinstance(stmt.iter, Call) and isinstance(stmt.iter.func, Name) and stmt.iter.func.id == 'range':
            if len(stmt.iter.args) == 1:
                # range(n) -> for (let i = 0; i < n; i++)
                end = gen_expr_js(stmt.iter.args[0])
                return f"for (let {stmt.target} = 0; {stmt.target} < {end}; {stmt.target}++) {{\n{body_js}\n}}"
            elif len(stmt.iter.args) == 2:
                # range(start, end) -> for (let i = start; i < end; i++)
                start = gen_expr_js(stmt.iter.args[0])
                end = gen_expr_js(stmt.iter.args[1])
                return f"for (let {stmt.target} = {start}; {stmt.target} < {end}; {stmt.target}++) {{\n{body_js}\n}}"
            elif len(stmt.iter.args) == 3:
                # range(start, end, step) -> for (let i = start; i < end; i += step)
                start = gen_expr_js(stmt.iter.args[0])
                end = gen_expr_js(stmt.iter.args[1])
                step = gen_expr_js(stmt.iter.args[2])
                return f"for (let {stmt.target} = {start}; {stmt.target} < {end}; {stmt.target} += {step}) {{\n{body_js}\n}}"
        else:
            # General for...of loop
            return f"for (let {stmt.target} of {iter_js}) {{\n{body_js}\n}}"
    
    elif isinstance(stmt, WhileStmt):
        test_js = gen_expr_js(stmt.test)
        body_js = gen_block_js(stmt.body, 1)  # While body gets indent level 1
        return f"while ({test_js}) {{\n{body_js}\n}}"
    
    elif isinstance(stmt, ExprStmt):
        # Expression statement
        expr_js = gen_expr_js(stmt.value)
        return f"{expr_js};"
    
    elif isinstance(stmt, Expr):
        # Legacy support - direct expression as statement
        expr_js = gen_expr_js(stmt)
        return f"{expr_js};"
    
    raise NotImplementedError(f"Unknown statement type: {type(stmt)}")


def gen_program_js(program: Program) -> str:
    """Generate JavaScript code for the entire program"""
    statements = []
    for stmt in program.body:
        stmt_js = gen_stmt_js(stmt)  # Top level statements don't get indented
        statements.append(stmt_js)
    
    return '\n'.join(statements)


def transpile_to_js(ir_program: Program) -> str:
    """Generate JavaScript code from IR program
    
    Args:
        ir_program: IR Program to transpile
        
    Returns:
        str: Generated JavaScript code
        
    Raises:
        NotImplementedError: If unsupported IR constructs are encountered
    """
    try:
        return gen_program_js(ir_program)
    except Exception as e:
        raise RuntimeError(f"Failed to generate JavaScript: {e}")


if __name__ == "__main__":
    from parser import parse_python_to_ir
    
    python_code = """
def greet(name):
    print("Hello, " + name)

x = 5
y = 10
z = 15

if x > y:
    print("x is greater than y")
elif x < y:
    print("x is less than y")
elif x == z:
    print("x equals z")
else:
    print("x equals y")

for i in range(3):
    print("Iteration", i)
    if i == 1:
        print("Middle iteration")

# Test 'in' and 'not in' operators
numbers = [1, 2, 3, 4, 5]
if x in numbers:
    print("x is in numbers")

if z not in numbers:
    print("z is not in numbers")

greet("World")
"""
    
    try:
        # Parse Python to IR
        ir_program = parse_python_to_ir(python_code)
        
        # Generate JavaScript from IR
        js_code = transpile_to_js(ir_program)
        
        print("Generated JavaScript:")
        print(js_code)
    except Exception as e:
        print(f"Error: {e}")
