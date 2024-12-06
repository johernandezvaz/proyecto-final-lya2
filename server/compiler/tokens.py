from typing import List, Dict

# Definición de tokens del lenguaje
TOKEN_SPEC = [
    ('MAIN',        r'main'),                 # main
    ('INT',         r'nombre'),               # int (nombre en francés)
    ('FLOAT',       r'crêpe'),                # float (crêpe en francés)
    ('IF',          r'macaron'),              # if (macaron en francés)
    ('ELSE',        r'autre'),                # else (autre en francés)
    ('WHILE',       r'tour_eiffel'),          # while (tour_eiffel en francés)
    ('READ',        r'lire'),                 # read (lire en francés)
    ('PRINT',       r'afficher'),             # print (afficher en francés)
    ('LBRACKET',    r'\('),                   # (
    ('RBRACKET',    r'\)'),                   # )
    ('LBRACE',      r'\{'),                   # {
    ('RBRACE',      r'\}'),                   # }
    ('COMMA',       r','),                    # ,
    ('PCOMMA',      r';'),                    # ;
    ('EQ',          r'=='),                   # ==
    ('NE',          r'!='),                   # !=
    ('LE',          r'<='),                   # <=
    ('GE',          r'>='),                   # >=
    ('OR',          r'\|\|'),                 # ||
    ('AND',         r'&&'),                   # &&
    ('ATTR',        r'\='),                   # =
    ('LT',          r'<'),                    # <
    ('GT',          r'>'),                    # >
    ('PLUS',        r'\+'),                   # +
    ('MINUS',       r'-'),                    # -
    ('MULT',        r'\*'),                   # *
    ('DIV',         r'\/'),                   # /
    ('ID',          r'[a-zA-Z_]\w*'),         # Identificadores
    ('FLOAT_CONST', r'\d+\.\d+'),             # Constantes de punto flotante
    ('INTEGER_CONST', r'\d+'),                # Constantes enteras
    ('STRING',      r'"[^"\n]*"'),            # Cadenas de texto
    ('NEWLINE',     r'\n'),                   # Fin de línea
    ('SKIP',        r'[ \t]+'),               # Espacios y tabulaciones
    ('COMMENT',     r'#.*'),                  # Comentarios
]

class Token:
    def __init__(self, type: str, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'Token({self.type}, {self.value}, line={self.line}, col={self.column})'

    def to_dict(self):
        return {
            'type': self.type,
            'value': self.value,
            'line': self.line,
            'column': self.column
        }