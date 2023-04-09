from cable_token import TokenType
from cable_lexer import Lexer
import cable_ast as ast


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_token()
    
    def assert_type(self, type: TokenType):
        return True if self.current_token.type == type else False

    def eat(self, type: TokenType):
        if self.assert_type(type):
            self.current_token = self.lexer.get_token()
        else:
            raise Exception(f'token type error(need {type}, token {self.current_token.type})')
    
    def num(self):
        v1 = self.current_token.value
        self.eat(TokenType.INT)
        if self.assert_type(TokenType.DOT):
            self.eat(TokenType.DOT)
            v2 = self.current_token.value
            self.eat(TokenType.INT)
            return ast.Num(float(str(v1) + '.' + str(v2)))
        else:
            return ast.Num(v1)

    def variable(self):
        node = ast.Variable(self.current_token.value)
        self.eat(TokenType.ID)
        return node
    
    def empty(self):
        return ast.NoOp()
    
    def assignment_statement(self):
        left = self.variable()
        self.eat(TokenType.EQ)
        right = self.expr()
        return ast.Assign(left, right)
    
    def statement(self):
        if self.assert_type(TokenType.ID):
            return self.assignment_statement()
        else:
            return self.empty()
    
    def body(self):
        node = self.statement()
        nodes = [node]
        while self.current_token.type in (TokenType.EOL, TokenType.SEMI):
            self.eat(self.current_token.type)
            nodes.append(self.statement())
        if self.assert_type(TokenType.ID):
            raise Exception
        root = ast.Compound()
        root.children = nodes
        return root
    
    def program(self):
        node = self.body()
        self.eat(TokenType.END)
        return node

    def factor(self):
        if self.assert_type(TokenType.MINUS):
            self.eat(TokenType.MINUS)
            return ast.UnaryOp(ast.UnaryOpType.OPPOSITE, self.factor())
        elif self.assert_type(TokenType.PLUS):
            self.eat(TokenType.PLUS)
            
        if self.assert_type(TokenType.INT):
            return self.num()
        elif self.assert_type(TokenType.LP):
            self.eat(TokenType.LP)
            node = self.expr()
            self.eat(TokenType.RP)
            return node
        else:
            return self.variable()
    
    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            if self.assert_type(TokenType.MUL):
                self.eat(TokenType.MUL)
                node = ast.BinOp(ast.BinOpType.MUL_OP, node, self.factor())
            if self.assert_type(TokenType.DIV):
                self.eat(TokenType.DIV)
                node = ast.BinOp(ast.BinOpType.DIV_OP, node, self.factor())
        return node
    
    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.assert_type(TokenType.PLUS):
                self.eat(TokenType.PLUS)
                node = ast.BinOp(ast.BinOpType.ADD_OP, node, self.term())
            if self.assert_type(TokenType.MINUS):
                self.eat(TokenType.MINUS)
                node = ast.BinOp(ast.BinOpType.SUB_OP, node, self.term())
        return node

    def parse(self):
        node = self.program()
        if self.current_token.type != TokenType.END:
            raise Exception
        return node