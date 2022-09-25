# Copyright 2022 Mertcan Davulcu.
# Use of this source code is governed by a BSD 3-Clause
# license that can be found in the LICENSE file.

from token import Token
from typing import Any

ERROR_WAITING_PARENTHESES: str = "waiting parentheses to close"
ERROR_INVALID_TOKEN: str = "invalid token: @"
ERROR_EXTRA_CLOSED_PARENTHESES: str = "extra closed parentheses"

TAG_MARK: str = "@"

# Makes log.
def make_log(token: Token, message: str, tag: Any | None = None) -> str:
	log = ""
	log += str(token.row) + ":" + str(token.column)
	log += " " + message
	if tag is not None:
		log = log.replace(TAG_MARK, str(tag))
	return log

# Makes plain log.
def make_log_plain(message: str, tag: Any | None = None) -> str:
	log = message
	if tag is not None:
		log = log.replace(TAG_MARK, str(tag))
	return log