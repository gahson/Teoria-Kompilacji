#!/usr/bin/python
import AST
from collections import defaultdict
from SymbolTable import *

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

arithmetic_operators = ['+', '+=', '-', '-=', '*', '*=', '/', '/=']
matrix_operators = ['.+', '.=', '/*', './']
boolean_operators = ['==', '!=', '<', '<=', '>', '>=', ]


for arithmetic_operator in arithmetic_operators:
    ttype[arithmetic_operator]['int']['int'] = 'int'
    ttype[arithmetic_operator]['float']['float'] = 'float'
    ttype[arithmetic_operator]['int']['float'] = 'float'
    ttype[arithmetic_operator]['float']['int'] = 'float'
    #ttype[op]['matrix']['matrix'] = 'matrix'
    #ttype[op]['vector']['vector'] = 'vector'

for matrix_operator in matrix_operators:
    ttype[matrix_operator]['matrix']['matrix'] = 'matrix'
    ttype[matrix_operator]['matrix']['int'] = 'matrix'
    ttype[matrix_operator]['matrix']['float'] = 'matrix'
    ttype[matrix_operator]['matrix']['vector'] = 'matrix'
    ttype[matrix_operator]['vector']['vector'] = 'vector'
    ttype[matrix_operator]['vector']['int'] = 'vector' 
    ttype[matrix_operator]['vector']['float'] = 'vector'

for boolean_operator in boolean_operators:
    ttype[boolean_operator]['int']['int'] = 'bool'
    ttype[boolean_operator]['float']['float'] = 'bool'
    ttype[boolean_operator]['int']['float'] = 'bool'
    ttype[boolean_operator]['float']['int'] = 'bool'
    
ttype['+']['string']['string'] = 'string'
ttype['+=']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'
ttype['*']['int']['string'] = 'string'

def get_type(operator, left, right):
    if operator in ttype:
            if left.type in ttype[operator]:
                if right.type in ttype[operator][left.type]:
                    return ttype[operator][left.type][right.type]
    return None
    
    
    
class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

    # simpler version of generic_visit, not so general
    #def generic_visit(self, node):
    #    for child in node.children:
    #        self.visit(child)



class TypeChecker(NodeVisitor):
    
    def __init__(self):
        self.table = SymbolTable(None, 'Program')
        self.nested_loops = 0

    def visit_Program(self, node):
        self.visit(node.instructions)
        
    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)
            
    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.instruction)
        
    def visit_IfElse(self, node):
        self.visit(node.condition)
        self.visit(node.instruction1)
        self.visit(node.instruction2)
        
    def visit_For(self, node):
        self.visit(node.var)
        self.visit(node.expression1)
        self.visit(node.expression2)
        self.nested_loops += 1
        self.visit(node.instruction)
        self.nested_loops -= 1
        
    def visit_While(self, node):
        self.visit(node.condition)
        self.nested_loops += 1
        self.visit(node.instruction)
        self.nested_loops -= 1
        
    def visit_Break(self, node):
        if self.nested_loops == 0:
            print(f"Line {-1}: 'Break' used outside of loop!")
            
    def visit_Continue(self, node):
        if self.nested_loops == 0:
            print(f"Line {-1}: 'Continue' used outside of loop!")
            
    def visit_Return(self, node):
        for expression in node.expression_list:
            self.visit(expression)
            
    def visit_Expressions(self, node):
        for expression in node.expressions:
            self.visit(expression)
            
    def visit_Print(self, node):
        for expression in node.expression_list:
            self.visit(expression)
            
    def visit_AssignmentInstruction(self, node):
        left = self.visit(node.lhs)
        operator = node.operator
        right = self.visit(node.expression)
        
        assignment_type = get_type(operator, left, right)

        if assignment_type is not None:
            if assignment_type is not 'matrix':
                