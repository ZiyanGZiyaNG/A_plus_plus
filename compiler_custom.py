# compiler_custom.py
from ast_nodes import *

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

def compile_to_custom_code(ast, filename):
    outputs = []
    eval_block(ast, {}, {}, outputs)
    with open(filename, "w", encoding="utf-8") as f:
        for line in outputs:
            f.write(str(line) + "\n")

def eval_expr(expr, env, funcs):
    if isinstance(expr, Number):
        return expr.value
    elif isinstance(expr, Variable):
        return env[expr.name]
    elif isinstance(expr, Input):
        return int(input())
    elif isinstance(expr, Array):
        return [eval_expr(e, env, funcs) for e in expr.elements]
    elif isinstance(expr, ArrayAccess):
        arr = env[expr.name]
        idx = eval_expr(expr.index, env, funcs)
        return arr[idx]
    elif isinstance(expr, MethodCall):
        arr = env[expr.obj]
        if expr.method == "Increase":
            val = eval_expr(expr.arg, env, funcs)
            arr.append(val)
            return None
        elif expr.method == "Reduce":
            if len(arr) == 0:
                raise Exception("Reduce() on empty array!")
            arr.pop()
            return None
        else:
            raise Exception(f"Unknown method: {expr.method}")
    elif isinstance(expr, PropertyAccess):
        arr = env[expr.obj]
        if expr.prop == "length":
            return len(arr)
        else:
            raise Exception(f"Unknown property: {expr.prop}")
    elif isinstance(expr, BinaryOp):
        left = eval_expr(expr.left, env, funcs)
        right = eval_expr(expr.right, env, funcs)
        return eval_bin_op(expr.op, left, right)
    elif isinstance(expr, FunctionCall):
        func = funcs.get(expr.name)
        if not func:
            raise Exception(f"Function not defined: {expr.name}")
        if len(func.params) != len(expr.args):
            raise Exception(f"Argument mismatch for function {expr.name}")
        new_env = {}
        for p, a in zip(func.params, expr.args):
            new_env[p] = eval_expr(a, env, funcs)
        try:
            eval_block(func.body, new_env, funcs, [])
        except ReturnException as e:
            return e.value
        return None
    else:
        raise Exception(f"Unknown expr: {expr}")

def eval_bin_op(op, left, right):
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
    raise Exception(f"Unknown binary operator: {op}")

def eval_block(block, env, funcs, outputs):
    for stmt in block.stmts:
        eval_stmt(stmt, env, funcs, outputs)

def eval_stmt(stmt, env, funcs, outputs):
    if isinstance(stmt, Assign):
        env[stmt.name] = eval_expr(stmt.expr, env, funcs)
    elif isinstance(stmt, ArrayAssign):
        arr = env[stmt.name]
        idx = eval_expr(stmt.index, env, funcs)
        val = eval_expr(stmt.expr, env, funcs)
        if idx >= len(arr):
            arr.extend([0] * (idx - len(arr) + 1))
        arr[idx] = val
    elif isinstance(stmt, Print):
        val = eval_expr(stmt.expr, env, funcs)
        if val is not None:
            outputs.append(val)
    elif isinstance(stmt, IfElse):
        if eval_expr(stmt.cond, env, funcs):
            eval_block(stmt.then_body, dict(env), funcs, outputs)
        elif stmt.else_body:
            eval_block(stmt.else_body, dict(env), funcs, outputs)
    elif isinstance(stmt, While):
        while eval_expr(stmt.cond, env, funcs):
            eval_block(stmt.body, dict(env), funcs, outputs)
    elif isinstance(stmt, For):
        start = eval_expr(stmt.start_expr, env, funcs)
        end = eval_expr(stmt.end_expr, env, funcs)
        for i in range(start, end):
            env[stmt.var_name] = i
            eval_block(stmt.body, dict(env), funcs, outputs)
    elif isinstance(stmt, Return):
        val = eval_expr(stmt.expr, env, funcs)
        raise ReturnException(val)
    elif isinstance(stmt, FunctionDef):
        funcs[stmt.name] = stmt
    else:
        raise Exception(f"Unknown stmt: {stmt}")
