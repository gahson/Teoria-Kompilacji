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

    '''
    [0] = p[1] - w parserach opartych na narzędziach takich jak PLY (Python Lex-Yacc)
    chcemy przekazywać wartości między poziomami reguł w trakcie parsowania. 
    '''
    # program -> instructions_opt
    @_('instructions_opt')
    def program(self, p):
        p[0] = p[1]

    # instructions_opt -> instructions | ε
    @_('instructions', '')
    def instructions_opt(self, p):
        p[0] = p[1]

    # instructions -> instructions instruction | instruction
    @_('instructions instruction', 'instruction')
    def instructions(self, p):
        if len(p) == 2:
            p[0] = AST.InstructionsOne(p[1])
        elif len(p) == 3:
            p[0] = AST.InstructionsList(p[1], p[2])

    # instruction -> { instructions } | reserved_instruction ; | assignment_instruction ;
    @_(" '{' instructions '}' ", "reserved_instruction ';'", "assignment_instruction ';'")
    def instruction(self, p):
        if len(p) == 4:
            p[0] = p[2]
        elif len(p) == 3:
            p[0] = p[1]
    
    # instruction -> IF '(' condition ')' instruction
    @_('IF "(" condition ")" instruction %prec IFX')
    def instruction(self, p):
        p[0] = AST.If(p[3], p[5])
    
    # instruction -> IF '(' condition ')' instruction ELSE instruction
    @_('IF "(" condition ")" instruction ELSE instruction')
    def instruction(self, p):
        p[0] = AST.IfElse(p[3], p[5], p[7])

    # instruction -> FOR var "=" expression ":" expression instruction
    @_('FOR var "=" expression ":" expression instruction')
    def instruction(self, p):
        p[0] = AST.For(p[2], p[4], p[6], p[7])

    # instruction -> WHILE "(" condition ")" instruction
    @_('WHILE "(" condition ")" instruction')
    def instruction(self, p):
        p[0] = AST.While(p[3], p[5])

    # reserved_instruction -> BREAK
    @_('BREAK')
    def reserved_instruction(self, p):
        p[0] = AST.Break()
    
    # reserved_instruction -> CONTINUE
    @_('CONTINUE')
    def reserved_instruction(self, p):
        p[0] = AST.Continue()

    # reserved_instruction -> RETURN expression_list
    @_('RETURN expression_list')
    def reserved_instruction(self, p):
        p[0] = AST.Return(p[2])
    
    # expression_list -> expression_list "," expression
    @_('expression_list "," expression')
    def expression_list(self, p):
        p[0] = AST.ExpressionList(p[2], p[4])

    # expression_list -> expression
    @_('expression')
    def expression_list(self, p):
        p[0] = AST.ExpressionOne(p[1])

    # reserved_instruction -> PRINT expression_list
    @_('PRINT expression_list')
    def reserved_instruction(self, p):
        p[0] = AST.Print(p[2])

    # assignment_instruction -> var assignment_operator expression | 
    # matrix_idx assignment_operator expression | vector_idx assignment_operator expression
    @_(
        'var assignment_operator expression',
        'matrix_idx assignment_operator expression',
        'vector_idx assignment_operator expression'
    )
    def assignment_instruction(self, p):
        p[0] = AST.AssignmentInstruction(p[1], p[2], p[3])

    # assignment_operator -> "=" | ADDASSIGN | SUBASSIGN | MULTASSIGN | DIVASSIGN
    @_(
        '"="',
        'ADDASSIGN',
        'SUBASSIGN',
        'MULTASSIGN',
        'DIVASSIGN'
    )
    def assignment_operator(self, p):
        p[0] = p[1]

    # Binary expressions
    @_(
       'expression "+" expression',
       'expression "-" expression',
       'expression "*" expression',
       'expression "/" expression'
       )
    def expression(self, p):
        p[0] = AST.BinaryExpression(p[1], p[2], p[3])

    # Matrix expressions
    @_(
        'expression DOTADD expression',
        'expression DOTSUB expression',
        'expression DOTMULT expression',
        'expression DOTDIV expression'
        )
    def expression(self, p):
        p[0] = AST.MatrixExpression(p[0], p[1], p[2])

    # Unary expressions
    @_(
        '"-" expression',
        'expression "\'"'
    )
    def expression(self, p):
        if p[1] == '-':
            p[0] = AST.UnaryMinus(p[2])
        else:
            p[0] = AST.UnaryTranspose(p[1])
    
    @_(
        'matrix',
        'vector'
    )
    def expression(self, p):
        p[0] = p[1]

    # Matrix functions
    @_(
        'EYE "(" expression ")"',
        'ZEROS "(" expression ")"',
        'ONES "(" expression ")"'
    )
    def expression(self, p):
        p[0] = AST.Function(p[3])

    @_('variable')
    def expression(self, p):
        p[0] = p[1]
    
    @_('STRING')
    def expression(self, p):
        p[0] = p[1]
    
    @_('ID')
    def var(self, p):
        p[0] = p[1]
    
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
        p[0] = AST.Condition(p[1], p[2], p[3])
    
    @_('"[" vectors "]"')
    def matrix(self, p):
        p[0] = p[2]
    
    @_('vectors "," vector', 'vector')
    def vectors(self, p):
        if len(p) == 4:
            p[0] = AST.VectorsList(p[1], p[3])
        else:
            p[0] = AST.VectorsOne(p[1])
    
    @_('"[" variables "]"')
    def vector(self, p):
        p[0] = p[2]
    
    @_('variables "," variable', 'variable')
    def variables(self, p):
        if len(p) == 4:
            p[0] = AST.VariablesList(p[1], p[3])
        else:
            p[0] = AST.VariablesOne(p[1])
    
    @_('var', 'INT', 'FLOAT', 'vector_idx', 'matrix_idx')
    def variable(self, p):
        p[0] = p[1]
    
    @_('var "[" INT "," INT "]"')
    def matrix_idx(self, p):
        p[0] = AST.MatrixIdx(p[1], p[3], p[5])
    
    @_('var "[" INT "]"')
    def vector_idx(self, p):
        p[0] = AST.VectorIdx(p[1], [3])
    
    
    
