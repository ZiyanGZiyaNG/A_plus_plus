# interpreter.py

import operator
import os
from ast_nodes import *

# ✅ 定義桌面上的 output.txt 路徑
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "output.txt")

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Environment(dict):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def get(self, name):
        if name in self:
            return self[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Undefined variable: {name}")

    def set(self, name, value):
        self[name] = value

bin_ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "%": operator.mod,
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge
}

def eval_expr(expr, env, funcs):
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, Variable):
        return env.get(expr.name)
    elif isinstance(expr, BinaryOp):
        return bin_ops[expr.op](eval_expr(expr.left, env, funcs), eval_expr(expr.right, env, funcs))
    elif isinstance(expr, FunctionCall):
        func_def = funcs.get(expr.name)
        if not func_def:
            raise Exception(f"Function not defined: {expr.name}")
        if len(func_def.params) != len(expr.args):
            raise Exception(f"Argument mismatch for function {expr.name}")
        new_env = Environment()
        for param, arg in zip(func_def.params, expr.args):
            new_env.set(param, eval_expr(arg, env, funcs))
        try:
            exec_block(func_def.body, new_env, funcs)
        except ReturnException as e:
            return e.value
        return None
    else:
        raise Exception(f"Unknown expression type: {type(expr)}")

def exec_stmt(stmt, env, funcs):
    if isinstance(stmt, Assign):
        env.set(stmt.name, eval_expr(stmt.expr, env, funcs))
    elif isinstance(stmt, Print):
        val = eval_expr(stmt.expr, env, funcs)
        with open(desktop_path, "a", encoding="utf-8") as f:
            f.write(str(val) + "\n")
    elif isinstance(stmt, IfElse):
        if eval_expr(stmt.cond, env, funcs):
            exec_block(stmt.then_body, env, funcs)
        elif stmt.else_body is not None:
            exec_block(stmt.else_body, env, funcs)
    elif isinstance(stmt, While):
        while eval_expr(stmt.cond, env, funcs):
            exec_block(stmt.body, env, funcs)
    elif isinstance(stmt, For):
        start = eval_expr(stmt.start_expr, env, funcs)
        end = eval_expr(stmt.end_expr, env, funcs)
        for i in range(start, end):
            env.set(stmt.var_name, i)
            exec_block(stmt.body, env, funcs)
    elif isinstance(stmt, Return):
        val = eval_expr(stmt.expr, env, funcs)
        raise ReturnException(val)
    elif isinstance(stmt, FunctionDef):
        funcs[stmt.name] = stmt
    else:
        raise Exception(f"Unknown statement type: {type(stmt)}")

def exec_block(block, env, funcs):
    for stmt in block.stmts:
        exec_stmt(stmt, env, funcs)

def run(ast):
    # ✅ 每次執行前清空桌面的 output.txt
    open(desktop_path, "w", encoding="utf-8").close()

    env = Environment()
    funcs = {}

    for stmt in ast.stmts:
        if isinstance(stmt, FunctionDef):
            funcs[stmt.name] = stmt

    for stmt in ast.stmts:
        if not isinstance(stmt, FunctionDef):
            exec_stmt(stmt, env, funcs)
