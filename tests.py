import unittest
import naivelexer


class NaiveLexerTest(unittest.TestCase):

    def test_number(self):
        lexer = naivelexer.NaiveLexer()
        self.assertEqual([('NUMBER', 1)], lexer.tokenize("1"))

    def test_string(self):
        lexer = naivelexer.NaiveLexer()
        self.assertEqual([('STRING', 'hello')], lexer.tokenize('"hello"'))

    def test_identifier(self):
        lexer = naivelexer.NaiveLexer()
        self.assertEqual([('IDENTIFIER', 'age')], lexer.tokenize('age'))
        self.assertEqual([('IDENTIFIER', 'age_limit')], lexer.tokenize('age_limit'))

    def test_constant(self):
        lexer = naivelexer.NaiveLexer()
        self.assertEqual([('CONSTANT', 'MAX')], lexer.tokenize('MAX'))
        self.assertEqual([('CONSTANT', 'MAX_NUM')], lexer.tokenize('MAX_NUM'))

    def test_operator(self):
        lexer = naivelexer.NaiveLexer()
        self.assertEqual([('+', '+')], lexer.tokenize('+'))
        self.assertEqual([('&&', '&&')], lexer.tokenize('&&'))

    def test_indent(self):
        lexer = naivelexer.NaiveLexer()
        code = """
if morning:
    if before_nine:
        print "breakfast"
    else:
        print "lunch"
else:
    print "dinner"
"""

        tokens = [
            ('IF', 'if'), ('IDENTIFIER', 'morning'),
            ('INDENT', 4),
                ('IF', 'if'), ('IDENTIFIER', 'before_nine'),
                ('INDENT', 8),
                    ('IDENTIFIER', 'print'), ('STRING', 'breakfast'),
                ('DEDENT', 4), ('NEWLINE', "\n"),
                ('ELSE', 'else'),
                ('INDENT', 8),
                    ('IDENTIFIER', 'print'), ('STRING', 'lunch'),
                ('DEDENT', 0), ('NEWLINE', "\n"),
            ('ELSE', 'else'),
            ('INDENT', 4),
                ('IDENTIFIER', 'print'), ('STRING', 'dinner'), ('DEDENT', 0)
        ]

        self.assertEqual(tokens, lexer.tokenize(code))


if __name__ == '__main__':
    unittest.main()
