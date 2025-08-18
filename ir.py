"""
Intermediate Representation (IR) definitions for the transpiler.

This module contains all the data classes that represent the abstract syntax tree
after parsing Python code but before generating the target language.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union, Optional


@dataclass
class Program:
    """Root node representing the entire program"""
    body: List[Stmt]


class Stmt:
    """Base class for all statement nodes"""
    pass


class Expr:
    """Base class for all expression nodes"""
    pass


# Statement nodes
@dataclass
class VariableAssign(Stmt):
    """Variable assignment: x = value"""
    name: str
    value: Expr


@dataclass
class AugAssign(Stmt):
    """Augmented assignment: x += value, x *= value"""
    target: str
    op: str
    value: Expr


@dataclass
class FunctionDef(Stmt):
    """Function definition: def name(args): body"""
    name: str
    args: list[str]
    body: List[Stmt]


@dataclass
class Return(Stmt):
    """Return statement: return value"""
    value: Optional[Expr]


@dataclass  
class IfStmt(Stmt):
    """If statement: if test: body else: orelse"""
    test: Expr
    body: List[Stmt]
    orelse: List[Stmt]  # Can contain another IfStmt for elif chains


@dataclass
class ForStmt(Stmt):
    """For loop: for target in iter: body"""
    target: str
    iter: Expr
    body: List[Stmt]


@dataclass
class WhileStmt(Stmt):
    """While loop: while test: body"""
    test: Expr
    body: List[Stmt]


@dataclass
class ExprStmt(Stmt):
    """Expression statement: just an expression"""
    value: Expr


# Expression nodes
@dataclass
class Name(Expr):
    """Variable reference: x"""
    id: str


@dataclass
class Num(Expr):
    """Numeric literal: 42, 3.14"""
    value: Union[int, float]


@dataclass
class Str(Expr):
    """String literal: "hello" """
    value: str


@dataclass
class Bool(Expr):
    """Boolean literal: True, False"""
    value: bool


@dataclass
class Null(Expr):
    """Null literal: None"""
    pass  


@dataclass
class BinOp(Expr):
    """Binary operation: left op right"""
    left: Expr
    op: str  
    right: Expr


@dataclass
class UnaryOp(Expr):
    """Unary operation: op operand ( -x, not x)"""
    op: str
    operand: Expr


@dataclass
class Subscript(Expr):
    """Subscript operation: value[index] ( arr[0])"""
    value: Expr
    index: Expr


@dataclass
class Call(Expr):
    """Function call: func(args)"""
    func: Expr
    args: List[Expr]


@dataclass
class Compare(Expr):
    """Comparison: left ops comparators"""
    left: Expr
    ops: List[str]
    comparators: List[Expr]


@dataclass
class ListExpr(Expr):
    """List literal: [1, 2, 3]"""
    elts: List[Expr]
