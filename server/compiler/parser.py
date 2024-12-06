from .ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.variables = {}

    def peek(self):
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None

    def consume(self, expected_type=None):
        if expected_type and self.peek()['type'] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {self.peek()['type']}")
        token = self.peek()
        self.current += 1
        return token

    def parse(self):
        if not self.tokens:
            return Program([])

        if self.peek()['type'] != 'MAIN':
            raise SyntaxError("Program must start with 'main'")

        self.consume('MAIN')
        if not self.peek() or self.peek()['type'] != 'LBRACE':
            raise SyntaxError("Expected '{' after 'main'")
        self.consume('LBRACE')
        
        body = []
        while self.peek() and self.peek()['type'] != 'RBRACE':
            statement = self.parse_statement()
            if statement:
                body.append(statement)

        if not self.peek() or self.peek()['type'] != 'RBRACE':
            raise SyntaxError("Expected '}' at end of program")
        self.consume('RBRACE')

        return Program(body)

    def parse_statement(self):
        if not self.peek():
            return None

        token = self.peek()
        
        if token['type'] in ['INT', 'FLOAT']:
            return self.parse_variable_declaration()
        elif token['type'] == 'PRINT':
            return self.parse_print()
        elif token['type'] == 'IF':
            return self.parse_if_statement()
        elif token['type'] == 'WHILE':
            return self.parse_while_loop()
        elif token['type'] == 'READ':
            return self.parse_read()
        elif token['type'] == 'ID':
            return self.parse_assignment()
        
        self.consume()
        return None

    def parse_variable_declaration(self):
        var_type = self.consume()['type']
        
        if not self.peek() or self.peek()['type'] != 'ID':
            raise SyntaxError(f"Expected identifier after {var_type.lower()}")
            
        var_name = self.consume('ID')['value']
        value = None

        if self.peek() and self.peek()['type'] == 'ATTR':
            self.consume('ATTR')
            value = self.parse_expression()

        if not self.peek() or self.peek()['type'] != 'PCOMMA':
            raise SyntaxError("Expected ';' after variable declaration")
        self.consume('PCOMMA')

        return VariableDeclaration(var_type, var_name, value)

    def parse_assignment(self):
        var_name = self.consume('ID')['value']

        if not self.peek() or self.peek()['type'] != 'ATTR':
            raise SyntaxError(f"Expected '=' after variable name '{var_name}'")
        self.consume('ATTR')

        value = self.parse_expression()

        if not self.peek() or self.peek()['type'] != 'PCOMMA':
            raise SyntaxError("Expected ';' after assignment")
        self.consume('PCOMMA')

        return Assignment(var_name, value)

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_additive()

        while self.peek() and self.peek()['type'] in ['GT', 'LT', 'EQ', 'NE', 'LE', 'GE']:
            operator = self.consume()['type']
            right = self.parse_additive()
            left = BinaryOperation(operator, left, right)

        return left

    def parse_additive(self):
        left = self.parse_multiplicative()

        while self.peek() and self.peek()['type'] in ['PLUS', 'MINUS']:
            operator = self.consume()['type']
            right = self.parse_multiplicative()
            left = BinaryOperation(operator, left, right)

        return left

    def parse_multiplicative(self):
        left = self.parse_primary()

        while self.peek() and self.peek()['type'] in ['MULT', 'DIV']:
            operator = self.consume()['type']
            right = self.parse_primary()
            left = BinaryOperation(operator, left, right)

        return left

    def parse_primary(self):
        if not self.peek():
            raise SyntaxError("Unexpected end of input")

        token = self.peek()

        if token['type'] in ['INTEGER_CONST', 'FLOAT_CONST']:
            self.consume()
            return Number(float(token['value']))
        elif token['type'] == 'STRING':
            self.consume()
            return String(token['value'][1:-1])  # Remove quotes
        elif token['type'] == 'ID':
            self.consume()
            return Identifier(token['value'])
        elif token['type'] == 'LBRACKET':
            self.consume()
            expr = self.parse_expression()
            if not self.peek() or self.peek()['type'] != 'RBRACKET':
                raise SyntaxError("Expected ')'")
            self.consume()
            return expr
        else:
            raise SyntaxError(f"Unexpected token: {token['type']}")

    def parse_print(self):
        self.consume('PRINT')
        
        if not self.peek() or self.peek()['type'] != 'LBRACKET':
            raise SyntaxError("Expected '(' after 'afficher'")
        self.consume('LBRACKET')

        expression = self.parse_expression()
        
        if not self.peek() or self.peek()['type'] != 'RBRACKET':
            raise SyntaxError("Expected ')' after expression")
        self.consume('RBRACKET')
        
        if not self.peek() or self.peek()['type'] != 'PCOMMA':
            raise SyntaxError("Expected ';' after print statement")
        self.consume('PCOMMA')

        return Print(expression)

    def parse_if_statement(self):
        self.consume('IF')
        
        if not self.peek() or self.peek()['type'] != 'LBRACKET':
            raise SyntaxError("Expected '(' after 'macaron'")
        self.consume('LBRACKET')

        condition = self.parse_expression()

        if not self.peek() or self.peek()['type'] != 'RBRACKET':
            raise SyntaxError("Expected ')' after condition")
        self.consume('RBRACKET')

        if not self.peek() or self.peek()['type'] != 'LBRACE':
            raise SyntaxError("Expected '{' after condition")
        self.consume('LBRACE')

        consequent = []
        while self.peek() and self.peek()['type'] != 'RBRACE':
            statement = self.parse_statement()
            if statement:
                consequent.append(statement)

        if not self.peek() or self.peek()['type'] != 'RBRACE':
            raise SyntaxError("Expected '}' after if block")
        self.consume('RBRACE')

        alternate = None
        if self.peek() and self.peek()['type'] == 'ELSE':
            self.consume('ELSE')
            if not self.peek() or self.peek()['type'] != 'LBRACE':
                raise SyntaxError("Expected '{' after 'autre'")
            self.consume('LBRACE')

            alternate = []
            while self.peek() and self.peek()['type'] != 'RBRACE':
                statement = self.parse_statement()
                if statement:
                    alternate.append(statement)

            if not self.peek() or self.peek()['type'] != 'RBRACE':
                raise SyntaxError("Expected '}' after else block")
            self.consume('RBRACE')

        return IfStatement(condition, consequent, alternate)

    def parse_while_loop(self):
        self.consume('WHILE')
        
        if not self.peek() or self.peek()['type'] != 'LBRACKET':
            raise SyntaxError("Expected '(' after 'tour_eiffel'")
        self.consume('LBRACKET')

        condition = self.parse_expression()

        if not self.peek() or self.peek()['type'] != 'RBRACKET':
            raise SyntaxError("Expected ')' after condition")
        self.consume('RBRACKET')

        if not self.peek() or self.peek()['type'] != 'LBRACE':
            raise SyntaxError("Expected '{' after condition")
        self.consume('LBRACE')

        body = []
        while self.peek() and self.peek()['type'] != 'RBRACE':
            statement = self.parse_statement()
            if statement:
                body.append(statement)

        if not self.peek() or self.peek()['type'] != 'RBRACE':
            raise SyntaxError("Expected '}' after while block")
        self.consume('RBRACE')

        return WhileLoop(condition, body)

    def parse_read(self):
        self.consume('READ')
        
        if not self.peek() or self.peek()['type'] != 'LBRACKET':
            raise SyntaxError("Expected '(' after 'lire'")
        self.consume('LBRACKET')

        if not self.peek() or self.peek()['type'] != 'ID':
            raise SyntaxError("Expected variable name in read statement")
        var_name = self.consume('ID')['value']

        if not self.peek() or self.peek()['type'] != 'RBRACKET':
            raise SyntaxError("Expected ')' after variable name")
        self.consume('RBRACKET')

        if not self.peek() or self.peek()['type'] != 'PCOMMA':
            raise SyntaxError("Expected ';' after read statement")
        self.consume('PCOMMA')

        return Read(var_name)