class Interpreter:
    def __init__(self):
        self.variables = {}
        self.output = []

    def evaluate(self, node):
        method = getattr(self, f'evaluate_{node["type"]}', None)
        if method is None:
            raise RuntimeError(f"Unknown node type: {node['type']}")
        return method(node)

    def evaluate_program(self, node):
        results = []
        for statement in node['body']:
            result = self.evaluate(statement)
            if result is not None:
                results.append(str(result))
        return '\n'.join(results)

    def evaluate_variable_declaration(self, node):
        if node.get('value'):
            value = self.evaluate(node['value'])
            self.variables[node['name']] = value
        else:
            self.variables[node['name']] = 0 if node['var_type'] == 'INT' else 0.0
        return None

    def evaluate_assignment(self, node):
        if node['name'] not in self.variables:
            raise RuntimeError(f"Cannot assign to undefined variable: {node['name']}")
        value = self.evaluate(node['value'])
        self.variables[node['name']] = value
        return None

    def evaluate_binary_operation(self, node):
        left = self.evaluate(node['left'])
        right = self.evaluate(node['right'])
        
        operators = {
            'PLUS': lambda x, y: x + y,
            'MINUS': lambda x, y: x - y,
            'MULT': lambda x, y: x * y,
            'DIV': lambda x, y: x / y if y != 0 else (_ for _ in ()).throw(RuntimeError("Division by zero")),
            'GT': lambda x, y: x > y,
            'LT': lambda x, y: x < y,
            'EQ': lambda x, y: x == y,
            'NE': lambda x, y: x != y,
            'LE': lambda x, y: x <= y,
            'GE': lambda x, y: x >= y,
        }
        
        if node['operator'] not in operators:
            raise RuntimeError(f"Unknown operator: {node['operator']}")
            
        return operators[node['operator']](left, right)

    def evaluate_number(self, node):
        return node['value']

    def evaluate_string(self, node):
        return node['value']

    def evaluate_identifier(self, node):
        if node['name'] not in self.variables:
            raise RuntimeError(f"Undefined variable: {node['name']}")
        return self.variables[node['name']]

    def evaluate_print(self, node):
        value = self.evaluate(node['expression'])
        return str(value)

    def evaluate_if_statement(self, node):
        condition = self.evaluate(node['condition'])
        if condition:
            results = []
            for statement in node['consequent']:
                result = self.evaluate(statement)
                if result is not None:
                    results.append(str(result))
            return '\n'.join(results) if results else None
        elif node['alternate']:
            results = []
            for statement in node['alternate']:
                result = self.evaluate(statement)
                if result is not None:
                    results.append(str(result))
            return '\n'.join(results) if results else None
        return None

    def evaluate_while_loop(self, node):
        results = []
        while self.evaluate(node['condition']):
            for statement in node['body']:
                result = self.evaluate(statement)
                if result is not None:
                    results.append(str(result))
        return '\n'.join(results) if results else None

    def evaluate_read(self, node):
        if node['variable'] not in self.variables:
            raise RuntimeError(f"Cannot read into undefined variable: {node['variable']}")
        value = input(f"Enter value for {node['variable']}: ")
        try:
            # Try to convert to float first
            self.variables[node['variable']] = float(value)
        except ValueError:
            # If conversion fails, store as string
            self.variables[node['variable']] = value
        return None