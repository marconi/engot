import ply.lex as lex


tokens = (
    'NUMBER',
    'STRING',
    'IDENTIFIER',
    'CONSTANT',
    'INDENT',
    'DEDENT',
    'NEWLINE'
)

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'True': 'TRUE',
    'False': 'FALSE',
    'None': 'NONE'
}

tokens += tuple(reserved.values())

t_ignore = r' \t'
t_CONSTANT = r'\b[A-Z][A-Z0-9_]+\b'
t_INDENT = r'\n[ ]+'
t_DEDENT = r'\n'


def t_IDENTIFIER(t):
    r'\b[a-z_]+\b:?'
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:-1]
    return t


def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)


if __name__ == '__main__':
    lexer = lex.lex()

    # Test it out
    code = """
if morning:
    if before_nine:
        print "breakfast"
    else:
        print "lunch"
else:
    print "dinner"
"""

    # Give the lexer some input
    lexer.input(code.strip())

    for token in lexer:
        print token
