# Copyright 2022 Mertcan Davulcu.
# Use of this source code is governed by a BSD 3-Clause
# license that can be found in the LICENSE file.

from string import punctuation
from tokens import *
from logs import *

# Reports rune is space or not.
def is_space(rune: str) -> bool:
	return (
		rune == ' ' or
		rune == '\t' or
		rune == '\v' or
		rune == '\n' or
		rune == '\r'
	)

# Reports rune is decimal or not.
def is_decimal(rune: str) -> bool:
	return (
		rune == '0' or
		rune == '1' or
		rune == '2' or
		rune == '3' or
		rune == '4' or
		rune == '5' or
		rune == '6' or
		rune == '7' or
		rune == '8' or
		rune == '9'
	)

# Keyword dictionary.
KEYWORDS: dict[str, int] = {
	"print": ID_PRINT,
}

# Operator dictionary.
OPERATORS: dict[str, int] = {
	"+": ID_OPERATOR,
	"-": ID_OPERATOR,
	"*": ID_OPERATOR,
	"/": ID_OPERATOR,
	"%": ID_OPERATOR,
	"^": ID_OPERATOR,
	"=": ID_OPERATOR,
}

# Lexer for experimental X language of PLTR.
class Lexer:
	def __init__(self, text: str) -> None:
		self.logs: list[str] = []
		self.text = text
		# Parentheses counter.
		self.__parentheses_n = 0
		# Current offset of text.
		self.__offset = 0
		# Current column.
		self.__column = 0
		# Current row.
		self.__row = 0

	# Sets lexer to new line.
	def __new_line(self) -> None:
		self.__column = 1
		self.__row += 1

	# Resume text from offset.
	# Skips spaces.
	# Returns text from starts offset.
	def __resume(self) -> str:
		for i, rune in enumerate(self.text[self.__offset:]):
			if is_space(rune):
				if rune == "\n":
					self.__new_line()
				self.__offset += 1
				continue
			break
		return self.text[self.__offset:]

	# Checks non-closed parenthseses.
	# Logs error if exist.
	def __check_ranges(self) -> None:
		if self.__parentheses_n > 0:
			self.logs.append(make_log_plain(ERROR_WAITING_PARENTHESES))

	# Lexes float literal.
	# Returns literal string.
	# Return empty string if failed lexing.
	def __lex_float(self, text: str, i: int) -> str:
		while i < len(text):
			i += 1
			rune = text[i]
			if not is_decimal(rune):
				break
		# Just dot.
		if i == 1:
			return ""
		return text[:i]

	# Lexes numeric literal.
	# Returns literal string.
	# Returns empty string if failed lexing.
	def __lex_num(self, text: str) -> str:
		i = 0
		while i < len(text):
			rune = text[i]
			if rune == '.':
				return self.__lex_float(text, i)
			elif not is_decimal(rune):
				break
			i += 1
		if i == 0:
			return ""
		return text[:i]

	# Returns true if numeric lexing is success, false if not.
	def __lex_numeric(self, text: str, token: Token) -> bool:
		lex = self.__lex_num(text)
		if lex == "":
			return False
		token.kind = lex
		token.identity = ID_EXPR
		return True

	# Lexes and returns identifier.
	# Returns empty string if failed lexing.
	def __lex_id(self, text: str) -> str:
		if text[0] != '_' and not text[0].isalpha():
			return ""
		identifier = ""
		for i, rune in enumerate(text):
			if rune != '_' and not is_decimal(rune) and not rune.isalpha():
				identifier = text[:i]
				break
		return identifier

	# Returns true if identifier lexing is success, false if not.
	def __lex_identifier(self, text: str, token: Token) -> bool:
		lex = self.__lex_id(text)
		if lex == "":
			return False
		token.kind = lex
		token.identity = ID_ID
		return True

	# Reports text is starts with keyword or not.
	def __is_keyword(self, text: str, keyword: str) -> bool:
		if not text.startswith(keyword):
			return False
		text = text[len(keyword):]
		if text == "":
			return True
		rune = text[0]
		if rune == '_':
			return False
		return is_space(rune) or rune in punctuation or not rune.isalpha()

	# Returns true if keyword lexing is success, false if not.
	def __lex_keyword(self, text: str, token: Token) -> bool:
		for k, v in KEYWORDS.items():
			if self.__is_keyword(text, k):
				token.kind = k
				token.identity = v
				return True
		return False

	# Returns true if operator lexing is success, false if not.
	def __lex_operator(self, text: str, token: Token) -> bool:
		for k, v in OPERATORS.items():
			if text.startswith(k):
				token.kind = k
				token.identity = v
				return True
		return False

	# Resume text from offset and returns token.
	# Returns None if finished text lexing.
	def __token(self) -> Token | None:
		text = self.__resume()
		if text == "":
			return None
		
		token = Token(ID_NA, self.__row, self.__column, "")
		if self.__lex_numeric(text, token):
			pass
		elif self.__lex_operator(text, token):
			pass
		elif self.__lex_keyword(text, token):
			pass
		elif self.__lex_identifier(text, token):
			pass
		elif text[0] == '(':
			self.__parentheses_n += 1
			token.kind = "("
			token.identity = ID_PARENTHESES
		elif text[0] == ')':
			if self.__parentheses_n == 0:
				self.logs.append(make_log(token, ERROR_EXTRA_CLOSED_PARENTHESES))
			else:
				self.__parentheses_n -= 1
			token.kind = ")"
			token.identity = ID_PARENTHESES
		else:
			self.logs.append(make_log_plain(ERROR_INVALID_TOKEN, text[0]))
			self.__offset += 1
			return None

		self.__offset += len(token.kind)
		self.__column += len(token.kind)
		return token

	# Lexes all tokens.
	def lex(self) -> list[Token]:
		self.__new_line()

		tokens: list[Token] = []
		while self.__offset < len(self.text):
			token = self.__token()
			if token is not None:
				tokens.append(token)

		self.__check_ranges()
		return tokens
