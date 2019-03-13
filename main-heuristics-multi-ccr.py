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

randomCCR = [0.1, 0.5, 1, 2, 10]
randomAlphas = [0.5, 1.0, 1.5, 2.0]
noOfTasks = 100
# deadline requirements
arrivalTime = 0
poissonArrivalRate = 0.1
k = 1.2

# Generate task dags
for id in range(0, len(randomCCR)):
    # ccr
    ccr = random.choice(randomCCR)
    print(ccr)
    alpha = random.choice(randomAlphas)

    taskDag = TaskDAG()
    taskDag.randomInitLayerBased(id, noOfTasks, alpha, processorDag, ccr)
    taskDag.removeTransitivity()

    # deadline requirements
    schedule = Heuristics.HEFT(taskDag, processorDag)
    taskDag.makespanHEFT = schedule.aft
    taskDag.k = k
    taskDag.deadline = taskDag.makespanHEFT * taskDag.k
    taskDag.arrivalTime = arrivalTime
    taskDag.exportDag('ccr' + str(ccr) + '.dag')

    arrivalTime = arrivalTime + poissonArrivalRate

for i in range(0, len(randomCCR)):
	ccr = randomCCR[i]
	taskDag = TaskDAG()
	# taskDag.importDag('dataset-PHAM/1.dag')
	taskDag.importDag('ccr' + str(ccr) + '.dag')
	print("ccr: " + str(ccr))
	# taskDag.importDag('exported-tasks.dag')

	schedule = Heuristics.HEFT(taskDag, processorDag)
	# print("AFT: " + str(schedule.aft))

	# print("Total computation cost: " + str(schedule.getTotalComputationCost()))
	# print("Avg computation cost: " + str(schedule.getTotalComputationCost() / (len(taskDag.tasks) - 2)))

	# print("Total communication cost: " + str(schedule.getTotalCommunicationCost()))
	# print("Total links: " + str(taskDag.totalLinks()))
	# print("Avg communication cost: " + str(schedule.getTotalCommunicationCost() / (taskDag.totalLinks())))

	# print("No of tasks allocated on fog nodes: " + str(schedule.getNoOfTasksAllocatedToFogNodes()))
	# print("No of tasks allocated on cloud nodes: " + str(schedule.getNoOfTasksAllocatedToCloudNodes()))

	totalCCR = 0
	for i in range(0, len(taskDag.tasks)):
	    taskComputationCost = schedule.getComputationCostOfTask(i)
	    maxPredCommunicationCost = schedule.getMaxPredCommunicationCost(i)

	    ccr = 0
	    if maxPredCommunicationCost != 0 and taskComputationCost != 0:
	        ccr = maxPredCommunicationCost / taskComputationCost

	    totalCCR += ccr
	    # print("Task " + str(i) + ", computation cost: " + str(taskComputationCost) + 
	    #     ", max pred communication: " + str(maxPredCommunicationCost) +
	    #     ", ccr: " + str(ccr))

	print("avg CCR: " + str(totalCCR / (len(taskDag.tasks) - 2)))