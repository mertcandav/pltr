# Copyright 2022 Mertcan Davulcu.
# Use of this source code is governed by a BSD 3-Clause
# license that can be found in the LICENSE file.

ID_NA = 0
ID_ID = 1
ID_EXPR = 2
ID_OPERATOR = 3
ID_PRINT = 4
ID_LET = 5
ID_PARENTHESES = 6

class Token:
    identity = 0
    row = 0
    column = 0
    kind = ""

    def __init__(self, identity: int, row: int, column: int, kind: str) -> None:
        self.identity = identity
        self.row = row
        self.column = column
        self.kind = kind
