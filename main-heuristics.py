from __future__ import print_function
from __future__ import division
from processorDag import ProcessorDAG
from taskDag import TaskDAG
from heuristics import Heuristics
import random

processorDag = ProcessorDAG()
# processorDag.importDag('dataset-PHAM/processors.dag')
processorDag.importDag('dataset/processors.dag')
# processorDag.importDag('exported-processors.dag')

taskDag = TaskDAG()
# taskDag.importDag('dataset-PHAM/1.dag')
taskDag.importDag('dataset/10.dag')
# taskDag.importDag('exported-tasks.dag')

schedule = Heuristics.HEFT(taskDag, processorDag)
print("AFT: " + str(schedule.aft))

print("Total computation cost: " + str(schedule.getTotalComputationCost()))
print("Avg computation cost: " + str(schedule.getTotalComputationCost() / (len(taskDag.tasks) - 2)))

print("Total communication cost: " + str(schedule.getTotalCommunicationCost()))
print("Total links: " + str(taskDag.totalLinks()))
print("Avg communication cost: " + str(schedule.getTotalCommunicationCost() / (taskDag.totalLinks())))

print("No of tasks allocated on fog nodes: " + str(schedule.getNoOfTasksAllocatedToFogNodes()))
print("No of tasks allocated on cloud nodes: " + str(schedule.getNoOfTasksAllocatedToCloudNodes()))

for i in range(0, len(taskDag.tasks)):
    taskComputationCost = schedule.getComputationCostOfTask(i)
    maxPredCommunicationCost = schedule.getMaxPredCommunicationCost(i)

    ccr = 0
    if maxPredCommunicationCost != 0 and taskComputationCost != 0:
        ccr = maxPredCommunicationCost / taskComputationCost

    print("Task " + str(i) + ", computation cost: " + str(taskComputationCost) + 
        ", max pred communication: " + str(maxPredCommunicationCost) +
        ", ccr: " + str(ccr))