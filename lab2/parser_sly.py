from sly import Parser
from scanner_sly import Scanner



class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
        ('nonassoc', 'IFX'), # Z prezenacji
        ('nonassoc', 'ELSE'),
    # to fill ...
    )

    # program -> instructions_opt
    @_('instructions_opt')
    def program(p):
        pass

    # instructions_opt -> instructions
    @_('instructions')
    def instructions_opt(p):
        pass

    # instructions_opt -> 
    @_('')
    def instructions_opt(p):
        pass
    
    # instructions -> instructions instruction
    @_('instructions instruction')
    def instructions(p):
        pass

    # instructions -> instruction
    @_('instruction')
    def instructions(p):
        pass
    
    # instruction -> { instructions } | reserved_instruction ; | assigment_instruction ;
    @_(" '{' instructions '}' ", 
       "reserved_instruction ';'",
       "assignment_instructions ';'")
    def instruction(p):
        pass
    
    # Rozdzielam słowa kluczowe, bo każde potem będzie wykonywało
    # inną akcję
    
    @_("IF '(' condition ')' instruction %prec IFX") # z prezentacji
    def reserved_instruction(p):
        pass
    
    @_("IF '(' condition ')' instruction ELSE instruction") # z prezentacji
    def reserved_instruction(p):
        pass
    
    # instruction, nie instructions, bo instruction -> { instructions }
    @_("FOR var '=' expression ':' expression instruction ")
    def reserved_instruction(p):
        pass
    # instruction, nie instructions, bo instruction -> { instructions }
    @_("WHILE '(' condition ')' instruction")
    def reserved_instruction(p):
        pass
    
    @_("BREAK")
    def reserved_instruction(p):
        pass
    
    @_("CONTINUE")
    def reserved_instruction(p):
        pass
    
    @_("RETURN")
    def reserved_instruction(p):
        pass
    
    @_("EYE")
    def reserved_instruction(p):
        pass
    
    @_("ZEROS")
    def reserved_instruction(p):
        pass
    
    @_("ONES")
    def reserved_instruction(p):
        pass
        
    @_("PRINT")
    def reserved_instruction(p):
        pass

    # do uzupełnienia
    @_('')
    def assignment_instructions(p):
        pass
    
    @_('')
    def condition(p):
        pass
    
    @_('')
    def var(p):
        pass
    
    @_('')
    def expression(p):
        pass

    # to finish the grammar
    # ....

