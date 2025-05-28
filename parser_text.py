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
    elif line.startswith("int "):
        # int x = 5
        match = re.match(r"int (\w+) *= *(.*)", line)
        if match:
            name = match.group(1)
            expr = parse_expr(match.group(2))
            return Assign(name, expr)
    elif line.startswith("out("):
        # out(x + 1)
        match = re.match(r"out\((.*)\)", line)
        if match:
            expr = parse_expr(match.group(1))
            return Print(expr)
    elif line.startswith("if"):
        # if (x > 0) {
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
        # for (int i = 0, i < 10, i = i + 1) {
        match = re.match(r"for *\(int (\w+) *= *(\d+), *\1 *< *(\w+),.*\) *\{", line)
        if match:
            var = match.group(1)
            start = Number(int(match.group(2)))
            # 上界可變數或常數
            end_token = match.group(3)
            if end_token.isdigit():
                end = Number(int(end_token))
            else:
                end = Variable(end_token)
            return ("for", var, start, end)
    elif line == "}":
        return "end"
    else:
        return None

def parse_expr(expr):
    expr = expr.strip()
    if expr == "in()":
        return Input()
    # binary expression a + b or a >= b
    for op in ["+", "-", "*", "/", "%", "==", "!=", ">=", "<=", ">", "<"]:
        parts = expr.split(op)
        if len(parts) == 2:
            left = parse_expr(parts[0])
            right = parse_expr(parts[1])
            return BinaryOp(op, left, right)
    # number or variable
    if expr.isdigit():
        return Number(int(expr))
    else:
        return Variable(expr)

def parse_program(lines):
    stack = [Block([])]
    for raw_line in lines:
        stmt = parse_line(raw_line)
        if isinstance(stmt, Assign) or isinstance(stmt, Print):
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
