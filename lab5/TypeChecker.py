#!/usr/bin/python
import AST
from collections import defaultdict
from SymbolTable import *

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))

arithmetic_operators = ['+', '+=', '-', '-=', '*', '*=', '/', '/=']
matrix_operators = ['.+', '.-', '.*', './']
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
    # Zawsze chcemy mieć możliwość nadpisania zmiennej (jak w pythonie)
    if operator == '=' and right.symbol_type in ['matrix', 'vector', 'int', 'float', 'string']:
        return right.symbol_type
    
    if operator in ttype:
            if left.symbol_type in ttype[operator]:
                if right.symbol_type in ttype[operator][left.symbol_type]:
                    return ttype[operator][left.symbol_type][right.symbol_type]
    return None
    
def get_dimensions(operator, left, right):

        if operator == '=':
            return right.matrix_dimensions
        elif operator in ['.+', '.-']:
            if left.matrix_dimensions == right.matrix_dimensions:
                return left.matrix_dimensions
        elif operator in ['.*', './']:
            if len(left.matrix_dimensions) == 2 and len(right.matrix_dimensions) == 2:
                if left.matrix_dimensions[1] == right.matrix_dimensions[0]:
                    return [left.matrix_dimensions[0], right.matrix_dimensions[1]]
            else: 
                # Dla większego rozmiaru przyjmujemy dla uproszczenia
                # że wymiary muszą być równe
                if left.matrix_dimensions == right.matrix_dimensions:
                    return left.matrix_dimensions
        return None
    
