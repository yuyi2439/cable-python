from enum import Enum, auto


class BinOpType(Enum):
    ADD_OP = auto()
    SUB_OP = auto()
    MUL_OP = auto()
    DIV_OP = auto()

class UnaryOpType(Enum):
    OPPOSITE = auto()


class Ast:
    pass


class BinOp(Ast):
    def __init__(self, op: BinOpType, left: Ast, right: Ast):
        self.op = op
        self.left = left
        self.right = right


class Num(Ast):
    def __init__(self, value: float):
        self.value = value


class UnaryOp(Ast):
    def __init__(self, op: UnaryOpType, tree: Ast):
        self.op = op
        self.tree = tree


class Compound(Ast):
    def __init__(self):
        self.children = []


class Variable(Ast):
    def __init__(self, name):
        self.name = name


class Assign(Ast):
    def __init__(self, left: Variable, right: Ast):
        self.left = left
        self.right = right


class NoOp(Ast):
    pass
