from __future__ import division
from processorDag import ProcessorDAG
from processor import Processor
from taskDag import TaskDAG
from slot import Slot
import sys

class Schedule(object):
    """docstring for Schedule"""
    def __init__(self, taskDag, processorDag):
        super(Schedule, self).__init__()
        self.taskDag = taskDag
        self.processorDag = processorDag
        self.isScheduled = False
        self.taskExecutionSlot = []
        self.processorExecutionSlots = []

        for i in range(0, len(processorDag.processors)):
            currentProcessor = processorDag.processors[i]
            self.processorExecutionSlots.append([Slot(None, currentProcessor, 0, sys.maxint)])

        for i in range(0, len(taskDag.tasks)):
            self.taskExecutionSlot.append(None)

    def add_new_slot(self, processor, task, startTime):
        currentProcessorSlots = self.processorExecutionSlots[processor.id]

        computationTime = task.computationRequired / processor.processingRate
        toBeTakenSlot = startTime + computationTime

        for i in range(0, len(currentProcessorSlots)):
            currentSlot = currentProcessorSlots[i]
            if currentSlot.start <= startTime and currentSlot.end >= toBeTakenSlot:
                start = startTime
                end = toBeTakenSlot

                newSlot = Slot(task, processor, start, end)
                currentProcessorSlots.append(newSlot)

                if start != currentSlot.start and end != currentSlot.end:
                    beforeSlot = Slot(None, processor, currentSlot.start, start)
                    afterSlot = Slot(None, processor, end, currentSlot.end)

                    currentProcessorSlots.append(beforeSlot)
                    currentProcessorSlots.append(afterSlot)
                elif start == currentSlot.start and end != currentSlot.end:
                    afterSlot = Slot(None, processor, end, currentSlot.end)
                    currentProcessorSlots.append(afterSlot)
                elif start != currentSlot.start and end == currentSlot.end:
                    beforeSlot = Slot(None, processor, currentSlot.start, start)
                    currentProcessorSlots.append(beforeSlot)

                del currentProcessorSlots[i]

                # sort all the slots in an increasing order based on start time
                currentProcessorSlots.sort(key = lambda el: el.start, reverse = True)
                # store execution slot of task for easy retrieving
                self.taskExecutionSlot[task.id] = newSlot
                print("Task " + str(task.id) + ", processor " + str(processor.id) + ", processingTime " + str(computationTime) + ": start " + str(start) + ", end " + str(end))

                break


    def canAddSlot(self, processor, task, startTime):
        isAllowedToAddSlot = False

        computationTime = task.computationRequired / processor.processingRate
        toBeTakenSlot = startTime + computationTime

        currentProcessorSlots = self.processorExecutionSlots[processorId]

        for i in range(0, len(currentProcessorSlots)):
            currentSlot = currentProcessorSlots[i]

            if currentSlot.start <= startTime and currentSlot.end >= toBeTakenSlot:
                isAllowedToAddSlot = True
                break

        return isAllowedToAddSlot

    def getBestSlotForTaskOnProcessor(self, processor, task):
        readyTime = -1

        for i in range(0, len(task.predecessors)):
            predTask = task.predecessors[i][0]
            predTaskConstraint = task.predecessors[i][1]
            predProcessor = self.taskExecutionSlot[predTask.id].processor

            communicationTime = ProcessorDAG.getCommunicationTime(predProcessor, processor, predTaskConstraint)

            predecessorSlotEnd = self.taskExecutionSlot[predTask.id].end
            currentReadyTime = predecessorSlotEnd + communicationTime

            if currentReadyTime > readyTime:
                readyTime = currentReadyTime

        processingTime = task.computationRequired / processor.processingRate

        currentProcessorSlots = self.processorExecutionSlots[processor.id]

        for i in range(0, len(currentProcessorSlots)):
            currentSlot = currentProcessorSlots[i]

            if currentSlot.task == None:
                actualStart = max(currentSlot.start, readyTime)
                actualEnd = actualStart + processingTime

                if actualEnd <= currentSlot.end:
                    return Slot(task, processor, actualStart, actualEnd)
            else:
                continue

        return Slot(task, processor, -1, -1)

    def get_ready_time_of_tasks(self,):
        pass

    def makespan(self):
        pass

    def cloud_cost(self):
        pass

    def print_schedule(self):
        pass

    def export(self, outputPath):
        pass
        