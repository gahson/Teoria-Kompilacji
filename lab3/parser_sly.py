from sly import Parser
from scanner_sly import Scanner
import AST

class Mparser(Parser):
    tokens = Scanner.tokens
    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'IFX'),  # dla niejednoznaczności if-else
        ('nonassoc', 'ELSE'),
        ('nonassoc', 'LT', 'GT', 'GE', 'LE', 'EQUAL', 'NOTEQUAL'),
        ("left", '+', '-'),
        ('left', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/'),
        ('left', 'DOTMULT', 'DOTDIV'),
        ('left', "'"),
        ('right', 'ADDASSIGN', 'SUBASSIGN', 'MULTASSIGN', 'DIVASSIGN'),
    )

    # program -> instructions_opt
    @_('instructions_opt')
    def program(self, p):
        return p[0]

    # instructions_opt -> instructions | ε
    @_('instructions', '')
    def instructions_opt(self, p):
        return p[0]

    # instructions -> instructions instruction | instruction
    @_('instructions instruction', 'instruction')
    def instructions(self, p):        
        if len(p) == 1:
            return AST.Instructions([p[0]])
        elif len(p) == 2:
            return AST.Instructions(p[0].instructions + [p[1]])

    # instruction -> { instructions } | reserved_instruction ; | assignment_instruction ;
    @_(" '{' instructions '}' ", "reserved_instruction ';'", "assignment_instruction ';'")
    def instruction(self, p):
        if len(p) == 3:
            return p[1]
        elif len(p) == 2:
            return p[0]
    
    # instruction -> IF '(' condition ')' instruction
    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        return AST.If(p[2], p[4])
    
    # instruction -> IF '(' condition ')' instruction ELSE instruction
    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        return AST.IfElse(p[2], p[4], p[6])

    # instruction -> FOR var "=" expression ":" expression instruction
    @_('FOR var "=" expression ":" expression instruction')
    def instruction(self, p):
        return AST.For(p[1], p[3], p[5], p[6])

    # instruction -> WHILE "(" condition ")" instruction
    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        return AST.While(p[2], p[4])

    # reserved_instruction -> BREAK
    @_('BREAK')
    def reserved_instruction(self, p):
        return AST.Break()
    
    # reserved_instruction -> CONTINUE
    @_('CONTINUE')
    def reserved_instruction(self, p):
        return AST.Continue()

    # reserved_instruction -> RETURN expression_list
    @_('RETURN expression_list')
    def reserved_instruction(self, p):
        return AST.Return(p[1])
    
    # expression_list -> expression_list "," expression
    @_('expression_list "," expression')
    def expression_list(self, p):
        return AST.ExpressionList(p[0], p[2])

    # expression_list -> expression
    @_('expression')
    def expression_list(self, p):
        return AST.ExpressionOne(p[0])

    # reserved_instruction -> PRINT expression_list
    @_('PRINT expression_list')
    def reserved_instruction(self, p):
        return AST.Print(p[1])

    # assignment_instruction -> var assignment_operator expression | 
    # matrix_idx assignment_operator expression | vector_idx assignment_operator expression
    @_(
        'var assignment_operator expression',
        'matrix_idx assignment_operator expression',
        'vector_idx assignment_operator expression'
    )
    def assignment_instruction(self, p):
        return AST.AssignmentInstruction(p[0], p[1], p[2])

    # assignment_operator -> "=" | ADDASSIGN | SUBASSIGN | MULTASSIGN | DIVASSIGN
    @_(
        '"="',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULTASSIGN',
        'DIVASSIGN'
    )
    def assignment_operator(self, p):
        return p[0]

    # Binary expressions
    @_(
       'expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression'
       )
    def expression(self, p):
        return AST.BinaryExpression(p[0], p[1], p[2])

    # Matrix expressions
    @_(
        'expression DOTADD expression',
        'expression DOTSUB expression',
        'expression DOTMULT expression',
        'expression DOTDIV expression'
        )
    def expression(self, p):
        return AST.MatrixExpression(p[0], p[1], p[2])

    # Unary expressions
    @_(
        '"-" expression',
        'expression "\'"'
    )
    def expression(self, p):
        if p[1] == '-':
            return AST.UnaryMinus(p[1])
        else:
            return AST.UnaryTranspose(p[0])
    
    @_(
        'matrix',
        'vector'
    )
    def expression(self, p):
        return p[0]

    # Matrix functions
    @_(
        'EYE "(" expression ")"',
        'ZEROS "(" expression ")"',
        'ONES "(" expression ")"'
    )
    def expression(self, p):
        return AST.Function(p[0], p[2])

    @_('variable')
    def expression(self, p):
        return p[0]
    
    @_('STRING')
    def expression(self, p):
        return p[0]
    
    @_('ID')
    def var(self, p):
        return AST.Id(p[0])
    
    # Relational expressions using defined tokens
    @_(
       'expression EQUAL expression',
       'expression NOTEQUAL expression',
       'expression LT expression',
       'expression GT expression',
       'expression LE expression',
       'expression GE expression'
    )
    def condition(self, p):
        return AST.Condition(p[0], p[1], p[2])
    
    @_('"[" vectors "]"')
    def matrix(self, p):
        return p[1]
    
    @_('vectors "," vector', 'vector')
    def vectors(self, p):
        if len(p) == 3:
            return AST.Vectors(p[0].vectors + [p[2]])
        else:
            return AST.Vectors([p[0]])
    
    @_('"[" variables "]"')
    def vector(self, p):
        return AST.Vector(p[1])
    
    @_('variables "," variable', 'variable')
    def variables(self, p):
        if len(p) == 3:
            return AST.Variables(p[0].variables + [p[2]])
        else:
            return AST.Variables([p[0]])
    
    @_('var', 'number', 'vector_idx', 'matrix_idx')
    def variable(self, p):
        return p[0]
    
    @_('INT', 'FLOAT')
    def number(self, p):
        return AST.Number(p[0])
    
    @_('var "[" INT "," INT "]"')
    def matrix_idx(self, p):
        return AST.MatrixIdx(p[0], p[2], p[4])
    
    @_('var "[" INT "]"')
    def vector_idx(self, p):
        return AST.VectorIdx(p[0], [2])
    
    
    
