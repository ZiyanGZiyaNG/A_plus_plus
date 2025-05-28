# interpreter.py

import operator
from ast_nodes import *

class Environment(dict):
    def get(self, name):
        return self[name]
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

def eval_expr(expr, env):
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, Variable):
        return env.get(expr.name)
    elif isinstance(expr, BinaryOp):
        return bin_ops[expr.op](eval_expr(expr.left, env), eval_expr(expr.right, env))
    else:
        raise Exception(f"Unknown expression type: {type(expr)}")

def exec_stmt(stmt, env):
    if isinstance(stmt, Assign):
        env.set(stmt.name, eval_expr(stmt.expr, env))
    elif isinstance(stmt, Print):
        print(eval_expr(stmt.expr, env))
    elif isinstance(stmt, IfElse):
        if eval_expr(stmt.cond, env):
            exec_block(stmt.then_body, env)
        else:
            exec_block(stmt.else_body, env)
    elif isinstance(stmt, While):
        while eval_expr(stmt.cond, env):
            exec_block(stmt.body, env)
    elif isinstance(stmt, For):
        start = eval_expr(stmt.start_expr, env)
        end = eval_expr(stmt.end_expr, env)
        for i in range(start, end):
            env.set(stmt.var_name, i)
            exec_block(stmt.body, env)
    else:
        raise Exception(f"Unknown statement type: {type(stmt)}")

def exec_block(block, env):
    for stmt in block.stmts:
        exec_stmt(stmt, env)
