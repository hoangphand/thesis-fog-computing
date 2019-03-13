from processorDag import ProcessorDAG
from taskDag import TaskDAG
from heuristics import Heuristics
import random
import copy

sizeOfDataSet = 100
noOfDagsToTest = 30
dirDataSet = 'dataset'

processorDag = ProcessorDAG()
processorDag.importDag(dirDataSet + '/processors.dag')

taskDag1 = TaskDAG()
taskDag1.importDag(dirDataSet + '/1.dag')
schedule = Heuristics.HEFT(taskDag1, processorDag)

makespan = schedule.aft - taskDag1.arrivalTime
print('\x1b[0;30;44m app 1 ACCEPTED!!! \x1b[0m')
print('makespan: ' + str(makespan) + ', deadline: ' + str(taskDag1.deadline) + ', ccr: ' + str(taskDag1.ccr))
print('ast: ' + str(schedule.taskExecutionSlot[0].start) + 
    ', aft: ' + str(schedule.taskExecutionSlot[len(taskDag1.tasks) - 1].end))
# print('no of slots: ' + str(schedule.countSlotsInNetwork()))
print("================================")

noOfAcceptedRequests = 1
for id in range(2, noOfDagsToTest + 1):
# for id in range(2, sizeOfDataSet + 1):
    taskDag = TaskDAG()
    taskDag.importDag(dirDataSet + '/' + str(id) + '.dag')
    taskDag.id = id

    tmpSchedule = Heuristics.DynamicHEFT(copy.deepcopy(schedule), taskDag)
    noOfClouds = tmpSchedule.getNoOfTasksAllocatedToCloudNodes()
    noOfFogs = tmpSchedule.getNoOfTasksAllocatedToFogNodes()

    makespan = tmpSchedule.aft - taskDag.arrivalTime

    if makespan <= taskDag.deadline:
        noOfAcceptedRequests += 1
        schedule.processorExecutionSlots = tmpSchedule.processorExecutionSlots[:]
        print('\x1b[6;30;42m app ' + str(id) + ': ACCEPTED!!! \x1b[0m')
    else:
        print('\x1b[0;30;41m app ' + str(id) + ': rejected \x1b[0m')

    print('makespan: ' + str(makespan) + ', deadline: ' + str(taskDag.deadline))
    print('ast: ' + str(tmpSchedule.taskExecutionSlot[0].start) + 
        ', aft: ' + str(tmpSchedule.taskExecutionSlot[len(taskDag.tasks) - 1].end))
    print('ccr: ' + str(taskDag.ccr) + ', tasks to cloud: ' + str(noOfClouds) + ', tasks to fog: ' + str(noOfFogs))
    # print('no of slots: ' + str(schedule.countSlotsInNetwork()))
    print("================================")

print("Accepted: " + str(noOfAcceptedRequests))