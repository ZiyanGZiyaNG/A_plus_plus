# compiler_custom.py
from ast_nodes import *

def compile_to_custom_code(ast, filename):
    outputs = []
    eval_block(ast, {}, outputs)
    with open(filename, "w", encoding="utf-8") as f:
        for line in outputs:
            f.write(str(line) + "\n")

def eval_expr(expr, env):
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, Variable):
        return env[expr.name]
    elif isinstance(expr, Input):
        return int(input())  # 支援輸入
    elif isinstance(expr, BinaryOp):
        left = eval_expr(expr.left, env)
        right = eval_expr(expr.right, env)
        op = expr.op
        if op == "+": return left + right
        if op == "-": return left - right
        if op == "*": return left * right
        if op == "/": return left // right
        if op == "%": return left % right
        if op == "==": return left == right
        if op == "!=": return left != right
        if op == ">=": return left >= right
        if op == "<=": return left <= right
        if op == ">": return left > right
        if op == "<": return left < right
    else:
        raise Exception(f"Unknown expr: {expr}")

def eval_block(block, env, outputs):
    for stmt in block.stmts:
        eval_stmt(stmt, env, outputs)

def eval_stmt(stmt, env, outputs):
    if isinstance(stmt, Assign):
        env[stmt.name] = eval_expr(stmt.expr, env)
    elif isinstance(stmt, Print):
        outputs.append(eval_expr(stmt.expr, env))
    elif isinstance(stmt, IfElse):
        if eval_expr(stmt.cond, env):
            eval_block(stmt.then_body, env.copy(), outputs)
        elif stmt.else_body:
            eval_block(stmt.else_body, env.copy(), outputs)
    elif isinstance(stmt, While):
        while eval_expr(stmt.cond, env):
            eval_block(stmt.body, env.copy(), outputs)
    elif isinstance(stmt, For):
        var = stmt.var_name
        start = eval_expr(stmt.start_expr, env)
        end = eval_expr(stmt.end_expr, env)
        for i in range(start, end):
            env[var] = i
            eval_block(stmt.body, env.copy(), outputs)
    else:
        raise Exception(f"Unknown stmt: {stmt}")
