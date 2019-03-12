from __future__ import division
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

    def addEdgeRandomConstraint(self, task, ccr, processorDag):
        avgBandwidth = processorDag.getAvgUploadBandwidth()
        avgProcessingRate = processorDag.getAvgProcessingRate()

        correspondingComm = round(ccr * (self.computationRequired * avgBandwidth) / avgProcessingRate, 2)
        lowerBound = 0.9 * correspondingComm
        upperBound = 1.1 * correspondingComm
        memoryConstraint = round(random.uniform(lowerBound, upperBound), 2)

        # memoryConstraint = round(ccr * (self.computationRequired * avgBandwidth) / avgProcessingRate, 2)

        # memoryConstraint = round(random.uniform(self.__class__.TASK_MEMORY_CONSTRAINT_LOWER_BOUND, 
        #                                         self.__class__.TASK_MEMORY_CONSTRAINT_UPPER_BOUND), 2)

        self.addSuccessor(task, memoryConstraint)
        task.addPredecessor(self, memoryConstraint)

    def removePredecessor(self, task):
        for i in range(0, len(self.predecessors)):
            if self.predecessors[i][0].id == task.id:
                del self.predecessors[i]
                return

    def removeSuccessor(self, task):
        for i in range(0, len(self.successors)):
            if self.successors[i][0].id == task.id:
                del self.successors[i]
                return

    def removeEdge(self, task):
        self.removePredecessor(task)
        self.removeSuccessor(task)
        task.removePredecessor(self)
        task.removeSuccessor(self)

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