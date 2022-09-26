# Copyright 2022 Mertcan Davulcu.
# Use of this source code is governed by a BSD 3-Clause
# license that can be found in the LICENSE file.

from parser import *
from tokens import *
from lexer import *

# This string is the pseudo representation
# for source code read from file.
PSEUDO_SOURCE_CODE = """
x = 20 + 4
print ((x + 20) * 2) + 5
"""

# A variable.
class Variable:
	def __init__(self, identifier: str, data: float | int) -> None:
		self.identifier = identifier
		self.data = data

# List of variables.
variables: list[Variable] = []

# Find variable by identifier.
# Returns variable if exist variable in given identifier, returns if not.
def find_variable(identifier: str) -> Variable | None:
	for var in variables:
		if var.identifier == identifier:
			return var
	return None

# Evaluate single expression.
def evaluate_single(op: BinopExpr, print_steps=False) -> float | int | None:
	x = 0
	# Identifier.
	if op.data[0] == '_' or op.data[0].isalpha():
		var = find_variable(op.data)
		if var is None:
			print("\rvariable is not exist in this indentifier: " + op.data)
			return None
		x = var.data
	elif "." in op.data:
		x = float(op.data)
	else:
		x = int(op.data)
	if print_steps:
		print(x, end="")
	return x

# Evaluate binary operation expression.
def evaluate_binary(op: BinaryOp, print_steps=False) -> float | int | None:
	if print_steps:
		print("(", end="")
	l = evaluate(op.left, print_steps)
	if l is None:
		return None
	if print_steps:
		print(" " + op.operator, end=" ")
	r = evaluate(op.right, print_steps)
	if r is None:
		return None
	if print_steps:
		print(") = ", end="")

	# Solve and return result.
	x = 0
	if op.operator == "+":
		x = l + r
	if op.operator == "-":
		x = l - r
	if op.operator == "*":
		x = l * r
	if op.operator == "/":
		x = l / r
	if op.operator == "^":
		x = l ** r
	if op.operator == "%":
		x = l % r

	# Cast to integer if left and right integer.
	if type(x) is float and type(l) is int and type(r) is int:
		x = int(x)

	return x

# Evaluate expression.
def evaluate(op: BinaryOp | BinopExpr, print_steps=False) -> float | int | None:
	# Single expression.
	if type(op) is BinopExpr:
		return evaluate_single(op, print_steps)
	
	x = evaluate_binary(op, print_steps)
	if print_steps and x is not None:
		print(x, end="")
	return x

# Interpret expression node.
def interpret_expr(expr: BinaryOp | BinopExpr) -> None:
	x = evaluate(expr)
	if x is not None:
		print(x)

# Interpret print statement node.
def interpret_print(op: PrintOp) -> None:
	x = evaluate(op.expr, print_steps=True)
	if x is not None:
		print()

# Interpret assignment statement node.
def interpret_assignment(op: AssignmentOp) -> None:
	expr = evaluate(op.expr)
	var = find_variable(op.identifier)
	# Not exist, create new.
	if var is None:
		var = Variable(op.identifier, expr)
		variables.append(var)
	else:
		var.data = expr

# Interpreter AST node.
def interpret_node(node) -> None:
	if node is None:
		return
	t = type(node)
	if t is BinaryOp or t is BinopExpr:
		interpret_expr(node)
	elif t is PrintOp:
		interpret_print(node)
	elif t is AssignmentOp:
		interpret_assignment(node)

if __name__ == "__main__":
	lexer = Lexer(PSEUDO_SOURCE_CODE)
	tokens = lexer.lex()
	parser = Parser(tokens)
	tree = parser.parse()
	if len(parser.logs) > 0:
		print(parser.logs)
	else:
		for node in tree:
			interpret_node(node)
