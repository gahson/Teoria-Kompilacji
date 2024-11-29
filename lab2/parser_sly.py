from sly import Parser
from scanner_sly import Scanner

class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'LT', 'GT', 'GE', 'LE', 'EQUAL', 'NOTEQUAL'),
        ("left", '+', '-'),
        ('left', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/'),
        ('left', 'DOTMULT', 'DOTDIV'),
        ('left', "'"),
        ('right', 'ADDASSIGN', 'SUBASSIGN', 'MULTASSIGN', 'DIVASSIGN'),
    )

    @_('instructions_opt')
    def program(self, p):
        pass

    @_('instructions', '')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction', 'instruction')
    def instructions(self, p):
        pass

    @_(" '{' instructions '}' ", "reserved_instruction ';'", "assignment_instruction ';'")
    def instruction(self, p):
        pass

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        pass

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        pass

    @_('FOR var "=" expression ":" expression instruction')
    def instruction(self, p):
        pass

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        pass

    @_('BREAK')
    def reserved_instruction(self, p):
        pass

    @_('CONTINUE')
    def reserved_instruction(self, p):
        pass

    @_('RETURN expression_list')
    def reserved_instruction(self, p):
        pass

    @_('expression_list "," expression', 'expression')
    def expression_list(self, p):
        pass

    @_('PRINT expression_list')
    def reserved_instruction(self, p):
        pass

    @_(
        'var assignment_operator expression',
        'matrix_idx assignment_operator expression',
        'vector_idx assignment_operator expression'
    )
    def assignment_instruction(self, p):
        pass

    @_(
        '"="',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULTASSIGN',
        'DIVASSIGN'
    )
    def assignment_operator(self, p):
        pass

    @_(
       'expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression'
       )
    def expression(self, p):
        pass

    @_(
        'expression DOTADD expression',
        'expression DOTSUB expression',
        'expression DOTMULT expression',
        'expression DOTDIV expression'
        )
    def expression(self, p):
        pass

    @_(
        '"-" expression',
        'expression "\'"'
    )
    def expression(self, p):
        pass

    @_(
        'matrix',
        'vector'
    )
    def expression(self, p):
        pass

    @_(
        'EYE "(" expression ")"',
        'ZEROS "(" expression ")"',
        'ONES "(" expression ")"'
    )
    def expression(self, p):
        pass

    @_('variable')
    def expression(self, p):
        pass

    @_('STRING')
    def expression(self, p):
        pass

    @_('ID')
    def var(self, p):
        pass

    @_(
       'expression EQUAL expression',
       'expression NOTEQUAL expression',
       'expression LT expression',
       'expression GT expression',
       'expression LE expression',
       'expression GE expression'
    )
    def condition(self, p):
        pass

    @_('"[" vectors "]"')
    def matrix(self, p):
        pass

    @_('vectors "," vector', 'vector')
    def vectors(self, p):
        pass

    @_('"[" variables "]"')
    def vector(self, p):
        pass

    @_('variables "," variable', 'variable')
    def variables(self, p):
        pass

    @_('var', 'number', 'vector_idx', 'matrix_idx')
    def variable(self, p):
        pass

    @_('INT', 'FLOAT')
    def number(self, p):
        pass

    @_('var "[" INT "," INT "]"')
    def matrix_idx(self, p):
        pass

    @_('var "[" INT "]"')
    def vector_idx(self, p):
        pass
