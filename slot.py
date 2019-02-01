class Slot(object):
    """docstring for Slot"""
    def __init__(self, task, processor, start, end):
        super(Slot, self).__init__()
        self.task = task
        self.processor = processor
        self.start = start
        self.end = end

    def print_slot(self):
        if self.task != None:
            print("Task " + str(self.task.id) + ", processor " + str(self.processor.id) + ": " + str(self.start) + ", " + str(self.end))
        else:
            print("Task None, processor " + str(self.processor.id) + ": " + str(self.start) + ", " + str(self.end))
