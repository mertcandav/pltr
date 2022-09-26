# Copyright 2022 Mertcan Davulcu.
# Use of this source code is governed by a BSD 3-Clause
# license that can be found in the LICENSE file.

from tokens import *
from __future__ import annotations

# Left or right expression of binary operation
class BinopExpr:
	data = ""

	def __init__(self, data: str) -> None:
		self.data = data

# Binary operation.
class BinaryOp:
	left: BinopExpr | BinaryOp = None
	operator: str = ""
	right: BinopExpr | BinaryOp = None

	def __init__(self,
				left: BinopExpr | BinaryOp,
				right: BinopExpr | BinaryOp,
				operator: str) -> None:
		self.left = left
		self.right = right
		self.operator = operator

# AST builder class for experimental X language of PLTR.
class AST:
	tokens: list[Token] = []

	# Builds AST left or right of binary operation.
	def __build_op(self, tokens: list[Token]) -> BinaryOp | BinopExpr:
		if tokens[0].identity != ID_OPERATOR:
			i = find_lowest_operator(tokens)
			if i != -1:
				return self.__build_ops(tokens)
		if tokens[0].identity == ID_PARENTHESES:
			return self.__build_op(tokens[1:-1])
		if len(tokens) > 2:
			raise Exception("invalid syntax")
		if len(tokens) == 2:
			token = tokens[0]
			if token.identity != ID_OPERATOR:
				raise Exception("invalid syntax")
			if token.kind != "+" and token.kind != "-":
				raise Exception("invalid syntax")
			return BinopExpr(token.kind + tokens[1].kind)
		return BinopExpr(tokens[0].kind)

	# Build evaluate expression.
	def __build_expression(self, tokens: list[Token]) -> BinaryOp:
		i = find_lowest_operator(tokens)
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
