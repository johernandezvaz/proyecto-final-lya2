from graphviz import Digraph

class AutomataVisualizer:
    def __init__(self):
        self.dot = Digraph(comment='French Language Compiler')
        self.dot.attr(rankdir='LR')
        
    def create_lexer_automaton(self):
        # Configuración del estilo
        self.dot.attr('node', shape='circle', style='filled', fillcolor='lightblue')
        
        # Estados principales
        states = {
            'START': 'Initial',
            'ID': 'Identifier',
            'KEYWORD': 'Keyword',
            'NUMBER': 'Number',
            'FLOAT': 'Float',
            'STRING': 'String',
            'OPERATOR': 'Operator',
            'DELIMITER': 'Delimiter',
            'ACCEPT': 'Accept'
        }
        
        # Crear estados
        for state, label in states.items():
            if state == 'ACCEPT':
                self.dot.node(state, label, shape='doublecircle', fillcolor='lightgreen')
            else:
                self.dot.node(state, label)

        # Transiciones para palabras clave y identificadores
        self.dot.edge('START', 'ID', 'letter')
        self.dot.edge('ID', 'ID', 'letter/digit')
        self.dot.edge('ID', 'KEYWORD', 'is_keyword')
        self.dot.edge('ID', 'ACCEPT', 'other')
        self.dot.edge('KEYWORD', 'ACCEPT', '')

        # Transiciones para números
        self.dot.edge('START', 'NUMBER', 'digit')
        self.dot.edge('NUMBER', 'NUMBER', 'digit')
        self.dot.edge('NUMBER', 'FLOAT', '.')
        self.dot.edge('FLOAT', 'FLOAT', 'digit')
        self.dot.edge('NUMBER', 'ACCEPT', 'other')
        self.dot.edge('FLOAT', 'ACCEPT', 'other')

        # Transiciones para strings
        self.dot.edge('START', 'STRING', '"')
        self.dot.edge('STRING', 'STRING', 'any except "')
        self.dot.edge('STRING', 'ACCEPT', '"')

        # Transiciones para operadores
        self.dot.edge('START', 'OPERATOR', '+,-,*,/,=,<,>,!')
        self.dot.edge('OPERATOR', 'ACCEPT', 'other')
        self.dot.edge('OPERATOR', 'OPERATOR', '=')

        # Transiciones para delimitadores
        self.dot.edge('START', 'DELIMITER', '(,),{,},;')
        self.dot.edge('DELIMITER', 'ACCEPT', '')

        return self.dot

    def get_grammar(self):
        return """
Gramática del Lenguaje (BNF):

<program>       ::= main <block>
<block>         ::= '{' <statement_list> '}'
<statement_list>::= <statement> <statement_list> | ε
<statement>     ::= <declaration> | <assignment> | <if_statement> | <while_statement> | <read_statement> | <print_statement>
<declaration>   ::= (nombre | crêpe) <id> ('=' <expression>)? ';'
<assignment>    ::= <id> '=' <expression> ';'
<if_statement>  ::= macaron '(' <condition> ')' <block> (autre <block>)?
<while_statement>::= tour_eiffel '(' <condition> ')' <block>
<read_statement>::= lire '(' <id> ')' ';'
<print_statement>::= afficher '(' <expression> ')' ';'
<condition>     ::= <expression> (<rel_op> <expression>)?
<expression>    ::= <term> (('+' | '-') <term>)*
<term>          ::= <factor> (('*' | '/') <factor>)*
<factor>        ::= <id> | <const> | '(' <expression> ')'
<rel_op>        ::= '==' | '!=' | '<' | '>' | '<=' | '>='
<id>            ::= [a-zA-Z_][a-zA-Z0-9_]*
<const>         ::= <integer_const> | <float_const>
"""

    def get_token_types(self):
        return {
            'Palabras Reservadas': [
                'main (programa principal)',
                'nombre (declaración de entero)',
                'crêpe (declaración de flotante)',
                'macaron (if)',
                'autre (else)',
                'tour_eiffel (while)',
                'afficher (imprimir)',
                'lire (leer)'
            ],
            'Operadores': [
                'Aritméticos: +, -, *, /',
                'Asignación: =',
                'Comparación: ==, !=, <, >, <=, >=',
                'Lógicos: &&, ||'
            ],
            'Delimitadores': [
                'Paréntesis: ( )',
                'Llaves: { }',
                'Punto y coma: ;',
                'Coma: ,'
            ],
            'Identificadores': 'Comienzan con letra o _, seguidos de letras, números o _',
            'Constantes': [
                'Enteros: Secuencia de dígitos',
                'Flotantes: Secuencia de dígitos con punto decimal',
                'Strings: Texto entre comillas dobles'
            ]
        }

    def get_parser_states(self):
        return """
Estados del Analizador Sintáctico:

1. INICIO → Espera 'main'
2. MAIN → Espera '{'
3. BLOCK → Espera declaraciones o '}'
4. DECLARATION → Procesa declaraciones de variables
5. IF_STATEMENT → Procesa estructuras condicionales
6. WHILE_STATEMENT → Procesa bucles
7. EXPRESSION → Procesa expresiones
8. TERM → Procesa términos
9. FACTOR → Procesa factores
10. ASSIGNMENT → Procesa asignaciones
11. PRINT → Procesa instrucciones de impresión
12. END → Estado final

Tabla de Transiciones:
--------------------
Estado Actual | Símbolo | Estado Siguiente
--------------------
INICIO        | main    | MAIN
MAIN          | {       | BLOCK
BLOCK         | nombre  | DECLARATION
BLOCK         | crêpe   | DECLARATION
BLOCK         | macaron | IF_STATEMENT
BLOCK         | autre   | IF_STATEMENT
BLOCK         | tour_   | WHILE_STATEMENT
BLOCK         | ID      | ASSIGNMENT
BLOCK         | }       | END
"""