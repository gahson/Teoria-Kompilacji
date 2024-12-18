
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

assignment_operatiors = {

    '=' : lambda x, y : y,
    '+=' : lambda x, y : x + y,
    '-=' : lambda x, y : x - y,
    '*=' : lambda x, y : x * y,
    '/=' : lambda x, y : x / y,
    
}

condition_operators = {
    
    '==' : lambda x, y : x == y,
    '!=' : lambda x, y : x != y,
    '<' : lambda x, y : x < y,
    '<=' : lambda x, y : x <= y,
    '>' : lambda x, y : x > y,
    '>=' : lambda x, y : x >= y
    
}

['+', '+=', '-', '-=', '*', '*=', '/', '/=']

arithmetic_operators = {
    
    '+' : lambda x, y : x + y,
    '-' : lambda x, y : x - y,
    '*' : lambda x, y : x * y,
    '/' : lambda x, y : x / y
    
}

matrix_operators = {
    
    '.+' : lambda x, y : np.add(x, y),
    '.-' : lambda x, y : np.subtract(x, y),
    '.*' : lambda x, y : x @ y,
    './' : lambda x, y : np.linalg.inv(x) @ y
    
}

functions = {
    
    'eye' : lambda x : np.eye(x),
    'ones' : lambda x : np.ones(x),
    'zeros' : lambda x : np.zeros((x, x))
    
}

class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node):
        # Uwaga while wywołuję tą sekcję
        for instruction in node.instructions:
            instruction.accept(self)
        
    @when(AST.If)
    def visit(self, node):
        condition = node.condition.accept(self)
        
        if condition:
            try:
                self.memory_stack.push('If')
                node.instruction.accept(self)
            except BreakException as breakException:
                raise breakException
            except ReturnValueException as returnValueException:
                raise returnValueException
            finally:
                self.memory_stack.pop()
            
    @when(AST.IfElse)
    def visit(self, node):
        condition = node.condition.accept(self)
        
        if condition:
            try:
                self.memory_stack.push('If')
                node.instruction1.accept(self)
            except BreakException as breakException:
                raise breakException
            except ReturnValueException as returnValueException:
                raise returnValueException
            finally:
                self.memory_stack.pop()
        else:
            try:
                self.memory_stack.push('Else')
                node.instruction2.accept(self)
            except BreakException as breakException:
                raise breakException
            except ReturnValueException as returnValueException:
                raise returnValueException
            finally:
                self.memory_stack.pop()

    @when(AST.For)
    def visit(self, node):
        
        expression1 = node.expression1.accept(self)
        
        #self.memory_stack.insert(node.var.id, expression1)

        expression2 = node.expression2.accept(self)
        
        self.memory_stack.push('For')
        
        if isinstance(expression2, np.ndarray):
            range_ = expression2
        else:
            range_ = range(expression1, expression2)

        for item in range_:
            try:
                self.memory_stack.set(node.var.id, item)
                node.instruction.accept(self)
            except ContinueException:
                    continue
            except BreakException:
                    break
        self.memory_stack.pop()
                
    @when(AST.While)
    def visit(self, node):
        self.memory_stack.push('While')
 
        while node.condition.accept(self):
            try:                
                node.instruction.accept(self)
            except ContinueException:
                    continue
            except BreakException:
                    break
                
        self.memory_stack.pop()
                
    @when(AST.Break)
    def visit(self, node):
        raise BreakException()
    
    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.Return)
    def visit(self, node):
        to_return = np.array([node.expression_list.accept(self) for i in range(len(node.expression_list))])
        
        raise ReturnValueException(node.expression_list.accept(self))
    
    @when(AST.Expressions)
    def visit(self, node):
        return [expression.accept(self) for expression in node.expressions]

    @when(AST.Print)
    def visit(self, node):
        to_print = node.expression_list.accept(self)
        print(*to_print)
        
    @when(AST.AssignmentInstruction)
    def visit(self, node):
        # a = b
        # a[0] = b
        # a[0, 0] = b 
        
        expression = node.expression.accept(self)
        operator = node.assignment_operator
            
        if isinstance(node.lhs, AST.Id):
            
            prev_value = node.lhs.accept(self)
            
            if prev_value: # zmienna istniała wcześniej
                self.memory_stack.insert(node.lhs.id, assignment_operatiors[operator](prev_value, expression))
            else:
                # Tutaj powienien być tylko operator '='
                self.memory_stack.insert(node.lhs.id, expression)
        elif isinstance(node.lhs, AST.MatrixIdx):
            # Jeśli przypisujemy do indeksu to macierz musiała wcześniej istnieć
            
            matrix = node.lhs.var.accept(self)
            idxs = node.lhs.idxs.accept(self)
            
            
            for idx in idxs[:-1]:
                matrix = matrix[idx]

            matrix[idxs[-1]] = assignment_operatiors[operator](matrix[idxs[-1]], expression)
            
            
    @when(AST.OperatorExpression)
    def visit(self, node):
        
        expression1 = node.expression1.accept(self)
        operator = node.operator
        expression2 = node.expression2.accept(self)
        
        if isinstance(expression1, np.ndarray): # type checker zapewnia, że expression2 to też list
            return matrix_operators[operator](expression1, expression2)
        else:
            return arithmetic_operators[operator](expression1, expression2)
        
        
            
    @when(AST.UnaryMinus)
    def visit(self, node):
        expression = node.expression.accept(self)
        return -expression
            
    @when(AST.UnaryTranspose)
    def visit(self, node):
        matrix = node.expression.accept(self)
        return np.transpose(matrix)
            
    @when(AST.Function)
    def visit(self, node):
        return functions[node.function_name](node.expression.accept(self)[0])
            
    @when(AST.Condition)
    def visit(self, node):
        expression1 = node.expression1.accept(self)
        operator = node.operator
        expression2 = node.expression2.accept(self)
        return condition_operators[operator](expression1, expression2)
            
    @when(AST.Vectors)
    def visit(self, node):
        return np.array([vector.accept(self) for vector in node.vectors])
            
    @when(AST.Variables)
    def visit(self, node):
        return np.array([variable.accept(self) for variable in node.variables])
            
    @when(AST.MatrixIdx)
    def visit(self, node):
        matrix = node.var.accept(self)
        for idx in node.idxs.accept(self):
            matrix = matrix[idx]
        return matrix
            
    @when(AST.Id)
    def visit(self, node):
        return self.memory_stack.get(str(node.id))
            
    @when(AST.IntNumber)
    def visit(self, node):
        return int(node.int_number)
            
    @when(AST.FloatNumber)
    def visit(self, node):
        return float(node.float_number)
            
    @when(AST.String)
    def visit(self, node):
        return str(node.string)
            
    @when(AST.Vector)
    def visit(self, node):
        return node.vector.accept(self)
        
        
        
        
        
        
    
        