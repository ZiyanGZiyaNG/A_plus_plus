# ast_nodes.py

class Number:
    def __init__(self, value):
        self.value = int(value)

class Variable:
    def __init__(self, name):
        self.name = name

class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Print:
    def __init__(self, expr):
        self.expr = expr

class Input:
    pass

class Array:
    def __init__(self, elements):
        self.elements = elements

class ArrayAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index

class ArrayAssign:
    def __init__(self, name, index, expr):
        self.name = name
        self.index = index
        self.expr = expr

class MethodCall:
    def __init__(self, obj, method, arg):
        self.obj = obj
        self.method = method
        self.arg = arg

class PropertyAccess:
    def __init__(self, obj, prop):
        self.obj = obj
        self.prop = prop

class IfElse:
    def __init__(self, cond, then_body, else_body):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class While:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class For:
    def __init__(self, var_name, start_expr, end_expr, body):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body

class Block:
    def __init__(self, stmts):
        self.stmts = stmts
