class Node(object):
    pass

class InstructionsOne(Node):
    def __init__(self, instruction):
        self.instruction = instruction
        

class InstructionsList(Node):
    def __init__(self, instructions, instruction):
        self.instructions = instruction.append(instruction)


class If(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction

class IfElse(Node):
    def __init__(self, condition ,instruction1, instruction2):
        self.condition = condition
        self.instruction1 = instruction1
        self.instruction2 = instruction2
        
class For(Node):
    def __init__(self, var, expression1, expression2, instruction):
        self.var = var
        self.expression1 = expression1
        self.expression2 = expression2
        self.instruction = instruction

class While(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        
class Break(Node):
    def __init__(self):
        pass
    
class Continue(Node):
    def __init__(self):
        pass

class Return(Node):
    def __init__(self, expression_list):
        self.expression_list = expression_list
        
class ExpressionList(Node):
    def __init__(self, expression_list, expression):
        self.expression_list = expression_list.append(expression)
        
class ExpressionOne(Node):
    def __init__(self, expression):
        self.expression = expression
        
class Print(Node):
    def __init__(self, expression_list):
        self.expression_list = expression_list
        
class AssignmentInstruction(Node):
    def __init__(self, lhs, assignment_operator, expression):
        self.lhs = lhs
        self.assignment_operator = assignment_operator
        self.expression = expression

class BinaryExpression(Node):
    def __init__(self, expression1, operator, expression2):
        self.expression1 = expression1
        self.operator = operator
        self.expression2 = expression2

class MatrixExpression(Node):
    def __init__(self, expression1, operator, expression2):
        self.expression1 = expression1
        self.operator = operator
        self.expression2 = expression2

class UnaryMinus(Node):
    def __init__(self, expression):
        self.expression = expression

class UnaryTranspose(Node):
    def __init__(self, expression):
        self.expression = expression
        
class Function(Node):
    def __init__(self, expression):
        self.expression = expression
        
class Condition(Node):
    def __init__(self, expression1, operator, expression2):
        self.expression1 = expression1
        self.operator = operator
        self.expression2 = expression2

class VectorsList(Node):
    def __init__(self, vectors, vector):
        self.vectors = vectors.append(vector)
        
class VectorsOne(Node):
    def __init__(self, vector):
        self.vector = vector

class VariablesList(Node):
    def __init__(self, variables, variable):
        self.variables = variables.append(variable)
        
class VariablesOne(Node):
    def __init__(self, variable):
        self.variable = variable

class MatrixIdx(Node):
    def __init__(self, var, idx1, idx2):
        self.var = var
        self.idx1 = idx1
        self.idx2 = idx2

class VectorIdx(Node):
    def __init__(self, var, idx):
        self.var = var
        self.idx = idx

class Error(Node):
    def __init__(self):
        pass
      
