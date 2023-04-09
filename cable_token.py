from enum import Enum, auto


class TokenType(Enum):
        INT = auto()
        END = auto()
        PLUS = '+'
        MINUS = '-'
        MUL = '*'
        DIV = '/'
        EOL = '\n'
        LP = '('
        RP = ')'
        DOT = '.'

        LC = '{'
        RC = '}'
        EQ = '='
        SEMI = ';'
        ID = auto()


class Token:
        def __init__(self, type: TokenType, value=None):
            self.type = type
            self.value = value