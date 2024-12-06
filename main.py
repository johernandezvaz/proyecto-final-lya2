import re

# Definir los patrones para los diferentes tipos de tokens
token_specification = [
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
    ('MISMATCH',    r'.'),                    # Cualquier otro carácter
]

# Compilar las expresiones regulares
tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

# Palabras clave del lenguaje
keywords = {
    'main', 'nombre', 'crêpe', 'macaron', 'autre', 'tour_eiffel', 'lire', 'afficher',
    'début', 'fin', 'baguette', 'croissant', 'arc_de_triomphe', 'notre_dame', 
    'champs_elysees', 'louvre', 'versailles', 'tarte_tatin', 'mont_saint_michel', 
    'carcassonne', 'lyon', 'marseille', 'strasbourg', 'bordeaux', 'nantes'
}

# Función para el análisis léxico
def lex(characters):
    line_num = 1
    line_start = 0
    pos = 0
    tokens = []
    mo = get_token(characters)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_num += 1
            line_start = pos
        elif kind == 'SKIP' or kind == 'COMMENT':
            pass
        elif kind == 'ID' and value in keywords:
            kind = value.upper()
            column = mo.start() - line_start
            tokens.append((kind, value, line_num, column))
        elif kind != 'MISMATCH':
            column = mo.start() - line_start
            tokens.append((kind, value, line_num, column))
        else:
            raise RuntimeError('Unexpected character %r on line %d' % (value, line_num))
        pos = mo.end()
        mo = get_token(characters, pos)
    if pos != len(characters):
        raise RuntimeError('Unexpected character %r on line %d' % (characters[pos], line_num))
    return tokens

# Solicitar al usuario que ingrese el código a analizar
print("Por favor, ingrese el código a analizar. Termine la entrada con una línea vacía:")
codigo_entrada = []
while True:
    linea = input()
    if linea == "":
        break
    codigo_entrada.append(linea)

codigo_entrada = "\n".join(codigo_entrada)

# Analizar el código de entrada
tokens = lex(codigo_entrada)
for token in tokens:
    print(token)
