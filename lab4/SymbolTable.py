#!/usr/bin/python
import copy

class VariableSymbol(object):
    def __init__(self, symbol_name, symbol_type):
        self.symbol_name = symbol_name
        self.symbol_type = symbol_type

class FunctionSymbol(object):
    def __init__(self, symbol_name, function_args):
        self.symbol_name = symbol_name
        self.symbol_type = "function"
        self.function_args = function_args

class MatrixSymbol(object):
    def __init__(self, symbol_name, matrix_dimensions):
        self.symbol_name = symbol_name
        self.symbol_type = 'matrix'
        self.matrix_dimensions = matrix_dimensions

class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.table = dict()

    def put(self, name, symbol):
        self.table.update({name: symbol})

    def get(self, name):
        return self.table.get(name, None)
    
    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        new_scope = SymbolTable(parent=self, name=name)
        new_scope.table = clone = copy.deepcopy(self.table)
        return new_scope
    
    def popScope(self):
        return self.parent

