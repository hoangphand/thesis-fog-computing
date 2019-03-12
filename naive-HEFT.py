from processorDag import ProcessorDAG
from taskDag import TaskDAG
from heuristics import Heuristics
import random

sizeOfDataSet = 100
dirDataSet = 'dataset'

processorDag = ProcessorDAG()
processorDag.importDag(dirDataSet + '/processors.dag')

taskDag1 = TaskDAG()
taskDag1.importDag(dirDataSet + '/1.dag')
schedule = Heuristics.HEFT(taskDag1, processorDag)

noOfAcceptedRequests = 0
for id in range(2, sizeOfDataSet + 1):
    taskDag = TaskDAG()
    taskDag.importDag(dirDataSet + '/' + str(id) + '.dag')

    tmpSchedule = Heuristics.DynamicHEFT(schedule, taskDag)
    noOfClouds = tmpSchedule.getNoOfTasksAllocatedToCloudNodes()
    noOfFogs = tmpSchedule.getNoOfTasksAllocatedToFogNodes()

    makespan = tmpSchedule.aft - taskDag.arrivalTime

    if makespan <= taskDag.deadline:
        noOfAcceptedRequests += 1
        schedule.processorExecutionSlots = tmpSchedule.processorExecutionSlots[:]
        print(str(id) + ': accepted, ast: ' + str(tmpSchedule.taskExecutionSlot[0].start))
    else:
        print(str(id) + ': rejected. makespan: ' + str(makespan) + ', deadline: ' + str(taskDag.deadline))

    print('ccr: ' + str(taskDag.ccr) + ', tasks to cloud: ' + str(noOfClouds) + ', tasks to fog: ' + str(noOfFogs))

print("Accepted: " + str(noOfAcceptedRequests))