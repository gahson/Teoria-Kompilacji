class Memory:

    def __init__(self, name): # memory name
        self.scope = name
        self.mem = {}

    def has_key(self, name):  # variable name
        if name in self.mem:
            return True
        return False

    def get(self, name):         # gets from memory current value of variable <name>
        return self.mem[name]
        
    def put(self, name, value):  # puts into memory current value of variable <name>
        self.mem.update((name, value))

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        
        if memory is None:
            self.stack.append(Memory('Program'))
        else:
            self.stack.append(Memory(memory))
        
    def get(self, name): # gets from memory stack current value of variable <name>
        # Iterujemy od tyłu żeby wziąć najpierw wartość z najbliższego scope'a
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i].has_key(name):
                return self.stack[i].get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)
        
    def set(self, name, value): # sets variable <name> to value <value>
        self.insert(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(Memory(memory))

    def pop(self): # pops the top memory from the stack
        # Trzeba zaaktualizować nadpisane wartości w ostatnim stacku w poprzednich stackach
        # przed wykonaniem pop'a
        
        for name, value in self.stack[-1].items():
            
            for i in range(len(self.stack) - 2, -1, -1):
                if self.stack[i].has_key(name):
                    self.stack[i].put(name, value)
                    break # Chcemy zaaktualizować wartość tylko w najbliższym scope'ie
        
        self.stack.pop()