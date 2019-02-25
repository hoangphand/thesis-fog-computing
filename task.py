import random

class Task(object):
    """docstring for Task"""

    # metrics: millions of instructions
    TASK_COMPUTATION_REQUIRED_LOWER_BOUND = 2
    TASK_COMPUTATION_REQUIRED_UPPER_BOUND = 60
    # metrics: MB (megabyte)
    TASK_MEMORY_REQUIRED_LOWER_BOUND = 0.5
    TASK_MEMORY_REQUIRED_UPPER_BOUND = 20
    # metrics: MB (megabyte)
    TASK_STORAGE_REQUIRED_LOWER_BOUND = 0.5
    TASK_STORAGE_REQUIRED_UPPER_BOUND = 20
    # metrics: Mb (megabit)
    TASK_MEMORY_CONSTRAINT_LOWER_BOUND = 0.2
    TASK_MEMORY_CONSTRAINT_UPPER_BOUND = 5

    # Methods
    def __init__(self, id, layerId, computationRequired, memoryRequired, storageRequired):
        super(Task, self).__init__()
        self.id = id
        self.layerId = layerId
        self.predecessors = []

        self.computationRequired = computationRequired
        self.memoryRequired = memoryRequired
        self.storageRequired = storageRequired

        self.successors = []

    def addPredecessor(self, task, memoryConstraint):
        self.predecessors.append((task, memoryConstraint))

    def addSuccessor(self, task, memoryConstraint):
        self.successors.append((task, memoryConstraint))

    def addEdge(self, task, memoryConstraint):
        self.addSuccessor(task, memoryConstraint)
        task.addPredecessor(self, memoryConstraint)

    def addEdgeRandomConstraint(self, task):
        memoryConstraint = round(random.uniform(self.__class__.TASK_MEMORY_CONSTRAINT_LOWER_BOUND, 
                                                self.__class__.TASK_MEMORY_CONSTRAINT_UPPER_BOUND), 2)
        self.addSuccessor(task, memoryConstraint)
        task.addPredecessor(self, memoryConstraint)

    def removeEdge(self, task, memoryConstraint):
        self.addSuccessor(task, memoryConstraint)
        task.addPredecessor(self, memoryConstraint)

    def generateRandomValues(self):
        memoryRequired = round(random.uniform(self.__class__.TASK_MEMORY_REQUIRED_LOWER_BOUND, 
                                                self.__class__.TASK_MEMORY_REQUIRED_UPPER_BOUND), 2)
        self.memoryRequired = memoryRequired

        # set computation required for task
        computationRequired = round(random.uniform(self.__class__.TASK_COMPUTATION_REQUIRED_LOWER_BOUND, 
                                                    self.__class__.TASK_COMPUTATION_REQUIRED_UPPER_BOUND), 2)
        self.computationRequired = computationRequired

        # set storage required for task
        storageRequired = round(random.uniform(self.__class__.TASK_STORAGE_REQUIRED_LOWER_BOUND, 
                                                self.__class__.TASK_STORAGE_REQUIRED_UPPER_BOUND), 2)
        self.storageRequired = storageRequired