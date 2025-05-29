# parser_text.py
from ast_nodes import *
import re

def parse_line(line):
    line = line.strip()
    for comment_mark in ("#", "--"):
        if comment_mark in line:
            line = line.split(comment_mark)[0].strip()
    if line == "":
        return None

    # 陣列賦值: arr[idx] = expr
    match = re.match(r"(\w+)\[(.+)\] *= *(.*)", line)
    if match:
        name = match.group(1)
        idx = parse_expr(match.group(2))
        expr = parse_expr(match.group(3))
        return ArrayAssign(name, idx, expr)

    # int 宣告與賦值
    if line.startswith("int "):
        match = re.match(r"int (\w+) *= *\[(.*)\]", line)
        if match:
            name = match.group(1)
            elems = [parse_expr(e.strip()) for e in match.group(2).split(",") if e.strip()]
            return Assign(name, Array(elems))
        match = re.match(r"int (\w+) *= *(.*)", line)
        if match:
            return Assign(match.group(1), parse_expr(match.group(2)))

    # 輸出 out(expr)
    if line.startswith("out("):
        match = re.match(r"out\((.*)\)", line)
        if match:
            return Print(parse_expr(match.group(1)))

    # return expr
    if line.startswith("return"):
        match = re.match(r"return (.+)", line)
        if match:
            return Return(parse_expr(match.group(1)))

    # func 定義
    if line.startswith("func "):
        match = re.match(r"func (\w+)\((.*?)\) *\{", line)
        if match:
            name = match.group(1)
            params = [p.strip() for p in match.group(2).split(",") if p.strip()]
            return ("func", name, params)

    # if 條件
    if line.startswith("if"):
        match = re.match(r"if *\((.*)\) *\{", line)
        if match:
            return ("if", parse_expr(match.group(1)))

    # else 區塊
    if line == "else":
        return "else"

    # while
    if line.startswith("while"):
        match = re.match(r"while *\((.*)\) *\{", line)
        if match:
            return ("while", parse_expr(match.group(1)))

    # for 迴圈
    if line.startswith("for"):
        match = re.match(r"for *\(int (\w+) *= *(.+), *\1 *< *(.+),.*\) *\{", line)
        if match:
            var, start, end = match.group(1), match.group(2), match.group(3)
            return ("for", var, parse_expr(start), parse_expr(end))

    # 區塊結束
    if line == "}":
        return "end"

    # 其他表達式
    return parse_expr(line)

def parse_expr(expr):
    expr = expr.strip()
    if expr.startswith("[") and expr.endswith("]"):
        elems = [e.strip() for e in expr[1:-1].split(",") if e.strip()]
        return Array([parse_expr(e) for e in elems])

    match = re.match(r"(\w+)\[(.+)\]", expr)
    if match:
        return ArrayAccess(match.group(1), parse_expr(match.group(2)))

    match = re.match(r"(\w+)\.(increase|reduce)\((.*)\)", expr)
    if match:
        obj, method, arg = match.group(1), match.group(2), match.group(3)
        return MethodCall(obj, method, parse_expr(arg) if arg.strip() else None)

    match = re.match(r"(\w+)\.length", expr)
    if match:
        return PropertyAccess(match.group(1), "length")

    match = re.match(r"(\w+)\((.*)\)", expr)
    if match:
        name, args = match.group(1), match.group(2)
        arg_list = [a.strip() for a in args.split(",") if a.strip()]
        return FunctionCall(name, [parse_expr(a) for a in arg_list])

    if expr == "in()":
        return Input()

    for op in ["+","-","*","/","%","==","!=" ,">=","<=",">","<"]:
        parts = expr.split(op)
        if len(parts) == 2:
            return BinaryOp(op, parse_expr(parts[0]), parse_expr(parts[1]))

    if expr.isdigit():
        return Number(int(expr))

    return Variable(expr)

def parse_program(lines):
    stack = [Block([])]
    for raw_line in lines:
        stmt = parse_line(raw_line)
        if stmt is None:
            continue

        if isinstance(stmt, (Assign, Print, ArrayAssign, Return)):
            stack[-1].stmts.append(stmt)
        elif isinstance(stmt, tuple) and stmt[0] == "if":
            new_block = Block([])
            stack[-1].stmts.append(IfElse(stmt[1], new_block, None))
            stack.append(new_block)
        elif stmt == "else":
            found = False
            for level in reversed(stack):
                for s in reversed(level.stmts):
                    if isinstance(s, IfElse) and s.else_body is None:
                        new_block = Block([])
                        s.else_body = new_block
                        stack.append(new_block)
                        found = True
                        break
                if found:
                    break
            if not found:
                raise Exception("else without matching if")
        elif isinstance(stmt, tuple) and stmt[0] == "while":
            new_block = Block([])
            stack[-1].stmts.append(While(stmt[1], new_block))
            stack.append(new_block)
        elif isinstance(stmt, tuple) and stmt[0] == "for":
            new_block = Block([])
            stack[-1].stmts.append(For(stmt[1], stmt[2], stmt[3], new_block))
            stack.append(new_block)
        elif isinstance(stmt, tuple) and stmt[0] == "func":
            new_block = Block([])
            stack[-1].stmts.append(FunctionDef(stmt[1], stmt[2], new_block))
            stack.append(new_block)
        elif stmt == "end":
            stack.pop()

    return stack[0]
