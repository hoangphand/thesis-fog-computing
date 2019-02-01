from __future__ import division
from processor_dag import ProcessorDAG
from processor import Processor
from task_dag import TaskDAG
from slot import Slot
import sys

class Schedule(object):
    """docstring for Schedule"""
    def __init__(self, task_dag, processor_dag):
        super(Schedule, self).__init__()
        self.task_dag = task_dag
        self.processor_dag = processor_dag
        self.is_scheduled = False
        self.task_execution_slot = []
        self.processor_execution_slots = []

        for i in range(0, len(processor_dag.processors)):
            current_processor = processor_dag.processors[i]
            self.processor_execution_slots.append([Slot(None, current_processor, 0, sys.maxint)])

        for i in range(0, len(task_dag.tasks)):
            self.task_execution_slot.append(None)

    def add_new_slot(self, processor, task, start_time):
        current_processor_slots = self.processor_execution_slots[processor.id]

        computation_time = task.computation_required / processor.processing_rate
        to_be_taken_slot = start_time + computation_time

        for i in range(0, len(current_processor_slots)):
            current_slot = current_processor_slots[i]
            if current_slot.start <= start_time and current_slot.end >= to_be_taken_slot:
                start = start_time
                end = to_be_taken_slot

                new_slot = Slot(task, processor, start, end)
                current_processor_slots.append(new_slot)

                if start != current_slot.start and end != current_slot.end:
                    before_slot = Slot(None, processor, current_slot.start, start)
                    after_slot = Slot(None, processor, end, current_slot.end)

                    current_processor_slots.append(before_slot)
                    current_processor_slots.append(after_slot)
                elif start == current_slot.start and end != current_slot.end:
                    after_slot = Slot(None, processor, end, current_slot.end)
                    current_processor_slots.append(after_slot)
                elif start != current_slot.start and end == current_slot.end:
                    before_slot = Slot(None, processor, current_slot.start, start)
                    current_processor_slots.append(before_slot)

                del current_processor_slots[i]

                # sort all the slots in an increasing order based on start time
                current_processor_slots.sort(key = lambda el: el.start, reverse = True)
                # store execution slot of task for easy retrieving
                self.task_execution_slot[task.id] = new_slot
                print("Task " + str(task.id) + ", processor " + str(processor.id) + ", processing_time " + str(computation_time) + ": start " + str(start) + ", end " + str(end))

                break


    def can_add_slot(self, processor, task, start_time):
        is_allowed_to_add_slot = False

        computation_time = task.computation_required / processor.processing_rate
        to_be_taken_slot = start_time + computation_time

        current_processor_slots = self.processor_execution_slots[processor_id]

        for i in range(0, len(current_processor_slots)):
            current_slot = current_processor_slots[i]

            if current_slot.start <= start_time and current_slot.end >= to_be_taken_slot:
                is_allowed_to_add_slot = True
                break

        return is_allowed_to_add_slot

    def get_best_slot_for_task_on_processor(self, processor, task):
        ready_time = -1

        for i in range(0, len(task.predecessors)):
            pred_task = task.predecessors[i][0]
            pred_task_constraint = task.predecessors[i][1]
            pred_processor = self.task_execution_slot[pred_task.id].processor

            communication_time = ProcessorDAG.get_communication_time(pred_processor, processor, pred_task_constraint)

            predecessor_slot_end = self.task_execution_slot[pred_task.id].end
            current_ready_time = predecessor_slot_end + communication_time

            if current_ready_time > ready_time:
                ready_time = current_ready_time

        processing_time = task.computation_required / processor.processing_rate

        current_processor_slots = self.processor_execution_slots[processor.id]

        for i in range(0, len(current_processor_slots)):
            current_slot = current_processor_slots[i]

            if current_slot.task == None:
                actual_start = max(current_slot.start, ready_time)
                actual_end = actual_start + processing_time

                if actual_end <= current_slot.end:
                    return Slot(task, processor, actual_start, actual_end)
            else:
                continue

        return Slot(task, processor, -1, -1)

    def get_ready_time_of_tasks(self,):
        pass

    def makespan(self):
        pass

    def cloud_cost(self):
        pass

    def print_schedule(self):
        pass

    def export(self, output_path):
        pass
        