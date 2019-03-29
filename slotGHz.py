class Slot(object):
    """docstring for Slot"""
    def __init__(self, task, processorCore, start, end):
        super(Slot, self).__init__()
        self.task = task
        self.processorCore = processorCore
        self.start = start
        self.end = end

    def printSlot(self):
        if self.task != None:
            print("Task " + str(self.task.id) + 
                ", processor " + str(self.processorCore.processor.id) + ": " + str(self.start) + ", " + str(self.end))
        else:
            print("Task None, processor " + str(self.processorCore.processor.id) + ": " + str(self.start) + ", " + str(self.end))