class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
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
        self.table = self.table.pushScope("If")
        
        self.visit(node.condition)
        self.visit(node.instruction)
        
        self.table = self.table.popScope()
        
    def visit_IfElse(self, node):
        self.table = self.table.pushScope("If")
        
        self.visit(node.condition)
        self.visit(node.instruction1)
        
        self.table = self.table.popScope()
        self.table = self.table.pushScope("Else")
        
        self.visit(node.instruction2)
        
        self.table = self.table.popScope()
        
    def visit_For(self, node):
        self.table = self.table.pushScope("For")
        
        self.visit(node.var)
        self.visit(node.expression1)
        self.visit(node.expression2)
        self.nested_loops += 1
        self.visit(node.instruction)
        self.nested_loops -= 1
        
        self.table = self.table.popScope()
        
    def visit_While(self, node):
        self.table = self.table.pushScope("While")
        
        self.visit(node.condition)
        self.nested_loops += 1
        self.visit(node.instruction)
        self.nested_loops -= 1
        
        self.table = self.table.popScope()
        
    def visit_Break(self, node):
        if self.nested_loops == 0:
            print(f"Line {node.lineno}: 'Break' used outside of a loop!")
            
    def visit_Continue(self, node):
        if self.nested_loops == 0:
            print(f"Line {node.lineno}: 'Continue' used outside of a loop!")
    
    # Return może zwrócić cokolwiek
    def visit_Return(self, node):
        if node.expression_list:
            self.visit(node.expression_list)
            
    def visit_Expressions(self, node):
        if node.expressions:
            self.visit(node.expressions)
            
    # Zakładamy, że print może wypisać wszystko
    def visit_Print(self, node):
        if node.expression_list:
            self.visit(node.expression_list)
    
    
    def visit_AssignmentInstruction(self, node):
        left = self.visit(node.lhs)
        operator = node.assignment_operator
        right = self.visit(node.expression) 
        # Sprawdzam, czy można wykonać operację na tych dwóch typach
        
        assignment_type = get_type(operator, left, right)

        #if self.table.get(node.lhs.id).symbol_type is None and operator != '=':
        #    print(f"Line {node.lineno}: Can't assign value to non existent symbol!")
                
        #else:        
        if assignment_type is not None:
            if assignment_type != 'matrix':
                # Jeśli rezultatem przypisania nie jest macierz to aktualizuję
                # zawartość symbolu to lewej
                self.table.put(left.symbol_name, VariableSymbol(left.symbol_name, right.symbol_type))
            else: 
                # Jeśli jest macierzą to również aktualizuję zawartość symbolu po lewej
                # tylko tym razem, typ symbolu to macierz
                if get_dimensions(operator, left, right) is not None:
                    self.table.put(left.symbol_name, MatrixSymbol(left.symbol_name, right.matrix_dimensions))
                else:
                    print(f"Line {node.lineno}: Wrong assignment operation!")
        else:
            if isinstance(left, VariableSymbol) and left.symbol_type is None:
                # Nic nie było wcześniej przypisane do lewego symbolu
                if isinstance(right, MatrixSymbol):
                    new_l = MatrixSymbol(left.symbol_name, right.matrix_dimensions)
                    self.table.put(left.symbol_name, new_l)
                elif isinstance(right, VariableSymbol):
                    new_l = VariableSymbol(left.symbol_name, right.symbol_type)
                    self.table.put(left.symbol_name, new_l)        
            else:
                # Left ma inny typ niż None, czyli próbujemy wykonać operację przypisania
                # na niekompatybilnych typach
                print(f"Line {node.lineno}: Can't perform '{operator}' on an instances of '{right.symbol_type}' and '{left.symbol_type}'")
        
    def visit_OperatorExpression(self, node):
        left = self.visit(node.expression1)
        operator = node.operator
        right = self.visit(node.expression2)
        operation_type = get_type(operator, left, right)

        if left.symbol_type is None:
            print(f"Line {node.lineno}: Can't perform '{operator}' on non existent variable!")
            return VariableSymbol(None, None)
        else:
            if operation_type == 'matrix': # Jesli tak, to napewno left i right to macierze
                dims = get_dimensions(operator, left, right) # Czy dla macierzy o podanych wymiarach operacja ma sens
                if dims is None:
                    print(f"Line {node.lineno}: Can perform {operator} on matrices with size {left.matrix_dimensions} and {right.matrix_dimensions}")
                    return MatrixSymbol(None, None)
                else:
                    return MatrixSymbol(None, dims)
            elif operation_type is None: # Wyrażenie nie ma sensu dla danych typów
                print(f"Line {node.lineno}: Can't perform '{operator}' on an instances of '{left.symbol_type}' and '{right.symbol_type}'")
            return VariableSymbol(None, operation_type)
        
    # Trzeba sprawdzić, czy minus jest ustawiony przez wartością liczbową
    def visit_UnaryMinus(self, node):
        symbol = self.visit(node.expression)
        if symbol.symbol_type not in ['int', 'float']:
            print(f"Line {node.lineno}: Unary minus operator can only be applied to a number!")
        return symbol
    
    # Trzeba sprawdzić, czy transpozycja jest wywołana na macierzy
    def visit_UnaryTranspose(self, node):
        symbol = self.visit(node.expression)
        if not isinstance(symbol, MatrixSymbol):
            print(f"Line {node.lineno}: Transposition only works on matrices!")
        return symbol
        
    # Trzeba sprawdzić, czy argument funkcji jest int'em
    def visit_Function(self, node):
        
        # Ma być dokładnie jeden argument
        if len(node.expression.expressions) != 1:
            print(f"Line {node.lineno}: Wrong number of arguments in '{node.function_name}' function!")
        else:
            #Skoro jest jeden argument to sprawdzam, czy jest int'em
            if self.visit(node.expression.expressions[0]).symbol_type != 'int':
                 print(f"Line {node.lineno}: Function argument must be an integer!")
            else:
                return MatrixSymbol(None, [node.expression.expressions[0].int_number, node.expression.expressions[0].int_number])
        return MatrixSymbol(None, [])
    # Trzeba sprawdzić, czy condition może zwrócić bool'a
    def visit_Condition(self, node):
        left = self.visit(node.expression1)
        operator = node.operator
        right = self.visit(node.expression2)

        if get_type(operator, left, right) != 'bool':
            print(f"Line {node.lineno}: Bad condition!")
    
    # Tutaj będzie macierz
    def visit_Vectors(self, node):
        vector_lengths = [len(v.vector.variables) for v in node.vectors]
        vector_no = len(node.vectors)
        if len(set(vector_lengths)) != 1:
            print(f"Line {node.lineno}: All vectors in a matrix have same size!")
        return MatrixSymbol(None, [vector_no, vector_lengths.pop()])
    
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
            dimension = matrix.matrix_dimensions
            
            # jeden indeks dla wektora lub 2 dla macierzy
            if len(node.idxs.variables) < 1:
                print(f"Line {node.lineno}: Number of indexes cant be lower than 1!")
            else:
                
                for i in range(len(node.idxs.variables)):
                
                    idx_type = self.visit(node.idxs.variables[0]).symbol_type
                
                    if idx_type != 'int':
                        print(f"Line {node.lineno}: Index type must be an integer!")
                    else:
                        if i >= len(dimension):
                            
                            print(f"Line {node.lineno}: Reference to non existent '{i + 1}' matrix dimension!")
                        else:
                            if node.idxs.variables[0].int_number >= dimension[i]:
                                print(f"Line {node.lineno}: Matrix index out of bounds")
        else:
            print(f"Line {node.lineno}: Unknown reference to {node.var.id}")
        
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
    
    def visit_String(self, node):
        return VariableSymbol(None, 'string')
    
    # Trzeba sprawdzić, czy wszystkie zmienne są tego samego typu
    def visit_Vector(self, node): 
        last_type = None
        
        for el in node.vector.variables:
            el_type = self.visit(el).symbol_type
            if last_type == None:   
                last_type = el_type
            else:
                if el_type != last_type:
                    print(f"Line {node.lineno}: Mixed types in vector!")
            
            # Zakładamy, że wektor może zawierać tylko liczby
            if el_type not in ['int', 'float']:
                    print(f"Line {node.lineno}: Vectors can only contain 'int' or 'float'")
            
        # jakby zwracamy symbol utworzony z [[...], [...], [...]] więc nie ma nazwy
        return MatrixSymbol(None, [len(node.vector.variables)])
            
            
            
        
            
                