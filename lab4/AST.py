class Node(object):
    pass

class Instructions(Node):
    def __init__(self, instructions):
        self.instructions = instructions
        
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
    def __init__(self, lineno):
        self.lineno = lineno
    
class Continue(Node):
    def __init__(self, lineno):
        self.lineno = lineno

class Return(Node):
    def __init__(self, expression_list):
        self.expression_list = expression_list
        
class Expressions(Node):
    def __init__(self, expressions):
        self.expressions = expressions
        
class Print(Node):
    def __init__(self, expression_list):
        self.expression_list = expression_list
        
class AssignmentInstruction(Node):
    def __init__(self, lhs, assignment_operator, expression, lineno):
        self.lhs = lhs
        self.assignment_operator = assignment_operator
        self.expression = expression
        self.lineno = lineno

class OperatorExpression(Node):
    def __init__(self, expression1, operator, expression2, lineno):
        self.expression1 = expression1
        self.operator = operator
        self.expression2 = expression2
        self.lineno = lineno
        
class UnaryMinus(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno

class UnaryTranspose(Node):
    def __init__(self, expression, lineno):
        self.expression = expression
        self.lineno = lineno
        
class Function(Node):
    def __init__(self, function_name, expression, lineno):
        self.function_name = function_name
        self.expression = expression
        self.lineno = lineno
        
class Condition(Node):
    def __init__(self, expression1, operator, expression2, lineno):
        self.expression1 = expression1
        self.operator = operator
        self.expression2 = expression2
        self.lineno = lineno

class Vectors(Node):
    def __init__(self, vectors, lineno):
        self.vectors = vectors
        self.lineno = lineno

class Variables(Node):
    def __init__(self, variables):
        self.variables = variables

class MatrixIdx(Node):
    def __init__(self, var, idxs, lineno):
        self.var = var
        self.idxs = idxs
        self.lineno = lineno

class Id(Node):
    def __init__(self, id):
        self.id = id

class IntNumber(Node):
    def __init__(self, int_number):
        self.int_number = int_number

class FloatNumber(Node):
    def __init__(self, float_number):
        self.float_number = float_number
        
class String(Node):
    def __init__(self, string):
        self.string = string

class Vector(Node):
    def __init__(self, vector, lineno):
        self.vector = vector
        self.lineno = lineno

class Error(Node):
    def __init__(self):
        pass
      
