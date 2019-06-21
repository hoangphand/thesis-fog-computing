from __future__ import division
from processorDag import ProcessorDAG
from taskDag import TaskDAG
from schedule import Schedule
from collections import deque
import sys

class Heuristics(object):
    """docstring for Heuristics"""
    def __init__(self):
        super(Heuristics, self).__init__()
        pass

    @staticmethod
    def HEFT(taskDag, processorDag):
        schedule = Schedule(taskDag, processorDag)

        # prioritize tasks
        ranks = Heuristics.prioritizeTasks(taskDag, processorDag)
        sortedIndices = sorted(range(len(ranks)), key = ranks.__getitem__, reverse = True)

        # print(sortedIndices)
        # init list of unscheduled tasks
        unscheduledTasks = deque(sortedIndices)
        # get the entry task by popping the first task from the unscheduled list
        entryTask = taskDag.tasks[unscheduledTasks.popleft()]
        # get the most powerful processor in the network
        # mostPowerfulProcessor = processorDag.getMostPowerfulProcessor()
        # allocate dummy entry task on the first processing node at timestamp 0
        schedule.addNewSlot(schedule.processorCoreExecutionSlots[0][0].processorCore, entryTask, 0)

        # loop through all unscheduled tasks
        while (len(unscheduledTasks) > 0):
            currentTask = taskDag.tasks[unscheduledTasks.popleft()]

            # calculate ready time to calculate current task on all the processors in the network
            selectedSlot = None
            selectedProcessorCore = None

            # loop through all processors to find the best processing execution location
            for i in range(0, len(schedule.processorCoreExecutionSlots)):
                currentProcessorCore = schedule.processorCoreExecutionSlots[i][0].processorCore
                # find the first-fit slot on the current processor for the current task
                currentSelectedSlot = schedule.getFirstFitSlotForTaskOnProcessorCore(currentProcessorCore, currentTask)

                if selectedSlot == None or currentSelectedSlot.end < selectedSlot.end:
                    selectedSlot = currentSelectedSlot
                    selectedProcessorCore = currentProcessorCore

            schedule.addNewSlot(selectedProcessorCore, currentTask, selectedSlot.start)

        schedule.aft = schedule.taskExecutionSlot[len(taskDag.tasks) - 1].end

        return schedule

    @staticmethod
    def DynamicHEFT(schedule, taskDag):
        schedule = schedule.cloneTrialSchedule(taskDag)

        # prioritize tasks
        ranks = Heuristics.prioritizeTasks(schedule.taskDag, schedule.processorDag)
        sortedIndices = sorted(range(len(ranks)), key = ranks.__getitem__, reverse = True)

        # print(sortedIndices)
        # init list of unscheduled tasks
        unscheduledTasks = deque(sortedIndices)
        # get the entry task by popping the first task from the unscheduled list
        entryTask = schedule.taskDag.tasks[unscheduledTasks.popleft()]
        # get the most powerful processor in the network
        # mostPowerfulProcessor = schedule.processorDag.getMostPowerfulProcessor()
        earliestProcessorForEntryTask = schedule.getFirstProcessorFreeAt(taskDag.arrivalTime)
        # allocate dummy entry task on the most powerful processing node at timestamp 0
        schedule.addNewSlot(earliestProcessorForEntryTask, entryTask, taskDag.arrivalTime)
        # schedule.addNewSlot(mostPowerfulProcessor, entryTask, 0)

        # loop through all unscheduled tasks
        while (len(unscheduledTasks) > 0):
            currentTask = schedule.taskDag.tasks[unscheduledTasks.popleft()]
            # print("task: " + str(currentTask.id))

            # calculate ready time to calculate current task on all the processors in the network
            selectedSlot = None
            selectedProcessor = None

            # loop through all processors to find the best processing execution location
            for i in range(0, len(schedule.processorDag.processors)):
                currentProcessor = schedule.processorDag.processors[i]
                # find the best slot on the current processor
                currentSelectedSlot = schedule.getFirstFitSlotForTaskOnProcessor(currentProcessor, currentTask)

                if selectedSlot == None or currentSelectedSlot.end < selectedSlot.end:
                    selectedSlot = currentSelectedSlot
                    selectedProcessor = currentProcessor

            schedule.addNewSlot(selectedProcessor, currentTask, selectedSlot.start)

        schedule.aft = schedule.taskExecutionSlot[len(taskDag.tasks) - 1].end

        return schedule

    @staticmethod
    def prioritizeTasks(taskDag, processorDag):
        totalProcessingRate = 0
        totalUploadBandwidth = 0

        for i in range(0, len(processorDag.processors)):
            totalProcessingRate += processorDag.processors[i].processingRate
            totalUploadBandwidth += processorDag.processors[i].wanUploadBandwidth

        totalNoOfProcessors = len(processorDag.processors)

        avgProcessingRate = totalProcessingRate / totalNoOfProcessors
        avgUploadBandwidth = totalUploadBandwidth / totalNoOfProcessors

        ranks = []

        for i in range(0, len(taskDag.tasks)):
            ranks.append(0)

        for i in range(0, len(taskDag.layers)):
            layerId = len(taskDag.layers) - i - 1

            for j in range(0, len(taskDag.layers[layerId])):
                taskId = len(taskDag.layers[layerId]) - j - 1

                avgComputationCost = taskDag.layers[layerId][taskId].computationRequired / avgProcessingRate

                if (len(taskDag.layers[layerId][taskId].successors) == 0):
                    ranks[taskDag.layers[layerId][taskId].id] = avgComputationCost
                else:
                    tmpMaxSuccessorCost = -1

                    for k in range(0, len(taskDag.layers[layerId][taskId].successors)):
                        currentSuccessor = taskDag.layers[layerId][taskId].successors[k][0]
                        communicationCost = taskDag.layers[layerId][taskId].successors[k][1] / avgUploadBandwidth
                        currentSuccessorCost = communicationCost + ranks[currentSuccessor.id]

                        if currentSuccessorCost > tmpMaxSuccessorCost:
                            tmpMaxSuccessorCost = currentSuccessorCost

                    ranks[taskDag.layers[layerId][taskId].id] = avgComputationCost + tmpMaxSuccessorCost
        
        return ranks