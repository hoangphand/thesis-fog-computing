import random

class Task(object):
    """docstring for Task"""

    # metrics: millions of instructions
    TASK_COMPUTATION_REQUIRED_LOWER_BOUND = 0.2
    TASK_COMPUTATION_REQUIRED_UPPER_BOUND = 2
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
    def __init__(self, id, layer_id, computation_required, memory_required, storage_required):
        super(Task, self).__init__()
        self.id = id
        self.layer_id = layer_id
        self.predecessors = []

        self.computation_required = computation_required
        self.memory_required = memory_required
        self.storage_required = storage_required

        self.successors = []

    def add_predecessor(self, task, memory_constraint):
        self.predecessors.append((task, memory_constraint))

    def add_successor(self, task, memory_constraint):
        self.successors.append((task, memory_constraint))

    def add_edge(self, task, memory_constraint):
        self.add_successor(task, memory_constraint)
        task.add_predecessor(self, memory_constraint)

    def add_edge_random_constraint(self, task):
        memory_constraint = round(random.uniform(self.__class__.TASK_MEMORY_CONSTRAINT_LOWER_BOUND, 
                                                self.__class__.TASK_MEMORY_CONSTRAINT_UPPER_BOUND), 2)
        self.add_successor(task, memory_constraint)
        task.add_predecessor(self, memory_constraint)

    def generate_random_values(self):
        memory_required = round(random.uniform(self.__class__.TASK_MEMORY_REQUIRED_LOWER_BOUND, 
                                                self.__class__.TASK_MEMORY_REQUIRED_UPPER_BOUND), 2)
        self.memory_required = memory_required

        # set computation required for task
        computation_required = round(random.uniform(self.__class__.TASK_COMPUTATION_REQUIRED_LOWER_BOUND, 
                                                    self.__class__.TASK_COMPUTATION_REQUIRED_UPPER_BOUND), 2)
        self.computation_required = computation_required

        # set storage required for task
        storage_required = round(random.uniform(self.__class__.TASK_STORAGE_REQUIRED_LOWER_BOUND, 
                                                self.__class__.TASK_STORAGE_REQUIRED_UPPER_BOUND), 2)
        self.storage_required = storage_required