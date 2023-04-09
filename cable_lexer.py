from cable_token import Token, TokenType


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
    
    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        pos = self.pos + 1
        return self.text[pos] if pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and (self.current_char.isspace() and self.current_char != '\n'):
            self.advance()

    def get_integer(self):
        buf = ''
        while self.current_char is not None and self.current_char.isdigit():
            buf += self.current_char
            self.advance()
        return Token(TokenType.INT, int(buf))

    def _id(self):
        buf = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            buf += self.current_char
            self.advance()
        return Token(TokenType.ID, buf)

    def get_token(self) -> Token:
        while self.current_char is not None:
            if self.current_char.isspace():
                if self.current_char == '\n':
                    self.advance()
                    return Token(TokenType.EOL)
                else:
                    self.skip_whitespace()
                    continue
                
            if self.current_char.isdigit():
                return self.get_integer()
            if self.current_char.isalpha() or self.current_char == '_':
                return self._id()
            
            if self.current_char in ('+','-','*','/','(',')','.','=',';','{','}'):
                current_char = self.current_char
                self.advance()
                return Token(TokenType(current_char))
            
            raise Exception(f'bad character{self.current_char}')
        return Token(TokenType.END)