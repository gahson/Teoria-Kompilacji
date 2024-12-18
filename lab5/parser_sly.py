from sly import Parser
from scanner_sly import Scanner
import AST

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
        return p[0]

    @_('instructions')
    def instructions_opt(self, p):
        return p[0]
    
    @_('')
    def instructions_opt(self, p):
        pass

    @_('instructions instruction', 'instruction')
    def instructions(self, p):        
        if len(p) == 1:
            return AST.Instructions([p[0]])
        elif len(p) == 2:
            return AST.Instructions(p[0].instructions + [p[1]])

    @_(" '{' instructions '}' ", "reserved_instruction ';'", "assignment_instruction ';'")
    def instruction(self, p):
        if len(p) == 3:
            return p[1]
        elif len(p) == 2:
            return p[0]

    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p[2], p[4])

    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.IfElse(p[2], p[4], p[6])

    @_('FOR var "=" expression ":" expression instruction')
    def instruction(self, p):
        return AST.For(p[1], p[3], p[5], p[6])

    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.While(p[2], p[4])

    @_('BREAK')
    def reserved_instruction(self, p):
        return AST.Break(p.lineno)
    
    @_('CONTINUE')
    def reserved_instruction(self, p):
        return AST.Continue(p.lineno)

    @_('RETURN expression_list')
    def reserved_instruction(self, p):
        return AST.Return(p[1])

    @_('expression_list "," expression', 'expression')
    def expression_list(self, p):
        if len(p) == 3:
            return AST.Expressions(p[0].expressions + [p[2]])
        else:
            return AST.Expressions([p[0]])

    @_('PRINT expression_list')
    def reserved_instruction(self, p):
        return AST.Print(p[1])

    @_(
        'var assignment_operator expression',
        'matrix_idx assignment_operator expression'
    )
    def assignment_instruction(self, p):
        return AST.AssignmentInstruction(p[0], p[1], p[2], p.lineno)

    @_(
        '"="',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULTASSIGN',
        'DIVASSIGN'
    )
    def assignment_operator(self, p):
        return p[0]

    @_(
       'expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression',
       )
    def expression(self, p):
        return AST.OperatorExpression(p[0], p[1], p[2], p.lineno)

    @_(
        'expression DOTADD expression',
        'expression DOTSUB expression',
        'expression DOTMULT expression',
        'expression DOTDIV expression'
        )
    def expression(self, p):
        return AST.OperatorExpression(p[0], p[1], p[2], p.lineno)

    @_(
        '"-" expression',
        'expression "\'"',
    )
    def expression(self, p):
        if p[0] == '-':
            return AST.UnaryMinus(p[1], p.lineno)
        else:
            return AST.UnaryTranspose(p[0], p.lineno)
    
    @_(
        '"(" expression ")"'
    )
    def expression(self, p):
        return p[1]
    
    @_(
        'matrix',
        'vector'
    )
    def expression(self, p):
        return p[0]

    @_(
        'EYE "(" expression_list ")"',
        'ZEROS "(" expression_list ")"',
        'ONES "(" expression_list ")"'
    )
    def expression(self, p):
        return AST.Function(p[0], p[2], p.lineno)

    @_('variable')
    def expression(self, p):
        return p[0]
    
    @_('ID')
    def var(self, p):
        return AST.Id(p[0])

    @_(
       'expression EQUAL expression',
       'expression NOTEQUAL expression',
       'expression LT expression',
       'expression GT expression',
       'expression LE expression',
       'expression GE expression'
    )
    def condition(self, p):
        return AST.Condition(p[0], p[1], p[2], p.lineno)
    
    @_('"[" vectors "]"')
    def matrix(self, p):
        return p[1]
    
    @_('vectors "," vector', 'vector')
    def vectors(self, p):
        if len(p) == 3:
            return AST.Vectors(p[0].vectors + [p[2]], p.lineno)
        else:
            return AST.Vectors([p[0]], p.lineno)
    
    @_('"[" variables "]"')
    def vector(self, p):
        return AST.Vector(p[1], p.lineno)
    
    @_('variables "," variable', 'variable')
    def variables(self, p):
        if len(p) == 3:
            return AST.Variables(p[0].variables + [p[2]])
        else:
            return AST.Variables([p[0]])
    
    @_('var', 'number', 'matrix_idx', 'string')
    def variable(self, p):
        return p[0]
    
    @_('INT')
    def number(self, p):
        return AST.IntNumber(p[0])
    
    @_('FLOAT')
    def number(self, p):
        return AST.FloatNumber(p[0])
    
    @_('STRING')
    def string(self, p):
        return AST.String(p[0])
    
    #@_('STRING')
    #def expression(self, p):
    #    return AST.String(p[0])
    
    @_('var "[" variables "]"')
    def matrix_idx(self, p):
        return AST.MatrixIdx(p[0], p[2], p.lineno)
    
    
