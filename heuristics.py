from __future__ import division
from processor_dag import ProcessorDAG
# from schedule import Schedule

class Heuristics(object):
    """docstring for Heuristics"""
    def __init__(self):
        super(Heuristics, self).__init__()
        pass

    @staticmethod
    def HEFT(dag, processor_dag):
        # new_schedule = Schedule(dag, processor_dag)

        # prioritize tasks
        ranks = Heuristics.prioritize_tasks(dag, processor_dag)
        sorted_indices = sorted(range(len(ranks)), key = ranks.__getitem__, reverse = True)

        print(sorted_indices)

        return ranks

    @staticmethod
    def prioritize_tasks(dag, processor_dag):
    	total_processing_rate = 0
        total_upload_bandwidth = 0

        for i in range(0, len(processor_dag.processors)):
        	total_processing_rate += processor_dag.processors[i].processing_rate
        	total_upload_bandwidth += processor_dag.processors[i].wan_upload_bandwidth

        total_no_of_processors = len(processor_dag.processors)

        avg_processing_rate = total_processing_rate / total_no_of_processors
        avg_upload_bandwidth = total_upload_bandwidth / total_no_of_processors

        ranks = []

        for i in range(0, len(dag.tasks)):
        	ranks.append(0)

        for i in range(0, len(dag.layers)):
        	layer_id = len(dag.layers) - i - 1

        	for j in range(0, len(dag.layers[layer_id])):
        		task_id = len(dag.layers[layer_id]) - j - 1

        		# print(dag.layers[layer_id][task_id].id)

        		avg_computation_cost = dag.layers[layer_id][task_id].computation_required / avg_processing_rate

        		if (len(dag.layers[layer_id][task_id].successors) == 0):
        			ranks[dag.layers[layer_id][task_id].id] = avg_computation_cost
        		else:
	        		tmp_max_successor_cost = -1

	        		for k in range(0, len(dag.layers[layer_id][task_id].successors)):
	        			current_successor = dag.layers[layer_id][task_id].successors[k][0]
	        			communication_cost = dag.layers[layer_id][task_id].successors[k][1] / avg_upload_bandwidth
	        			current_successor_cost = communication_cost + ranks[current_successor.id]

	        			if current_successor_cost > tmp_max_successor_cost:
	        				tmp_max_successor_cost = current_successor_cost

	        		ranks[dag.layers[layer_id][task_id].id] = avg_computation_cost + tmp_max_successor_cost
    	
    	return ranks