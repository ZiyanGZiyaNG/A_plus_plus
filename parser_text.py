# parser_text.py
from ast_nodes import *
import re

def parse_line(line):
    line = line.strip()
    # 支援 # 或 -- 註解
    for comment_mark in ("#", "--"):
        if comment_mark in line:
            line = line.split(comment_mark)[0].strip()
    if line == "":
        return None
    # 陣列賦值：arr[2] = xxx
    match = re.match(r"(\w+)\[(.+)\] *= *(.*)", line)
    if match:
        name = match.group(1)
        idx = parse_expr(match.group(2))
        expr = parse_expr(match.group(3))
        return ArrayAssign(name, idx, expr)
    elif line.startswith("int "):
        # int arr = [1, 2, 3]
        match = re.match(r"int (\w+) *= *\[(.*)\]", line)
        if match:
            name = match.group(1)
            elems = [parse_expr(e.strip()) for e in match.group(2).split(",") if e.strip() != ""]
            return Assign(name, Array(elems))
        # int x = ...  (普通變數)
        match = re.match(r"int (\w+) *= *(.*)", line)
        if match:
            name = match.group(1)
            expr = parse_expr(match.group(2))
            return Assign(name, expr)
    elif line.startswith("out("):
        match = re.match(r"out\((.*)\)", line)
        if match:
            expr = parse_expr(match.group(1))
            return Print(expr)
    elif line.startswith("if"):
        match = re.match(r"if *\((.*)\) *\{", line)
        if match:
            cond = parse_expr(match.group(1))
            return ("if", cond)
    elif line.startswith("else"):
        return "else"
    elif line.startswith("while"):
        match = re.match(r"while *\((.*)\) *\{", line)
        if match:
            cond = parse_expr(match.group(1))
            return ("while", cond)
    elif line.startswith("for"):
        # for (int i = 0, i < xxx, i = i + 1) {
        match = re.match(r"for *\(int (\w+) *= *(.+), *\1 *< *(.+),.*\) *\{", line)
        if match:
            var = match.group(1)
            start = parse_expr(match.group(2))
            end = parse_expr(match.group(3))
            return ("for", var, start, end)
    elif line == "}":
        return "end"
    else:
        return None

def parse_expr(expr):
    expr = expr.strip()
    # 陣列動態建立 [1, 2, 3]
    if expr.startswith("[") and expr.endswith("]"):
        elems = [parse_expr(e.strip()) for e in expr[1:-1].split(",") if e.strip() != ""]
        return Array(elems)
    # arr[索引]
    match = re.match(r"(\w+)\[(.+)\]", expr)
    if match:
        return ArrayAccess(match.group(1), parse_expr(match.group(2)))
    # arr.increase(xxx) / arr.reduce()
    match = re.match(r"(\w+)\.(increase|reduce)\((.*)\)", expr)
    if match:
        obj = match.group(1)
        method = match.group(2)
        arg = parse_expr(match.group(3)) if method == "Increase" and match.group(3).strip() else None
        return MethodCall(obj, method, arg)
    # arr.length
    match = re.match(r"(\w+)\.length", expr)
    if match:
        return PropertyAccess(match.group(1), "length")
    # in()
    if expr == "in()":
        return Input()
    # 二元運算
    for op in ["+", "-", "*", "/", "%", "==", "!=", ">=", "<=", ">", "<"]:
        parts = expr.split(op)
        if len(parts) == 2:
            left = parse_expr(parts[0])
            right = parse_expr(parts[1])
            return BinaryOp(op, left, right)
    # 數字
    if expr.isdigit():
        return Number(int(expr))
    # 變數
    return Variable(expr)

def parse_program(lines):
    stack = [Block([])]
    for raw_line in lines:
        stmt = parse_line(raw_line)
        if isinstance(stmt, Assign) or isinstance(stmt, Print) or isinstance(stmt, ArrayAssign):
            stack[-1].stmts.append(stmt)
        elif isinstance(stmt, tuple) and stmt[0] == "if":
            new_block = Block([])
            stack[-1].stmts.append(IfElse(stmt[1], new_block, None))
            stack.append(new_block)
        elif stmt == "else":
            prev_if = None
            for s in reversed(stack[-2].stmts):
                if isinstance(s, IfElse) and s.else_body is None:
                    prev_if = s
                    break
            new_block = Block([])
            prev_if.else_body = new_block
            stack.append(new_block)
        elif isinstance(stmt, tuple) and stmt[0] == "while":
            new_block = Block([])
            stack[-1].stmts.append(While(stmt[1], new_block))
            stack.append(new_block)
        elif isinstance(stmt, tuple) and stmt[0] == "for":
            new_block = Block([])
            stack[-1].stmts.append(For(stmt[1], stmt[2], stmt[3], new_block))
            stack.append(new_block)
        elif stmt == "end":
            stack.pop()
    return stack[0]
