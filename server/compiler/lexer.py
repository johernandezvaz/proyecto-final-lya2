import re
from .tokens import Token, TOKEN_SPEC

def lex(characters: str):
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPEC)
    line_num = 1
    line_start = 0
    tokens = []

    for mo in re.finditer(tok_regex, characters):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        
        if kind == 'SKIP':
            if '\n' in value:
                line_start = mo.end()
                line_num += value.count('\n')
            continue
        elif kind == 'COMMENT':
            continue
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        
        token = Token(kind, value, line_num, column)
        tokens.append(token.to_dict())

    return tokens