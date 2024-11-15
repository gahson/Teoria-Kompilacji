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
        pass

    # instructions_opt -> instructions | ε
    @_('instructions')
    def instructions_opt(self, p):
        pass

    @_('')  # epsilon production
    def instructions_opt(self, p):
        pass

    # instructions -> instructions instruction | instruction
    @_('instructions instruction')
    def instructions(self, p):
        pass

    @_('instruction')
    def instructions(self, p):
        pass

    # instruction -> { instructions } | reserved_instruction ; | assignment_instruction ;
    @_(" '{' instructions '}' ")
    def instruction(self, p):
        pass

    @_("reserved_instruction ';'")  # Simple instruction
    def instruction(self, p):
        pass

    @_("assignment_instruction ';'")  # Assignment instruction
    def instruction(self, p):
        pass

    # reserved_instruction -> IF '(' condition ')' instruction [ ELSE instruction ]
    @_('IF "(" condition ")" instructions %prec IFX')
    def reserved_instruction(self, p):
        pass

    @_('IF "(" condition ")" instructions ELSE instructions')
    def reserved_instruction(self, p):
        pass

    # Loop instructions
    @_('FOR var "=" expression ":" expression instructions')
    def reserved_instruction(self, p):
        pass

    @_('WHILE "(" condition ")" instructions')
    def reserved_instruction(self, p):
        pass

    # Simple reserved instructions
    @_('BREAK')
    def reserved_instruction(self, p):
        pass

    @_('CONTINUE')
    def reserved_instruction(self, p):
        pass

    @_('RETURN expression_list')
    def reserved_instruction(self, p):
        pass
    
    # Expression list for print
    @_('expression_list "," expression')
    def expression_list(self, p):
        pass

    @_('expression')
    def expression_list(self, p):
        pass

    @_('PRINT expression_list')
    def reserved_instruction(self, p):
        pass

    # assignment_instruction -> var '=' expression
    @_('var "=" expression')
    def assignment_instruction(self, p):
        pass

    # Extended assignment instructions
    @_('var ADDASSIGN expression')
    def assignment_instruction(self, p):
        pass

    @_('var SUBASSIGN expression')
    def assignment_instruction(self, p):
        pass

    @_('var MULTASSIGN expression')
    def assignment_instruction(self, p):
        pass

    @_('var DIVASSIGN expression')
    def assignment_instruction(self, p):
        pass

    # Binary expressions
    @_('expression "+" expression')
    def expression(self, p):
        pass

    @_('expression "-" expression')
    def expression(self, p):
        pass

    @_('expression "*" expression')
    def expression(self, p):
        pass

    @_('expression "/" expression')
    def expression(self, p):
        pass

    # Matrix expressions
    @_('expression DOTADD expression')
    def expression(self, p):
        pass

    @_('expression DOTSUB expression')
    def expression(self, p):
        pass

    @_('expression DOTMULT expression')
    def expression(self, p):
        pass

    @_('expression DOTDIV expression')
    def expression(self, p):
        pass

    # Relational expressions using defined tokens
    @_('expression EQUAL expression')
    def condition(self, p):
        pass

    @_('expression NOTEQUAL expression')
    def condition(self, p):
        pass

    @_('expression LT expression')
    def condition(self, p):
        pass

    @_('expression GT expression')
    def condition(self, p):
        pass

    @_('expression LE expression')
    def condition(self, p):
        pass

    @_('expression GE expression')
    def condition(self, p):
        pass
    
    @_('var EQUAL expression')
    def condition(self, p):
        pass

    @_('var NOTEQUAL expression')
    def condition(self, p):
        pass

    @_('var LT expression')
    def condition(self, p):
        pass

    @_('var GT expression')
    def condition(self, p):
        pass

    @_('var LE expression')
    def condition(self, p):
        pass

    @_('var GE expression')
    def condition(self, p):
        pass

    # Unary expressions
    @_('expression "\'"')
    def expression(self, p):
        pass

    @_('"-" expression')
    def expression(self, p):
        pass

    # Matrix functions
    @_('EYE "(" expression ")"')
    def expression(self, p):
        pass

    @_('ZEROS "(" expression ")"')
    def expression(self, p):
        pass

    @_('ONES "(" expression ")"')
    def expression(self, p):
        pass

    # Variable and constants
    @_('INT')
    def expression(self, p):
        pass

    @_('FLOAT')
    def expression(self, p):
        pass

    @_('var')
    def expression(self, p):
        pass

    @_('ID')
    def var(self, p):
        pass

    @_('STRING')
    def expression(self, p):
        pass
