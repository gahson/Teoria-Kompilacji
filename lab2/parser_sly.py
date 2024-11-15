from sly import Parser
from scanner_sly import Scanner

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
        return p.instructions_opt

    # instructions_opt -> instructions | ε
    @_('instructions')
    def instructions_opt(self, p):
        return p.instructions

    @_('')  # epsilon production
    def instructions_opt(self, p):
        return []

    # instructions -> instructions instruction | instruction
    @_('instructions instruction')
    def instructions(self, p):
        return p.instructions + [p.instruction]

    @_('instruction')
    def instructions(self, p):
        return [p.instruction]

    # instruction -> { instructions } | reserved_instruction ; | assignment_instruction ;
    @_(" '{' instructions '}' ")
    def instruction(self, p):
        return p.instructions

    @_("reserved_instruction ';'")  # Simple instruction
    def instruction(self, p):
        return p.reserved_instruction

    @_("assignment_instruction ';'")  # Assignment instruction
    def instruction(self, p):
        return p.assignment_instruction

    # reserved_instruction -> IF '(' condition ')' instruction [ ELSE instruction ]
    @_('IF "(" condition ")" instruction %prec IFX')
    def reserved_instruction(self, p):
        return ('if', p.condition, p.instruction)

    @_('IF "(" condition ")" instruction ELSE instruction')
    def reserved_instruction(self, p):
        return ('if-else', p.condition, p.instruction0, p.instruction1)

    # Loop instructions
    @_('FOR var "=" expression ":" expression instruction')
    def reserved_instruction(self, p):
        return ('for', p.var, p.expression0, p.expression1, p.instruction)

    @_('WHILE "(" condition ")" instruction')
    def reserved_instruction(self, p):
        return ('while', p.condition, p.instruction)

    # Simple reserved instructions
    @_('BREAK')
    def reserved_instruction(self, p):
        return ('break',)

    @_('CONTINUE')
    def reserved_instruction(self, p):
        return ('continue',)

    @_('RETURN expression')
    def reserved_instruction(self, p):
        return ('return', p.expression)

    @_('PRINT expression')
    def reserved_instruction(self, p):
        return ('print', p.expression)

    # assignment_instruction -> var '=' expression
    @_('var "=" expression')
    def assignment_instruction(self, p):
        return ('assign', p.var, p.expression)

    # Extended assignment instructions
    @_('var ADDASSIGN expression')
    def assignment_instruction(self, p):
        return ('add_assign', p.var, p.expression)

    @_('var SUBASSIGN expression')
    def assignment_instruction(self, p):
        return ('sub_assign', p.var, p.expression)

    @_('var MULTASSIGN expression')
    def assignment_instruction(self, p):
        return ('mul_assign', p.var, p.expression)

    @_('var DIVASSIGN expression')
    def assignment_instruction(self, p):
        return ('div_assign', p.var, p.expression)

    # Binary expressions
    @_('expression "+" expression')
    def expression(self, p):
        return ('add', p.expression0, p.expression1)

    @_('expression "-" expression')
    def expression(self, p):
        return ('sub', p.expression0, p.expression1)

    @_('expression "*" expression')
    def expression(self, p):
        return ('mul', p.expression0, p.expression1)

    @_('expression "/" expression')
    def expression(self, p):
        return ('div', p.expression0, p.expression1)

    #Matrix expressions
    @_('expression DOTADD expression')
    def expression(self, p):
        return ('dotadd', p.expression0, p.expression1)

    @_('expression DOTSUB expression')
    def expression(self, p):
        return ('dotsub', p.expression0, p.expression1)

    @_('expression DOTMULT expression')
    def expression(self, p):
        return ('dotmul', p.expression0, p.expression1)

    @_('expression DOTDIV expression')
    def expression(self, p):
        return ('dotdiv', p.expression0, p.expression1)

    # Relational expressions using defined tokens
    @_('expression EQUAL expression')
    def condition(self, p):
        return ('eq', p.expression0, p.expression1)

    @_('expression NOTEQUAL expression')
    def condition(self, p):
        return ('neq', p.expression0, p.expression1)

    @_('expression LT expression')
    def condition(self, p):
        return ('lt', p.expression0, p.expression1)

    @_('expression GT expression')
    def condition(self, p):
        return ('gt', p.expression0, p.expression1)

    @_('expression LE expression')
    def condition(self, p):
        return ('le', p.expression0, p.expression1)

    @_('expression GE expression')
    def condition(self, p):
        return ('ge', p.expression0, p.expression1)

    # Unary expressions
    @_('expression "\'"')
    def expression(self, p):
        return ('transpose', p.expression)

    @_('"-" expression')
    def expression(self, p):
        return ('negate', p.expression)

    # Matrix functions
    @_('EYE "(" expression ")"')
    def expression(self, p):
        return ('eye', p.expression)

    @_('ZEROS "(" expression ")"')
    def expression(self, p):
        return ('zeros', p.expression)

    @_('ONES "(" expression ")"')
    def expression(self, p):
        return ('ones', p.expression)

    # Variable and constants
    @_('INT')
    def expression(self, p):
        return ('number', p.INT)

    @_('FLOAT')
    def expression(self, p):
        return ('float', p.FLOAT)

    @_('var')
    def expression(self, p):
        return ('var', p.var)

    @_('ID')
    def var(self, p):
        return ('id', p.ID)


