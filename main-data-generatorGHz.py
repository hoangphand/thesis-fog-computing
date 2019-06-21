from __future__ import division
from taskDag import TaskDAG
from processorDag import ProcessorDAG
import random

# For processor dag
noOfFogs = 15
noOfClouds = 25

# For task dag
randomAlphas = [0.5, 1.0, 1.5, 2.0]
randomCCR = [0.2, 0.5, 1, 2, 5]
noOfApplications = 10000
randomNoOfTasks = [20, 40, 60, 80, 100]
# deadline requirements
arrivalTime = 0
poissonArrivalRate = 1

processorDag = ProcessorDAG('processors.dag')

# Generate task dags
for id in range(1, noOfApplications + 1):
    # ccr
    ccr = random.choice(randomCCR)
    print(str(id) + ", ccr: " + str(ccr))
    alpha = random.choice(randomAlphas)
    noOfTasks = random.choice(randomNoOfTasks)

    taskDag = TaskDAG()
    taskDag.randomInitLayerBased(id, noOfTasks, alpha, processorDag, ccr)
    taskDag.removeTransitivity()

    # calculate task priority
    avgProcessingRate = processorDag.getAvgProcessingRate()
    avgBandwidth = processorDag.getAvgBandwidth()

    for i in range(0, len(taskDag.layers)):
        layerId = len(taskDag.layers) - i - 1

        for j in range(0, len(taskDag.layers[layerId])):
            taskId = len(taskDag.layers[layerId]) - j - 1

            avgComputationCost = taskDag.layers[layerId][taskId].computationRequired / avgProcessingRate

            if (len(taskDag.layers[layerId][taskId].successors) == 0):
                taskDag.layers[layerId][taskId].priority = avgComputationCost
            else:
                tmpMaxSuccessorCost = -1

                for k in range(0, len(taskDag.layers[layerId][taskId].successors)):
                    currentSuccessor = taskDag.layers[layerId][taskId].successors[k][0]
                    communicationCost = taskDag.layers[layerId][taskId].successors[k][1] / avgBandwidth
                    currentSuccessorCost = communicationCost + currentSuccessor.priority

                    if currentSuccessorCost > tmpMaxSuccessorCost:
                        tmpMaxSuccessorCost = currentSuccessorCost

                taskDag.layers[layerId][taskId].priority = avgComputationCost + tmpMaxSuccessorCost

    taskDag.tasks[0].priority = taskDag.tasks[0].priority + 1

    criticalPath = []
    criticalPathLength = 0
    currentTask = taskDag.tasks[0]

    while currentTask.id != len(taskDag.tasks) - 1:
        topPrioritySuccessorTask = None
        topSuccessorDependency = None

        criticalPathLength += currentTask.computationRequired / avgProcessingRate

        for i in range(0, len(currentTask.successors)):
            currentSuccessorDependency = currentTask.successors[i]
            successorTask = currentSuccessorDependency[0]

            if topPrioritySuccessorTask is None or successorTask.priority > topPrioritySuccessorTask.priority:
                topSuccessorDependency = currentSuccessorDependency
                topPrioritySuccessorTask = successorTask

        criticalPathLength += topSuccessorDependency[1] / avgBandwidth
        currentTask = topPrioritySuccessorTask
        criticalPath.append(taskDag.tasks[currentTask.id])

    taskDag.baseDeadline = criticalPathLength
    taskDag.deadline = random.uniform(criticalPathLength, 2 * criticalPathLength)
    taskDag.arrivalTime = arrivalTime
    taskDag.exportDag('dataset/cp-tr-n10000-5/' + str(taskDag.id) + '.dag')

    arrivalTime = arrivalTime + poissonArrivalRate
