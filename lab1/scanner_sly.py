import sys
from sly import Lexer


class Scanner(Lexer):

    tokens={ID, DOTADD, DOTSUB, DOTMULT, DOTDIV, ADDASSIGN, SUBASSIGN, MULTASSIGN, 
            DIVASSIGN,LT, GT, NOTEQUAL, EQUAL, IF, ELSE, FOR,
              WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT,INT,
            FLOAT, STRINGS    }
    literals = [ '+', '-', '*', '/','=','<','>','(',')','[',']','{','}',',',':',';','\'' ]

    ignore=' \t\n'
    ignore_comment=r'#.*\n'
    igonre_comment2=R'\'\'\'.*\'\'\''

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    DOTADD=r'\.\+'
    DOTSUB=r'\.-'
    DOTMULT=r'\.\*'
    DOTDIV=r'\./'
    ADDASSIGN=r'\+='
    SUBASSIGN=r'-='
    MULTASSIGN=r'\*='
    DIVASSIGN=r'/='
    LT=r'<='
    GT=r'>='
    NOTEQUAL=r'!='
    EQUAL=r'=='
    IF=r'if'
    ELSE=r'else'
    FOR=r'for'
    WHILE=r'while'
    BREAK=r'break'
    CONTINUE=r'continue'
    RETURN=r'return'
    EYE=r'eye'
    ZEROS=r'zeros'
    ONES=r'ones'
    PRINT= r'print'
    INT=r'\d+'
    FLOAT=r'\d+\.\d*'
    STRING=r'\".*?\"'

    pass





if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    
    for tok in lexer.tokenize(text):
        print(tok)
