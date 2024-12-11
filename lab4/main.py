import sys
from scanner_sly import Scanner
from parser_sly import Mparser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "examples/control_transfer.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    text = file.read()
    lexer = Scanner()
    parser = Mparser()

    ast = parser.parse(lexer.tokenize(text))
    ast.printTree()
    # Below code shows how to use visitor
    typeChecker = TypeChecker()   
    typeChecker.visit(ast)   # or alternatively ast.accept(typeChecker)