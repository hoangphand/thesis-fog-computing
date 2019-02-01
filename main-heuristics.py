# from __future__ import print_function
from processor_dag import ProcessorDAG
from task_dag import TaskDAG
from heuristics import Heuristics
import random

processor_dag = ProcessorDAG()
processor_dag.import_dag('exported-processors.dag')

task_dag = TaskDAG()
task_dag.import_dag('generated-task-dags/6.dag')
task_dag.print_dag()

# ranks = Heuristics.prioritize_tasks(task_dag, processor_dag)
# for i in range(0, len(ranks)):
#     print(str(i) + ": " + str(ranks[i]))

# sorted_indices = sorted(range(len(ranks)), key = ranks.__getitem__, reverse = True)
# for i in range(0, len(ranks)):
#     print(str(sorted_indices[i]) + ": " + str(ranks[sorted_indices[i]]))

schedule = Heuristics.HEFT(task_dag, processor_dag)

# for i in range(0, len(ranks)):
#     # print(str(sorted_indices[i]) + ": " + str(ranks[sorted_indices[i]]))
# # for i in range(0, len(schedule.task_execution_slot)):
#     current_slot = schedule.task_execution_slot[sorted_indices[i]]

#     if current_slot != None:
#         print("Task " + str(current_slot.task.id) + ", processor " + str(current_slot.processor.id) + ": " + str(current_slot.start) + ", " + str(current_slot.end))
#     else:
#         print("Task " + str(i) + ": None")

# for i in range(0, len(schedule.processor_execution_slots)):
#     print("Processor " + str(i) + ":")
#     current_processor_slots = schedule.processor_execution_slots[i]

#     for j in range(0, len(current_processor_slots)):
#         current_slot = current_processor_slots[j]

#         if current_slot.task == None:
#             print("Task " + str(j) + ": " + str(current_slot.start) + ", " + str(current_slot.end))
#         else:
#             print("None: " + str(current_slot.start) + ", " + str(current_slot.end))