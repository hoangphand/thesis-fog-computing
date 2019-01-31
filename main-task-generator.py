from task_dag import TaskDAG
import random

random_alphas = [0.5, 1.0, 1.5, 2.0]
no_of_tasks = 100

for id in range(1, 101):
    alpha = random.choice(random_alphas)
    dag = TaskDAG()
    dag.random_init(id, no_of_tasks, alpha)
    dag.export_dag('generated-task-dags/' + str(dag.id) + '.dag')
    print(str(id) + ": " + str(alpha))
    # dag.print_dag()