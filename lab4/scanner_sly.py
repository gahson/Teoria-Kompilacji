import sys
from sly import Lexer


class Scanner(Lexer):

    # Słowa kluczowe
    reserved = {IF, ELSE, FOR, WHILE, BREAK, CONTINUE, RETURN, EYE, ZEROS, ONES, PRINT}

    # Tokeny
    tokens={ID, DOTADD, DOTSUB, DOTMULT, DOTDIV, ADDASSIGN, SUBASSIGN, MULTASSIGN, 
            DIVASSIGN,LT, GT, GE, LE, NOTEQUAL, EQUAL, INT,
            FLOAT, STRING} | reserved
    
    # Literał, zwracany przez lexer w takiej samej postaci
    literals = [ '+', '-', '*', '/','=','<','>','(',')','[',']','{','}',',',':',';','\'' ]
    
    # Z teści zadania:
    # Następujące znaki powinny być pomijane:
    #     białe znaki: spacje, tabulatory, znaki nowej linii
    #     komentarze: komentarze rozpoczynające się znakiem # do znaku końca linii
    ignore=' \t'
    ignore_comment=r'#.*'
    #igonre_comment2=R'\'\'\'.*\'\'\''
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # https://sly.readthedocs.io/en/latest/sly.html#token-remapping
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT

    DOTADD=r'\.\+'
    DOTSUB=r'\.-'
    DOTMULT=r'\.\*'
    DOTDIV=r'\./'
    ADDASSIGN=r'\+='
    SUBASSIGN=r'-='
    MULTASSIGN=r'\*='
    DIVASSIGN=r'/='
    GE=r'>='
    LE=r'<='
    LT=r'<'
    GT=r'>'
    NOTEQUAL=r'!='
    EQUAL=r'=='
    

    
    # https://sly.readthedocs.io/en/latest/sly.html#adding-match-actions
    
    # FLOAT musi być dopasowany przed INT'em, bo może dojść do sytuacji, że:
    # dopasujemy 60.5 do INT jeśli najpierw sprawdzimy r'\d+'
    @_(r'((\d+\.\d*|\.\d+)([eE][-+]?\d+)?)|(\d+)([eE][-+]?\d+)')
    def FLOAT(self, t):
        t.value = float(t.value)
        return t
    
    @_(r'\d+')
    def INT(self, t):
        t.value = int(t.value)
        return t

    @_(r'\".*?\"')
    def STRING(self, t):
        t.value = str(t.value)
        return t
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value) # Zliczamy, w której lini jesteśmy
        
    def error(self, t):
        print(f"Unknown character at ({t.lineno}) line'{t.value[0]}'")
        self.index += 1 # Skip do następnego znaku zamiast domyślnego rzucenia wyjątku

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example_full.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    
    for tok in lexer.tokenize(text):
        print(tok)