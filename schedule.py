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
        # self.isScheduled = False
        # store execution slot of each task for easy retrieving
        self.taskExecutionSlot = []
        # store all execution slots of each processor
        self.processorExecutionSlots = []

        for i in range(0, len(processorDag.processors)):
            currentProcessor = processorDag.processors[i]
            self.processorExecutionSlots.append([Slot(None, currentProcessor, 0, sys.maxint)])

        for i in range(0, len(taskDag.tasks)):
            self.taskExecutionSlot.append(None)

        # actual finish time of schedule
        self.aft = 0

    def addNewSlot(self, processor, task, startTime):
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
                # print("Task " + str(task.id) + 
                #     ", processor " + str(processor.id) + 
                #     ", processingTime " + str(computationTime) + ": start " + str(start) + ", end " + str(end))

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

    # this function calculates the earliest slot that a processor 
    # will be able to execute a specified task
    def getBestSlotForTaskOnProcessor(self, processor, task):
        readyTime = -1

        # loop through all predecessors of the current task
        for i in range(0, len(task.predecessors)):
            # get predecessor task in the tuple of (task, dependency)
            predTask = task.predecessors[i][0]
            # get dependency of current predecessor
            predTaskConstraint = task.predecessors[i][1]
            # get processor which processes the current predecessor task
            predProcessor = self.taskExecutionSlot[predTask.id].processor

            # calculate communication time to transmit data dependency from 
            # processor which is assigned to process the predecessor task to 
            # the processor which is being considered to use to process the current task
            communicationTime = self.processorDag.getCommunicationTime(predProcessor, 
                processor, predTaskConstraint)

            predecessorSlotEnd = self.taskExecutionSlot[predTask.id].end
            currentReadyTime = predecessorSlotEnd + communicationTime

            if currentReadyTime > readyTime:
                readyTime = currentReadyTime

        processingTime = task.computationRequired / processor.processingRate

        currentProcessorSlots = self.processorExecutionSlots[processor.id]

        # find the earliest slot
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

    def getTotalComputationCost(self):
        totalComputationCost = 0

        for i in range(0, len(self.taskExecutionSlot)):
          totalComputationCost += self.getComputationCostOfTask(i)

        return totalComputationCost

    def getTotalCommunicationCost(self):
        totalCommunicationCost = 0

        for indexLayer in range(0, len(self.taskDag.layers)):
            for indexTask in range(0, len(self.taskDag.layers[indexLayer])):
                currentTask = self.taskDag.layers[indexLayer][indexTask]

                for indexPred in range(0, len(currentTask.predecessors)):
                    currentPred = currentTask.predecessors[indexPred]

                    tmp = self.processorDag.getCommunicationTime(
                            self.taskExecutionSlot[currentPred[0].id].processor, 
                            self.taskExecutionSlot[currentTask.id].processor, 
                            currentPred[1])

                    totalCommunicationCost += tmp

        return totalCommunicationCost

    def cloneTrialSchedule(self, taskDag):
        newSchedule = Schedule(taskDag, self.processorDag)
        newSchedule.processorExecutionSlots = self.processorExecutionSlots[:]

        return newSchedule

    def getComputationCostOfTask(self, taskId):
        currentTask = self.taskExecutionSlot[taskId].task
        currentProcessor = self.taskExecutionSlot[taskId].processor

        computationCost = currentTask.computationRequired / currentProcessor.processingRate

        return computationCost

    def getMaxPredCommunicationCost(self, taskId):
        maxCommunicationCost = -1

        currentTask = self.taskDag.tasks[taskId]

        for indexPred in range(0, len(currentTask.predecessors)):
            currentPred = currentTask.predecessors[indexPred]

            tmp = self.processorDag.getCommunicationTime(
                    self.taskExecutionSlot[currentPred[0].id].processor, 
                    self.taskExecutionSlot[currentTask.id].processor, 
                    currentPred[1])

            if maxCommunicationCost < tmp:
                maxCommunicationCost = tmp

        return maxCommunicationCost

    def getNoOfTasksAllocatedToCloudNodes(self):
        noOfAllocatedCloudNotes = 0

        for i in range(1, len(self.taskDag.tasks) - 1):
            if not self.taskExecutionSlot[i].processor.isFog:
                noOfAllocatedCloudNotes += 1

        return noOfAllocatedCloudNotes

    def getNoOfTasksAllocatedToFogNodes(self):
        return len(self.taskDag.tasks) - self.getNoOfTasksAllocatedToCloudNodes() - 2

    def getReadyTimeOfTasks(self,):
        pass

    def makespan(self):
        pass

    def cloudCost(self):
        pass

    def printSchedule(self):
        pass

    def export(self, outputPath):
        pass
        