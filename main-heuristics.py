# from __future__ import print_function
from processorDag import ProcessorDAG
from taskDag import TaskDAG
from heuristics import Heuristics
import random

processorDag = ProcessorDAG()
processorDag.importDag('exported-processors.dag')

taskDag = TaskDAG()
taskDag.importDag('generated-task-dags/6.dag')
taskDag.printDag()

# ranks = Heuristics.prioritize_tasks(taskDag, processorDag)
# for i in range(0, len(ranks)):
#     print(str(i) + ": " + str(ranks[i]))

# sortedIndices = sorted(range(len(ranks)), key = ranks.__getitem__, reverse = True)
# for i in range(0, len(ranks)):
#     print(str(sortedIndices[i]) + ": " + str(ranks[sortedIndices[i]]))

schedule = Heuristics.HEFT(taskDag, processorDag)

# for i in range(0, len(ranks)):
#     # print(str(sortedIndices[i]) + ": " + str(ranks[sortedIndices[i]]))
# # for i in range(0, len(schedule.taskExecutionSlot)):
#     currentSlot = schedule.taskExecutionSlot[sortedIndices[i]]

#     if currentSlot != None:
#         print("Task " + str(currentSlot.task.id) + ", processor " + str(currentSlot.processor.id) + ": " + str(currentSlot.start) + ", " + str(currentSlot.end))
#     else:
#         print("Task " + str(i) + ": None")

# for i in range(0, len(schedule.processorExecutionSlots)):
#     print("Processor " + str(i) + ":")
#     currentProcessorSlots = schedule.processorExecutionSlots[i]

#     for j in range(0, len(currentProcessorSlots)):
#         currentSlot = currentProcessorSlots[j]

#         if currentSlot.task == None:
#             print("Task " + str(j) + ": " + str(currentSlot.start) + ", " + str(currentSlot.end))
#         else:
#             print("None: " + str(currentSlot.start) + ", " + str(currentSlot.end))