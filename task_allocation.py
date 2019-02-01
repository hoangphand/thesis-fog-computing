class TaskAllocation(object):
    """docstring for TaskAllocation"""
    def __init__(self, task, processor, est, eft, ast, aft):
        super(TaskAllocation, self).__init__()
        self.task = task
        self.processor = processor
        self.est = est
        self.eft = eft
        self.ast = ast
        self.aft = aft
        