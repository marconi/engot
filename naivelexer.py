import re
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("NaiveLexer")


class TokenMatcher(object):
    def __init__(self):
        self.result = None

    def check(self, pattern, value):
        self.result = re.match(pattern, value)
        return self.result


class NaiveLexer:

    KEYWORDS = ['def', 'class', 'if', 'else', 'True', 'False', 'None']

    def tokenize(self, code):
        code = code.strip()
        code_cursor = 0
        tokens = []
        current_indent = 0
        indent_stack = []
        matcher = TokenMatcher()

        while code_cursor < len(code):
            chunk = code[code_cursor:]

            if matcher.check('^([a-z]\w*)', chunk):
                identifier = matcher.result.group()
                if identifier in NaiveLexer.KEYWORDS:
                    tokens.append((identifier.upper(), identifier))
                else:
                    tokens.append(('IDENTIFIER', identifier))
                code_cursor += len(identifier)

            elif matcher.check('^([A-Z]\w*)', chunk):
                constant = matcher.result.group()
                tokens.append(('CONSTANT', constant))
                code_cursor += len(constant)

            elif matcher.check('^(\d+)', chunk):
                number = matcher.result.group()
                tokens.append(('NUMBER', int(number)))
                code_cursor += len(number)

            elif matcher.check('^"(.*?)"', chunk):
                string = matcher.result.group(1)
                tokens.append(('STRING', string))
                code_cursor += len(string) + 2

            elif matcher.check('^\:\n( +)', chunk):
                indent = len(matcher.result.group(1))
                if indent <= current_indent:
                    raise Exception("Bad Indent: got %s instead of > %s" % (
                        str(indent), str(current_indent)))
                current_indent = indent
                indent_stack.append(current_indent)
                tokens.append(('INDENT', indent))
                code_cursor += indent + 2

            elif matcher.check('^\n( *)', chunk):
                indent = len(matcher.result.group(1))
                if indent == current_indent:
                    tokens.append(('NEWLINE', "\n"))
                elif indent < current_indent:
                    while indent < current_indent:
                        indent_stack.pop()
                        try:
                            current_indent = indent_stack[-1]
                        except IndexError:
                            current_indent = 0
                            break
                        tokens.append(('DEDENT', indent))
                    tokens.append(('NEWLINE', "\n"))
                else:
                    raise Exception("Cannot indent without code block")
                code_cursor += indent + 1

            elif matcher.check('^(\|\||&&|==|!=|<=|>=)', chunk):
                operator = matcher.result.group()
                tokens.append((operator, operator))
                code_cursor += len(operator)

            elif matcher.check('^ ', chunk):
                code_cursor += 1

            else:
                value = chunk[0: 1]
                tokens.append((value, value))
                code_cursor += 1

        while len(indent_stack) > 0:
            indent_stack.pop()
            try:
                tokens.append(('DEDENT', indent_stack[0]))
            except IndexError:
                tokens.append(('DEDENT', 0))

        return tokens
