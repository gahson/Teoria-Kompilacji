
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Instructions)
    def visit(self, node):
        # Trzeba stworzyć ogólny scop'e
        self.memory_stack = MemoryStack()
        self.memory_stack.push('Program')
        
        for instruction in node.instructions:
            instruction.accept(self)
        
        self.memory_stack.pop()
        
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
        var = node.var.accept(self)
        expression1 = node.expression1.accept(self)
        expresison2 = node.expression2.accept(self)
        
        for item in expresison2:
            try:
                self.memory_stack.push('For')
                self.memory_stack.set(expression1, item)
                node.insruction.accept(self)
            except ContinueException:
                    continue
            except BreakException:
                    break
            finally:
                self.memory_stack.pop()
                
    @when(AST.While)
    def visit(self, node):
 
        while node.condition.accept(self):
            try:
                self.memory_stack.push('While')
                node.instruction.accept(self)
            except ContinueException:
                    continue
            except BreakException:
                    break
            finally:
                self.memory_stack.pop()
                
    @when(AST.Break)
    def visit(self, node):
        raise BreakException()
    
    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()
    
    @when(AST.Return)
    def visit(self, node):
        to_return = [node.expression_list.accept(self) for i in range(len(node.expression_list))]
        
        raise ReturnValueException(node.expression_list.accept(self))
    
    @when(AST.Expressions)
    def visit(self, node):
        node.expressions.accept(self)
        
    @when(AST.Print)
    def visit(self, node):
        to_print = [node.expression_list.accept(self) for i in range(len(node.expression_list))]
        print(*to_print)
        
    
        