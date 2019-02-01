from __future__ import division
from processor_dag import ProcessorDAG
from task_dag import TaskDAG
from schedule import Schedule
from collections import deque
import sys

class Heuristics(object):
    """docstring for Heuristics"""
    def __init__(self):
        super(Heuristics, self).__init__()
        pass

    @staticmethod
    def HEFT(task_dag, processor_dag):
        schedule = Schedule(task_dag, processor_dag)

        # prioritize tasks
        ranks = Heuristics.prioritize_tasks(task_dag, processor_dag)
        sorted_indices = sorted(range(len(ranks)), key = ranks.__getitem__, reverse = True)

        # print(sorted_indices)
        # init list of unscheduled tasks
        unscheduled_tasks = deque(sorted_indices)
        # get the entry task by popping the first task from the unscheduled list
        entry_task = task_dag.tasks[unscheduled_tasks.popleft()]
        # get the most powerful processor in the network
        most_powerful_processor = processor_dag.get_most_powerful_processor()

        schedule.add_new_slot(most_powerful_processor, entry_task, 0)

        count = 0
        # loop through all unscheduled tasks
        while (len(unscheduled_tasks) > 0):
            current_task = task_dag.tasks[unscheduled_tasks.popleft()]

            # calculate ready time to calculate current task on all the processors in the network
            best_slot = None
            best_aft = sys.maxint
            best_processor = None

            for i in range(0, len(processor_dag.processors)):
                current_processor = processor_dag.processors[i]
                current_best_slot = schedule.get_best_slot_for_task_on_processor(current_processor, current_task)

                if current_best_slot.end < best_aft:
                    best_aft = current_best_slot.end
                    best_slot = current_best_slot
                    best_processor = current_processor

            schedule.add_new_slot(best_processor, current_task, best_slot.start)

        return schedule

    @staticmethod
    def prioritize_tasks(task_dag, processor_dag):
        total_processing_rate = 0
        total_upload_bandwidth = 0

        for i in range(0, len(processor_dag.processors)):
            total_processing_rate += processor_dag.processors[i].processing_rate
            total_upload_bandwidth += processor_dag.processors[i].wan_upload_bandwidth

        total_no_of_processors = len(processor_dag.processors)

        avg_processing_rate = total_processing_rate / total_no_of_processors
        avg_upload_bandwidth = total_upload_bandwidth / total_no_of_processors

        ranks = []

        for i in range(0, len(task_dag.tasks)):
            ranks.append(0)

        for i in range(0, len(task_dag.layers)):
            layer_id = len(task_dag.layers) - i - 1

            for j in range(0, len(task_dag.layers[layer_id])):
                task_id = len(task_dag.layers[layer_id]) - j - 1

                avg_computation_cost = task_dag.layers[layer_id][task_id].computation_required / avg_processing_rate

                if (len(task_dag.layers[layer_id][task_id].successors) == 0):
                    ranks[task_dag.layers[layer_id][task_id].id] = avg_computation_cost
                else:
                    tmp_max_successor_cost = -1

                    for k in range(0, len(task_dag.layers[layer_id][task_id].successors)):
                        current_successor = task_dag.layers[layer_id][task_id].successors[k][0]
                        communication_cost = task_dag.layers[layer_id][task_id].successors[k][1] / avg_upload_bandwidth
                        current_successor_cost = communication_cost + ranks[current_successor.id]

                        if current_successor_cost > tmp_max_successor_cost:
                            tmp_max_successor_cost = current_successor_cost

                    ranks[task_dag.layers[layer_id][task_id].id] = avg_computation_cost + tmp_max_successor_cost
        
        return ranks