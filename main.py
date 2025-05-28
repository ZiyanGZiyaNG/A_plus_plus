# main.py
import os
from parser_text import parse_program
from compiler_custom import compile_to_custom_code

code = """
-- 會要求你輸入一個數字

"""

desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, "output.txt")

ast = parse_program(code.strip().splitlines())
compile_to_custom_code(ast, output_file)
