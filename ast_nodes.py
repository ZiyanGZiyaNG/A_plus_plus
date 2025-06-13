# ast_nodes.py

# 數值
class Number:
    def __init__(self, value):
        self.value = int(value)

# 變數
class Variable:
    def __init__(self, name):
        self.name = name

# 二元運算(+-*/)
class BinaryOp:
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

# 賦值(=)
class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

# 輸出
class Print:
    def __init__(self, expr):
        self.expr = expr

# 輸入
class Input:
    pass

# 定義陣列
class Array:
    def __init__(self, elements):
        self.elements = elements

# 陣列索引
class ArrayAccess:
    def __init__(self, name, index):
        self.name = name
        self.index = index

# 陣列數值改變
class ArrayAssign:
    def __init__(self, name, index, expr):
        self.name = name
        self.index = index
        self.expr = expr

# 物件操作
class MethodCall:
    def __init__(self, obj, method, arg):
        self.obj = obj
        self.method = method
        self.arg = arg

class PropertyAccess:
    def __init__(self, obj, prop):
        self.obj = obj
        self.prop = prop

# if 結構
class IfElse:
    def __init__(self, cond, then_body, else_body):
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

# while 結構
class While:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

# for 結構
class For:
    def __init__(self, var_name, start_expr, end_expr, body):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.body = body

# if/for/while 結構的判斷
class Block:
    def __init__(self, stmts):
        self.stmts = stmts

# 函數定義
class FunctionDef:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

# 函數呼叫
class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

# 函數的return
class Return:
    def __init__(self, expr):
        self.expr = expr
