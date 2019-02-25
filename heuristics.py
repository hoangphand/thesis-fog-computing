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
        ranks = Heuristics.prioritize_tasks(taskDag, processorDag)
        sortedIndices = sorted(range(len(ranks)), key = ranks.__getitem__, reverse = True)

        # print(sortedIndices)
        # init list of unscheduled tasks
        unscheduledTasks = deque(sortedIndices)
        # get the entry task by popping the first task from the unscheduled list
        entryTask = taskDag.tasks[unscheduledTasks.popleft()]
        # get the most powerful processor in the network
        mostPowerfulProcessor = processorDag.getMostPowerfulProcessor()

        schedule.add_new_slot(mostPowerfulProcessor, entryTask, 0)

        count = 0
        # loop through all unscheduled tasks
        while (len(unscheduledTasks) > 0):
            currentTask = taskDag.tasks[unscheduledTasks.popleft()]

            # calculate ready time to calculate current task on all the processors in the network
            bestSlot = None
            bestAFT = sys.maxint
            bestProcessor = None

            for i in range(0, len(processorDag.processors)):
                currentProcessor = processorDag.processors[i]
                currentBestSlot = schedule.getBestSlotForTaskOnProcessor(currentProcessor, currentTask)

                if currentBestSlot.end < bestAFT:
                    bestAFT = currentBestSlot.end
                    bestSlot = currentBestSlot
                    bestProcessor = currentProcessor

            schedule.add_new_slot(bestProcessor, currentTask, bestSlot.start)

        return schedule

    @staticmethod
    def prioritize_tasks(taskDag, processorDag):
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
                        current_successor = taskDag.layers[layerId][taskId].successors[k][0]
                        communication_cost = taskDag.layers[layerId][taskId].successors[k][1] / avgUploadBandwidth
                        currentSuccessorCost = communication_cost + ranks[current_successor.id]

                        if currentSuccessorCost > tmpMaxSuccessorCost:
                            tmpMaxSuccessorCost = currentSuccessorCost

                    ranks[taskDag.layers[layerId][taskId].id] = avgComputationCost + tmpMaxSuccessorCost
        
        return ranks