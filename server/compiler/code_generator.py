class CodeGenerator:
    def __init__(self):
        self.code = []
        self.variables = {}

    def generate_code(self, ir_code):
        python_code = []
        
        for instruction in ir_code:
            op = instruction['op']
            
            if op == 'DECLARE':
                var_type = instruction['arg1']
                initial_value = instruction['arg2']
                var_name = instruction['result']
                self.variables[var_name] = var_type
                python_code.append(f"{var_name} = {initial_value}")
                
            elif op in ['PLUS', 'MINUS', 'MULT', 'DIV']:
                op_map = {'PLUS': '+', 'MINUS': '-', 'MULT': '*', 'DIV': '/'}
                python_code.append(
                    f"{instruction['result']} = {instruction['arg1']} {op_map[op]} {instruction['arg2']}"
                )
                
            elif op == 'ASSIGN':
                python_code.append(f"{instruction['result']} = {instruction['arg1']}")
                
            elif op == 'IF_FALSE':
                python_code.append(f"if not {instruction['arg1']}:")
                python_code.append(f"    goto {instruction['result']}")
                
            elif op == 'GOTO':
                python_code.append(f"goto {instruction['result']}")
                
            elif op == 'LABEL':
                python_code.append(f"label {instruction['result']}:")
                
            elif op == 'PRINT':
                python_code.append(f"print({instruction['arg1']})")

        return '\n'.join(python_code)