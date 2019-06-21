from __future__ import division
from processorDag import ProcessorDAG
from processor import Processor
from processorCore import ProcessorCore
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
        self.processorCoreExecutionSlots = []

        schedulePositionId = 0
        for i in range(0, len(processorDag.processors)):
            currentProcessor = processorDag.processors[i]

            for j in range(0, currentProcessor.noOfCores):
                self.processorCoreExecutionSlots.append([
                    Slot(None, ProcessorCore(currentProcessor, j, schedulePositionId), 0, sys.maxint)
                ])
                schedulePositionId += 1

        for i in range(0, len(taskDag.tasks)):
            self.taskExecutionSlot.append(None)

        # actual finish time of schedule
        self.aft = 0

    # add a new slot for a task on a processor at time startTime
    def addNewSlot(self, processorCore, task, startTime):
        currentProcessorCoreSlots = self.processorCoreExecutionSlots[processorCore.schedulePositionId]

        computationTime = task.computationRequired / processorCore.processor.processingRate
        endTime = startTime + computationTime

        for i in range(0, len(currentProcessorCoreSlots)):
            currentSlot = currentProcessorCoreSlots[i]
            # find the first slot on the processor that fits the startTime and endTime
            if currentSlot.task == None and currentSlot.start <= startTime and currentSlot.end >= endTime:
                newSlot = Slot(task, processorCore, startTime, endTime)
                currentProcessorCoreSlots.append(newSlot)

                if startTime != currentSlot.start and endTime != currentSlot.end:
                    slotBefore = Slot(None, processorCore, currentSlot.start, startTime)
                    slotAfter = Slot(None, processorCore, endTime, currentSlot.end)

                    currentProcessorCoreSlots.append(slotBefore)
                    currentProcessorCoreSlots.append(slotAfter)
                elif startTime == currentSlot.start and endTime != currentSlot.end:
                    slotAfter = Slot(None, processorCore, endTime, currentSlot.end)

                    currentProcessorCoreSlots.append(slotAfter)
                elif startTime != currentSlot.start and endTime == currentSlot.end:
                    slotBefore = Slot(None, processorCore, currentSlot.start, startTime)

                    currentProcessorCoreSlots.append(slotBefore)

                del currentProcessorCoreSlots[i]

                # sort all the slots in an increasing order based on start time
                currentProcessorCoreSlots.sort(key = lambda el: el.start, reverse = False)
                # store execution slot of task for easy retrieving
                self.taskExecutionSlot[task.id] = newSlot
                # print("Task " + str(task.id) + 
                #     ", processor " + str(processor.id) + 
                #     ", processingTime " + str(computationTime) + ": start " + str(start) + ", end " + str(end))

                break

    # this function calculates the earliest slot that a processor 
    # will be able to execute a specified task
    def getFirstFitSlotForTaskOnProcessorCore(self, processorCore, task):
        # the ready time of the task at which
        # all required input data has arrived at the current processor
        readyTime = -1

        # loop through all predecessors of the current task
        # to calculate readyTime
        for i in range(0, len(task.predecessors)):
            # get predecessor task in the tuple of (task, dependency)
            predTask = task.predecessors[i][0]
            # get dependency of current predecessor
            predTaskConstraint = task.predecessors[i][1]
            # get processor which processes the current predecessor task
            predProcessorCore = self.taskExecutionSlot[predTask.id].processorCore

            # calculate communication time to transmit data dependency from 
            # processor which is assigned to process the predecessor task to 
            # the processor which is being considered to use to process the current task
            communicationTime = self.processorDag.getCommunicationTimeBetweenCores(predProcessorCore, 
                processorCore, predTaskConstraint)

            predecessorSlotEnd = self.taskExecutionSlot[predTask.id].end
            currentReadyTime = predecessorSlotEnd + communicationTime

            if currentReadyTime > readyTime:
                readyTime = currentReadyTime

        processingTime = task.computationRequired / processorCore.processor.processingRate

        currentProcessorCoreSlots = self.processorCoreExecutionSlots[processorCore.schedulePositionId]

        # find the earliest slot
        for i in range(0, len(currentProcessorCoreSlots)):
            currentSlot = currentProcessorCoreSlots[i]

            if currentSlot.task == None:
                actualStart = max(currentSlot.start, readyTime)
                actualEnd = actualStart + processingTime

                if actualEnd <= currentSlot.end:
                    # return the first fit slot for the task on the current processor
                    return Slot(task, processorCore, actualStart, actualEnd)
            else:
                continue

        print("nothing")
        return Slot(task, processorCore, -1, -1)

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

                    tmp = self.processorDag.getCommunicationTimeBetweenCores(
                            self.taskExecutionSlot[currentPred[0].id].processorCore, 
                            self.taskExecutionSlot[currentTask.id].processorCore, 
                            currentPred[1])

                    totalCommunicationCost += tmp

        return totalCommunicationCost

    def cloneTrialSchedule(self, taskDag):
        newSchedule = Schedule(taskDag, self.processorDag)
        newSchedule.processorCoreExecutionSlots = self.processorCoreExecutionSlots[:]

        return newSchedule

    def getComputationCostOfTask(self, taskId):
        currentTask = self.taskExecutionSlot[taskId].task
        currentProcessor = self.taskExecutionSlot[taskId].processorCore.processor

        computationCost = currentTask.computationRequired / currentProcessor.processingRate

        return computationCost

    def getMaxPredCommunicationCost(self, taskId):
        maxCommunicationCost = -1

        currentTask = self.taskDag.tasks[taskId]

        for indexPred in range(0, len(currentTask.predecessors)):
            currentPred = currentTask.predecessors[indexPred]

            tmp = self.processorDag.getCommunicationTimeBetweenCores(
                    self.taskExecutionSlot[currentPred[0].id].processorCore, 
                    self.taskExecutionSlot[currentTask.id].processorCore, 
                    currentPred[1])

            if maxCommunicationCost < tmp:
                maxCommunicationCost = tmp

        return maxCommunicationCost

    def getNoOfTasksAllocatedToCloudNodes(self):
        noOfAllocatedCloudNotes = 0

        for i in range(1, len(self.taskDag.tasks) - 1):
            if not self.taskExecutionSlot[i].processorCore.processor.isFog:
                noOfAllocatedCloudNotes += 1

        return noOfAllocatedCloudNotes

    def getNoOfTasksAllocatedToFogNodes(self):
        return len(self.taskDag.tasks) - self.getNoOfTasksAllocatedToCloudNodes() - 2

    def getFirstProcessorCoreFreeAt(self, time):
        selectedProcessorCore = None
        earliestStartTime = sys.maxint

        for processorCoreId in range(0, len(self.processorCoreExecutionSlots)):
            for slotId in range(0, len(self.processorCoreExecutionSlots[processorCoreId])):
                currentSlot = self.processorCoreExecutionSlots[processorCoreId][slotId]

                if currentSlot != None and currentSlot.start <= time:
                    if currentSlot.start < earliestStartTime:
                        earliestStartTime = currentSlot.start
                        selectedProcessorCore = self.processorCoreExecutionSlots[processorCoreId].processorCore
                    else:
                        continue
                else:
                    continue
        
        return selectedProcessor

    def countSlotsInNetwork(self):
        count = 0

        for i in range(0, len(self.processorDag.processors)):
            count += len(self.processorCoreExecutionSlots[i])

        return count

    def showProcessorSlots(self):
        for i in range(0, len(self.processorCoreExecutionSlots)):
            currentProcessorSlots = self.processorCoreExecutionSlots[i]

            if len(currentProcessorSlots) > 1:
                print("Processor " + str(i)),

                for j in range(0, len(currentProcessorSlots)):
                    currentSlot = currentProcessorSlots[j]

                    print("["),

                    if currentSlot.task == None:
                        print("n"),
                    else:
                        print(str(currentSlot.task.id)),

                    print(str(currentSlot.start) + "-" + str(currentSlot.end) + "]--"),
                print()


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
        