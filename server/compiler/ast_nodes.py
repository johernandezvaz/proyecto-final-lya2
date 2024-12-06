class ASTNode:
    def to_dict(self):
        raise NotImplementedError

class Program(ASTNode):
    def __init__(self, body):
        self.body = body
    
    def to_dict(self):
        return {
            'type': 'program',
            'body': [stmt.to_dict() for stmt in self.body]
        }

class VariableDeclaration(ASTNode):
    def __init__(self, var_type, name, value=None):
        self.var_type = var_type
        self.name = name
        self.value = value
    
    def to_dict(self):
        return {
            'type': 'variable_declaration',
            'var_type': self.var_type,
            'name': self.name,
            'value': self.value.to_dict() if self.value else None
        }

class Assignment(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def to_dict(self):
        return {
            'type': 'assignment',
            'name': self.name,
            'value': self.value.to_dict()
        }

class BinaryOperation(ASTNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right
    
    def to_dict(self):
        return {
            'type': 'binary_operation',
            'operator': self.operator,
            'left': self.left.to_dict(),
            'right': self.right.to_dict()
        }

class Number(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def to_dict(self):
        return {
            'type': 'number',
            'value': self.value
        }

class String(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def to_dict(self):
        return {
            'type': 'string',
            'value': self.value
        }

class Identifier(ASTNode):
    def __init__(self, name):
        self.name = name
    
    def to_dict(self):
        return {
            'type': 'identifier',
            'name': self.name
        }

class Print(ASTNode):
    def __init__(self, expression):
        self.expression = expression
    
    def to_dict(self):
        return {
            'type': 'print',
            'expression': self.expression.to_dict()
        }

class IfStatement(ASTNode):
    def __init__(self, condition, consequent, alternate=None):
        self.condition = condition
        self.consequent = consequent
        self.alternate = alternate
    
    def to_dict(self):
        return {
            'type': 'if_statement',
            'condition': self.condition.to_dict(),
            'consequent': [stmt.to_dict() for stmt in self.consequent],
            'alternate': [stmt.to_dict() for stmt in self.alternate] if self.alternate else None
        }

class WhileLoop(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def to_dict(self):
        return {
            'type': 'while_loop',
            'condition': self.condition.to_dict(),
            'body': [stmt.to_dict() for stmt in self.body]
        }

class Read(ASTNode):
    def __init__(self, variable):
        self.variable = variable
    
    def to_dict(self):
        return {
            'type': 'read',
            'variable': self.variable
        }