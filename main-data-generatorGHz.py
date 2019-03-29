from __future__ import division
from taskDagGHz import TaskDAG
from processorDagGHz import ProcessorDAG
import random
from heuristicsGHz import Heuristics

# For processor dag
noOfFogs = 15
noOfClouds = 25

# For task dag
randomAlphas = [0.5, 1.0, 1.5, 2.0]
randomCCR = [0.2, 0.5, 1, 2, 5]
noOfApplications = 100
noOfTasks = 100
# deadline requirements
arrivalTime = 0
poissonArrivalRate = 0.1
k = 1.2

# Generate processing nodes
processorDag = ProcessorDAG('processors.dag')
# processorDag = ProcessorDAG()
# processorDag.exportDag('processors1.dag')

# Generate task dags
for id in range(1, noOfApplications + 1):
    # ccr
    ccr = random.choice(randomCCR)
    print(str(id) + ", ccr: " + str(ccr))
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
    taskDag.exportDag('dataset-GHz/' + str(taskDag.id) + '.dag')

    arrivalTime = arrivalTime + poissonArrivalRate