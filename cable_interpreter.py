import cable_ast as ast
from cable_parser import Parser


class NodeVisitor:
    def visit(self, node: ast.Ast):
        method_name = 'visit_' + type(node).__name__
        visiter = getattr(self, method_name, self.generic_visit)
        return visiter(node)
    
    def generic_visit(self, node):
        raise Exception(f'未找到visit_{type(node).__name__}()方法')


class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}

    def __init__(self, parser: Parser):
        self.parser = parser
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)
    
    def visit_Assign(self, node: ast.Assign):
        var_name = node.left.name
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
    
    def visit_Variable(self, node):
        var_name = node.name
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError(f'错误的标识符: {repr(var_name)}')
        else:
            return value
    
    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node: ast.BinOp):
        if node.op == ast.BinOpType.ADD_OP:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op == ast.BinOpType.SUB_OP:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op == ast.BinOpType.MUL_OP:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op == ast.BinOpType.DIV_OP:
            return self.visit(node.left) / self.visit(node.right)
    
    def visit_Num(self, node: ast.Num):
        return node.value
    
    def visit_UnaryOp(self, node: ast.UnaryOp):
        if node.op == ast.UnaryOpType.OPPOSITE:
            return -self.visit(node.tree)
    
    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
