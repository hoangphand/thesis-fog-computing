# from __future__ import print_function
from processor_dag import ProcessorDAG
from task_dag import TaskDAG
from heuristics import Heuristics
import random

processor_dag = ProcessorDAG()
processor_dag.import_dag('exported-processors.dag')

task_dag = TaskDAG()
task_dag.import_dag('generated-task-dags/3.dag')
task_dag.print_dag()

ranks = Heuristics.HEFT(task_dag, processor_dag)

for i in range(0, len(ranks)):
	print(str(i) + ": " + str(ranks[i]))