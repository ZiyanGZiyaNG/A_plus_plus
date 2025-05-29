from parser_text import parse_program
from interpreter import run

code = '''

'''

ast = parse_program(code.strip().splitlines())
run(ast)
