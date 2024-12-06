class SemanticTranslator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f't{self.temp_counter}'

    def new_label(self):
        self.label_counter += 1
        return f'L{self.label_counter}'

    def emit(self, op, arg1=None, arg2=None, result=None):
        instruction = {
            'op': op,
            'arg1': arg1,
            'arg2': arg2,
            'result': result
        }
        self.code.append(instruction)
        return instruction

    def translate_expression(self, node):
        if node['type'] == 'binary_operation':
            left_temp = self.translate_expression(node['left'])
            right_temp = self.translate_expression(node['right'])
            result = self.new_temp()
            self.emit(node['operator'], left_temp, right_temp, result)
            return result
        elif node['type'] == 'number':
            temp = self.new_temp()
            self.emit('ASSIGN', str(node['value']), None, temp)
            return temp
        elif node['type'] == 'identifier':
            return node['name']
        return None

    def translate_declaration(self, node):
        if node.get('value'):
            value_temp = self.translate_expression(node['value'])
            self.emit('DECLARE', node['var_type'], value_temp, node['name'])
        else:
            self.emit('DECLARE', node['var_type'], '0', node['name'])

    def translate_assignment(self, node):
        value_temp = self.translate_expression(node['value'])
        self.emit('ASSIGN', value_temp, None, node['name'])

    def translate_if(self, node):
        condition_temp = self.translate_expression(node['condition'])
        else_label = self.new_label()
        end_label = self.new_label()

        self.emit('IF_FALSE', condition_temp, None, else_label)
        
        for stmt in node['consequent']:
            self.translate_statement(stmt)
        
        self.emit('GOTO', None, None, end_label)
        self.emit('LABEL', None, None, else_label)
        
        if node['alternate']:
            for stmt in node['alternate']:
                self.translate_statement(stmt)
        
        self.emit('LABEL', None, None, end_label)

    def translate_while(self, node):
        start_label = self.new_label()
        end_label = self.new_label()
        
        self.emit('LABEL', None, None, start_label)
        condition_temp = self.translate_expression(node['condition'])
        self.emit('IF_FALSE', condition_temp, None, end_label)
        
        for stmt in node['body']:
            self.translate_statement(stmt)
        
        self.emit('GOTO', None, None, start_label)
        self.emit('LABEL', None, None, end_label)

    def translate_print(self, node):
        value_temp = self.translate_expression(node['expression'])
        self.emit('PRINT', value_temp)

    def translate_statement(self, node):
        if node['type'] == 'variable_declaration':
            self.translate_declaration(node)
        elif node['type'] == 'assignment':
            self.translate_assignment(node)
        elif node['type'] == 'if_statement':
            self.translate_if(node)
        elif node['type'] == 'while_loop':
            self.translate_while(node)
        elif node['type'] == 'print':
            self.translate_print(node)

    def translate(self, ast):
        if ast['type'] == 'program':
            for statement in ast['body']:
                self.translate_statement(statement)
        return self.code