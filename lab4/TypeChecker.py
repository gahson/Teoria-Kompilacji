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
    
def get_dimensions(operator, left, right):

        if operator == '=':
            return right.dimensions
        if operator in ['+', '-', '+=', '-=', '*=', '/=', '.+', '.-', '/*', './']:
            if left.dimensions == right.dimensions:
                return left.dimensions
        if operator =='*':
            if left.dimensions[1] == right.dimensions[0]:
                return [left.dimensions[0], right.dimensions[1]]
        if operator == '/':
            return [left.dimensions[0], right.dimensions[1]]
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
        if node.expression_list:
            self.visit(node.expression_list)
            
    def visit_Expressions(self, node):
        if node.expressions:
            self.visit(node.expressions)
            
    def visit_Print(self, node):
        if node.expression_list:
            self.visit(node.expression_list)
    
    
    def visit_AssignmentInstruction(self, node):
        left = self.visit(node.lhs)
        operator = node.assignment_operator
        right = self.visit(node.expression)

        assignment_type = get_type(operator, left, right)

        if assignment_type is not None:
            if assignment_type != 'matrix':
                self.table.put(left.name, VariableSymbol(left.name, right.type))
            else: # jest macierzą
                if get_dimensions(operator, left, right) is not None:
                    self.table.put(left.name, ArraySymbol(left.name, right.dimensions))
                else:
                    print(f"Line {-1}: Wrong assignment operation!")
        elif isinstance(left, VariableSymbol) and isinstance(right, ArraySymbol):
            new_l = ArraySymbol(left.name, right.dimensions)
            self.table.put(left.name, new_l)
        elif isinstance(left, VariableSymbol):
            #print(node.expression)
            left.type = right.type
        else:
            print("Line {}: Wrong Assignment".format(node.line) + str(left) + operator + str(right))
            
 
    
    
    def visit_OperatorExpression(self, node):
        
        left = self.visit(node.expression1)
        op = node.operator
        right = self.visit(node.expression2)
        _type = get_type(op, left, right)
        if _type == 'matrix':
            dims = get_dimensions(op, left, right)
            if dims is None:
                print(f"Line {-1}: Wrong dimensions {left.dimensions} and {right.dimensions} doesn't match!")
                return ArraySymbol(None, None)
            else:
                return ArraySymbol(None, dims)
        elif _type is None:
            print(f"Line -1: Wrong Binary Expression! Can't perform '{op}' on '{left.type}' and '{right.type}'")
        return VariableSymbol(None, _type)
    
    # Trzeba sprawdzić, czy minus jest ustawiony przez wartością liczbową
    def visit_UnaryMinus(self, node):
        if self.visit(node.expression) not in ['int', 'float']:
            print(f"Line {-1}: Unary minus operator can only be applied to a number!")
    
    # Trzeba sprawdzić, czy transpozycja jest wywołana na macierzy
    def visit_UnaryTranspose(self, node):
        if self.visit(node.expression) != ArraySymbol.__class__:
            print(f"Line {-1}: Transposition only work on matrices!")
    
    # Trzeba sprawdzić, czy argument funkcji jest int'em
    def visit_Function(self, node):
        
        # Ma być dokładnie jeden argument
        if len(node.expression.expressions) != 1:
            print(f"Line {-1}: Wrong number of arguments")
        else:
            #Skoro jest jeden argument to sprawdzam, czy jest int'em
            if self.visit(node.expression.expressions[0]).type != 'int':
                 print(f"Line {-1}: Function argument must be an integer!")
            else:
                return ArraySymbol(None, [node.expression.expressions[0].int_number, node.expression.expressions[0].int_number])
        return ArraySymbol(None, [])
    # Trzeba sprawdzić, czy condition może zwrócić bool'a
    def visit_Condition(self, node):
        left = self.visit(node.expression1)
        operator = node.operator
        right = self.visit(node.expression2)

        if self.operations.get_type(operator, left, right) != 'bool':
            print(f"Line {-1}: Bad condition!")
    
    # Tutaj będzie macierz
    def visit_Vectors(self, node):
        vector_lengths = [len(v.vector.variables) for v in node.vectors]
        vector_no = len(node.vectors)
        if len(set(vector_lengths)) != 1:
            print("Line {}: Wrong Vector sizes, must be of same length in one matrix")
        return ArraySymbol(None, [vector_no, vector_lengths.pop()])
    
    def visit_Variables(self, node):
        for variable in node.variables:
            self.visit(variable)
            
    # Trzeba sprawdzić, czy macierz istnieje,
    # indeksy o którego się odwołujemy są int'ami
    # oraz czy nie wychodzimy poza rozmiar macierzy
    def visit_MatrixIdx(self, node):
        
        # sprawdzam, czy macierz, do której się odwołujemy wogóle istnieje
        matrix = self.table.get(node.var.id)
            
        if matrix:
            dimension = matrix.dimensions
            
            # jeden indeks dla wektora lub 2 dla macierzy
            if len(node.idxs.variables) < 1:
                print(f"Line {-1}: Number of indexes cant be lower than 1!")
            else:
                
                for i in range(len(node.idxs.variables)):
                
                    idx_type = self.visit(node.idxs.variables[0]).type
                
                    if idx_type != 'int':
                        print(f"Line {-1}: Index type must be an integer!")
                    else:
                        if i >= len(dimension):
                            print(f"Line {-1}: Reference to non existent matrix dimension!")
                        else:
                            if node.idxs.variables[0].int_number >= dimension[i]:
                                print(f"Line {-1}: Matrix index out of bounds")
        else:
            print(f"Line {-1}: Unknown reference to {node.var.id}")
        
        return VariableSymbol(None, None)
        
    # Trzeba sprawdzić, czy ID istnieje, jeśli tak to się do niego odwołać,
    # jeśli nie to dodać do tabeli
    def visit_Id(self, node):
        id = self.table.get(node.id)
        if id:
            return id
        else:
            new_id = VariableSymbol(node.id, None)
            self.table.put(node.id, new_id)
            return new_id
    
    def visit_IntNumber(self, node):
        return VariableSymbol(None, 'int')
    
    def visit_FloatNumber(self, node):
        return VariableSymbol(None, 'float')
    
    # Trzeba sprawdzić, czy wszystkie zmienne są tego samego typu
    def visit_Vector(self, node): 
        last_type = None
        
        for el in node.vector.variables:
            el_type = self.visit(el).type
            if last_type == None:   
                last_type = el_type
            else:
                if el_type != last_type:
                    print(f"Line {-1}: Mixed types in vector!")
            if el_type not in ['int', 'float']:
                    print(f"Line {-1}: Vector can only contain 'int' or 'float'")
        return ArraySymbol(None, [len(node.vector.variables)])
            
            
            
        
            
                