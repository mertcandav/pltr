# Copyright 2022 Mertcan Davulcu.
# Use of this source code is governed by a BSD 3-Clause
# license that can be found in the LICENSE file.

from lexer import Lexer
from ast import AST

# This string is the pseudo representation
# for source code read from file.
PSEUDO_SOURCE_CODE: str = """
123
123.5
x
hello
print
+ - * ^/ %
()
"""

if __name__ == "__main__":
	lexer = Lexer(PSEUDO_SOURCE_CODE)
	tokens = lexer.lex()
	if len(lexer.logs) > 0:
		print(lexer.logs)
		exit(0)
	for token in tokens:
		print(token.kind)
