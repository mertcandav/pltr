# Copyright 2022 Mertcan Davulcu.
# Use of this source code is governed by a BSD 3-Clause
# license that can be found in the LICENSE file.

from __future__ import annotations
from tokens import *
from logs import *

# Left or right expression of binary operation
class BinopExpr:
	def __init__(self, data: str) -> None:
		self.data = data

# Binary operation.
class BinaryOp:
	def __init__(self,
				left: BinopExpr | BinaryOp,
				right: BinopExpr | BinaryOp,
				operator: str) -> None:
		self.left = left
		self.right = right
		self.operator = operator

# Print operation
class PrintOp:
	def __init__(self, expr: BinopExpr | BinaryOp) -> None:
		self.expr = expr

# Assignment operation
class AssignmentOp:
	def __init__(self, identifier: Token, expr: BinopExpr | BinaryOp) -> None:
		self.identifier = identifier
		self.expr = expr

# AST builder class for experimental X language of PLTR.
class AST:
	def __init__(self, tokens: list[Token]) -> None:
		self.tokens = tokens
		self.logs: list[str] = []
		self.__offset = 0
		self.__tree: list[BinaryOp] = []

	# Returns next statement.
	def __resume_statement(self) -> list[Token]:
		pn = 0
		tokens = self.tokens[self.__offset:]
		for i, token in enumerate(tokens):
			if token.identity == ID_PARENTHESES:
				if token.kind == "(":
					pn += 1
				else:
					pn -= 1
				continue
			if pn > 0 or i == 0:
				continue
			prev = tokens[i-1]
			# New line
			if prev.row < token.row:
				tokens = tokens[:i]
				break

		self.__offset += len(tokens)
		return tokens

	# Builds print operation.
	def __build_print(self, tokens: list[Token]) -> PrintOp | None:
		# Just print keyword.
		if len(tokens) == 1:
			self.logs.append(make_log(tokens[0], ERROR_EXPRESSION_MISSING))
			return None

		# Remove print keyword from expression.
		tokens = tokens[1:]

		expr = self.__build_expr(tokens)
		return PrintOp(expr)

	# Builds assignment operation.
	def __build_assignment(self, tokens: list[Token]) -> AssignmentOp:
		identifier = tokens[0]
		
		# Remove identifier and assignment operator token.
		tokens = tokens[2:]
		expr = self.__build_expr(tokens)

		return AssignmentOp(identifier, expr)

	# Append statement to tree from tokens.
	def __append_statement(self, tokens: list[Token]) -> None:
		# Print operation.
		if tokens[0].identity == ID_PRINT:
			self.__tree.append(self.__build_print(tokens))
			return
		
		# Assignment checking.
		if len(tokens) > 1:
			identifier = tokens[0]
			if identifier.identity == ID_ID:
				# Is assignment.
				if tokens[1].identity == ID_OPERATOR and tokens[1].kind == "=":
					self.__tree.append(self.__build_assignment(tokens))
					return

		# Expression.
		self.__tree.append(self.__build_expr(tokens))

	# Builds AST from tokens.
	def build(self) -> list[BinaryOp]:
		while self.__offset < len(self.tokens):
			tokens = self.__resume_statement()
			self.__append_statement(tokens)
		return self.__tree

	# Builds AST left or right of binary operation.
	def __build_op(self, tokens: list[Token]) -> BinaryOp | BinopExpr | None:
		# If first token is not operator.
		if tokens[0].identity != ID_OPERATOR:
			i = find_lowest_operator(tokens)
			if i != -1:
				return self.__build_expr(tokens)

		# Parentheses group.
		if tokens[0].identity == ID_PARENTHESES:
			return self.__build_op(tokens[1:-1])

		# Expression can have two token maximum.
		# If len(token) > 2: invalid syntax
		if len(tokens) > 2:
			self.logs.append(make_log(tokens[2], ERROR_INVALID_SYNTAX))
			return None

		# If expression have two token, first token must be unary operator.
		if len(tokens) == 2:
			token = tokens[0]
			if token.identity != ID_OPERATOR:
				self.logs.append(make_log(token, ERROR_INVALID_SYNTAX))
				return None
			# Check for valid unary operator.
			if token.kind != "+" and token.kind != "-":
				self.logs.append(make_log(token, ERROR_INVALID_SYNTAX))
				return None
			return BinopExpr(token.kind + tokens[1].kind)

		return BinopExpr(tokens[0].kind)

	# Build evaluate expression.
	def __build_expr(self, tokens: list[Token]) -> BinaryOp | BinopExpr:
		i = find_lowest_operator(tokens)
		# Operator not found, expression is probably
		# parentheses group or single expression.
		if i == -1:
			return self.__build_op(tokens)

		op = BinaryOp(None, None, None)
		op.left = self.__build_op(tokens[:i])
		op.operator = tokens[i].kind
		op.right = self.__build_op(tokens[i+1:])
		return op

# Returns lowest precedenced operator index.
# Returns -1 if operator not exist.
# Skips parentheses ranges.
def find_lowest_operator(tokens: list[Token]) -> int:
	p1 = -1
	p2 = -1
	pn = 0
	i = len(tokens)
	while i >= 0:
		i -= 1
		token = tokens[i]
		if token.identity == ID_PARENTHESES:
			if token.kind == "(":
				pn += 1
			else:
				pn -= 1
			continue
		if pn != 0:
			continue
		if token.identity != ID_OPERATOR:
			continue
		if token.kind == "+" or token.kind == "-":
			return i
		elif token.kind == "/" or token.kind == "*":
			p2 = p2 if p2 != -1 else i
		else:
			p3 = p3 if p3 != -1 else i
	if p2 != -1:
		return p2
	return p1
