"""
Python AST to IR transformer.

This module converts Python AST nodes to our intermediate representation (IR).
"""

import ast
from typing import List
from ir import (
    Program, Stmt, Expr,
    VariableAssign, FunctionDef, Return, IfStmt, ForStmt, ExprStmt,
    Name, Num, Str, Bool, Null, BinOp, Call, Compare, ListExpr
)


# Operator mappings
BIN_OPS = {
    ast.Add: '+',
    ast.Sub: '-',
    ast.Mult: '*',
    ast.Div: '/',
    ast.Mod: '%',
    ast.Pow: '**',
    ast.FloorDiv: '//',
    ast.BitAnd: '&',
    ast.BitOr: '|',
    ast.BitXor: '^',
    ast.LShift: '<<',
    ast.RShift: '>>'
}

COMPARE_OPS = {
    ast.Eq: '===',
    ast.NotEq: '!==',
    ast.Lt: '<',
    ast.LtE: '<=',
    ast.Gt: '>',
    ast.GtE: '>=',
    ast.Is: '===',
    ast.IsNot: '!==',
    ast.In: 'in',
    ast.NotIn: 'not in'  # Special handling in codegen
}


def py_exp_to_ir(node: ast.AST) -> Expr:
    """Convert Python AST expression to IR expression"""
    if isinstance(node, ast.Constant):
        v = node.value
        if isinstance(v, (int, float)):
            return Num(value=v)
        elif isinstance(v, str):
            return Str(value=v)
        elif isinstance(v, bool):
            return Bool(value=v)
        elif v is None:
            return Null()
        
    elif isinstance(node, ast.BinOp):
        opType = type(node.op)
        if opType in BIN_OPS:
            return BinOp(
                left=py_exp_to_ir(node.left),
                op=BIN_OPS[opType],
                right=py_exp_to_ir(node.right)
            )
        else:
            raise NotImplementedError(f"Unsupported operator: {node.op}")
        
    elif isinstance(node, ast.Name):
        return Name(id=node.id)
    
    elif isinstance(node, ast.Call):
        return Call(
            func=py_exp_to_ir(node.func),
            args=[py_exp_to_ir(arg) for arg in node.args]
        )
    
    elif isinstance(node, ast.Compare):
        ops = [COMPARE_OPS[type(op)] for op in node.ops]
        comparators = [py_exp_to_ir(comp) for comp in node.comparators]
        return Compare(
            left=py_exp_to_ir(node.left),
            ops=ops,
            comparators=comparators
        )
    
    elif isinstance(node, ast.List):
        elts = [py_exp_to_ir(elt) for elt in node.elts]
        return ListExpr(elts=elts)
    
    raise NotImplementedError(f"Unknown AST expression node: {type(node)}")


def py_stmt_to_ir(node: ast.AST) -> Stmt:
    """Convert Python AST statement to IR statement"""
    if isinstance(node, ast.Assign):
        targets = [target.id for target in node.targets if isinstance(target, ast.Name)]
        if len(targets) != 1:
            raise NotImplementedError("Multiple assignment targets are not supported.")
        return VariableAssign(name=targets[0], value=py_exp_to_ir(node.value))
    
    elif isinstance(node, ast.FunctionDef):
        args = [arg.arg for arg in node.args.args]
        body = [py_stmt_to_ir(stmt) for stmt in node.body]
        return FunctionDef(name=node.name, args=args, body=body)
    
    elif isinstance(node, ast.Return):
        value = py_exp_to_ir(node.value) if node.value else None
        return Return(value=value)
    
    elif isinstance(node, ast.If):
        test = py_exp_to_ir(node.test)
        body = [py_stmt_to_ir(stmt) for stmt in node.body]
        orelse = [py_stmt_to_ir(stmt) for stmt in node.orelse] if node.orelse else []
        return IfStmt(test=test, body=body, orelse=orelse)
    
    elif isinstance(node, ast.For):
        if not isinstance(node.target, ast.Name):
            raise NotImplementedError("Only simple variable targets supported in for loops")
        target = node.target.id
        iter_expr = py_exp_to_ir(node.iter)
        body = [py_stmt_to_ir(stmt) for stmt in node.body]
        return ForStmt(target=target, iter=iter_expr, body=body)
    
    elif isinstance(node, ast.Expr):
        # Expression statement - wrap in ExprStmt
        return ExprStmt(value=py_exp_to_ir(node.value))
    
    raise NotImplementedError(f"Unknown AST statement node: {type(node)}")


def py_module_to_ir(module: ast.Module) -> Program:
    """Convert Python AST module to IR Program"""
    body = []
    for node in module.body:
        ir_stmt = py_stmt_to_ir(node)
        body.append(ir_stmt)
    return Program(body=body)


def parse_python_to_ir(python_code: str) -> Program:
    """Parse Python source code to IR
    
    Args:
        python_code: Python source code as string
        
    Returns:
        Program: IR representation of the code
        
    Raises:
        SyntaxError: If the Python code is invalid
        NotImplementedError: If unsupported constructs are used
    """
    try:
        tree = ast.parse(python_code)
        return py_module_to_ir(tree)
    except SyntaxError as e:
        raise SyntaxError(f"Invalid Python syntax: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to parse Python code: {e}")
