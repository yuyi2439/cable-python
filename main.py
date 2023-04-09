from cable_lexer import Lexer
from cable_parser import Parser
from cable_interpreter import Interpreter


if __name__ == '__main__':
    text = """
    number = 2 ; a = number
    b = 10 * a + 10 * number / 4
    _c = a - -b
    x = 11
    """
    lexer = Lexer(text)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    value = interpreter.interpret()
    print(interpreter.GLOBAL_SCOPE)
