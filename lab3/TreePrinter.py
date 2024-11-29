import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)
        
    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)
            
    @addToClass(AST.If)
    def printTree(self, indent=0):
        print("| " * indent + 'IF')
        self.condition.printTree(indent + 1)
        print("| " * indent + 'THEN')
        self.instruction.printTree(indent + 1)
        
    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print("| " * indent + 'IF')
        self.condition.printTree(indent + 1)
        print("| " * indent + 'THEN')
        self.instruction1.printTree(indent + 1)
        print("| " * indent + 'ELSE')
        self.instruction2.printTree(indent + 1)
        
    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("| " * indent + 'FOR')
        self.var.printTree(indent + 1)
        print("| " * (indent + 1) + 'RANGE')
        self.expression1.printTree(indent + 2)
        self.expression2.printTree(indent + 2)
        self.instruction.printTree(indent + 1)
        
    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)
        
    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("| " * indent + 'BREAK')
        
    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("| " * indent + 'CONTINUE')
        
    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("| " * indent + 'RETURN')
        self.expression_list.printTree(indent + 1)
        
    @addToClass(AST.Expressions)
    def printTree(self, indent=0):
        for expression in self.expressions:
            expression.printTree(indent)
        
    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("| " * indent + 'PRINT')
        self.expression_list.printTree(indent + 1)
        
    @addToClass(AST.AssignmentInstruction)
    def printTree(self, indent=0):
        print("| " * indent + self.assignment_operator)
        self.lhs.printTree(indent + 1)
        self.expression.printTree(indent + 1)
        
    @addToClass(AST.OperatorExpression)
    def printTree(self, indent=0):
        print("| " * indent + self.operator)
        self.expression1.printTree(indent + 1)
        self.expression2.printTree(indent + 1)
       
    @addToClass(AST.UnaryMinus) # Do poprawy
    def printTree(self, indent=0):
        print("| " * indent + "UNARY MINUS")
        self.expression.printTree(indent + 1)
        
    @addToClass(AST.UnaryTranspose)
    def printTree(self, indent=0):
        print("| " * indent + "TRANSPOSE")
        self.expression.printTree(indent + 1)
        
    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print("| " * indent + self.function_name)
        self.expression.printTree(indent + 1)
        
    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print("| " * indent + self.operator)
        self.expression1.printTree(indent + 1)
        self.expression2.printTree(indent + 1)
        
    @addToClass(AST.Vectors)
    def printTree(self, indent=0):
        print("| " * indent + "VECTOR")
        for vector in self.vectors:
            vector.printTree(indent + 1)
            
    @addToClass(AST.Variables)
    def printTree(self, indent=0):
        for variable in self.variables:
            variable.printTree(indent)
            
    @addToClass(AST.MatrixIdx)
    def printTree(self, indent=0):
        print("| " * indent + "REF")
        self.var.printTree(indent + 1)
        print("| " * (indent + 1) + str(self.idx1))
        print("| " * (indent + 1) + str(self.idx2))
        
    @addToClass(AST.VectorIdx)
    def printTree(self, indent=0):
        print("| " * indent + "VECTOR INDEX")
        self.var.printTree(indent + 1)
        print("| " * indent + str(self.idx))
    
    @addToClass(AST.Id)
    def printTree(self, indent=0):
        print("| " * indent + self.id)
        
    @addToClass(AST.IntNumber)
    def printTree(self, indent=0):
        print("| " * indent + str(self.int_number))

    @addToClass(AST.FloatNumber)
    def printTree(self, indent=0):
        print("| " * indent + str(self.float_number))

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("| " * indent + "VECTOR")
        self.vector.printTree(indent + 1)
    
    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
    