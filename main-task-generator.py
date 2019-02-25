from taskDag import TaskDAG
import random

randomAlphas = [0.5, 1.0, 1.5, 2.0]
noOfTasks = 100

# for id in range(1, 101):
#     alpha = random.choice(randomAlphas)
#     dag = TaskDAG()
#     # dag.randomInitProb(id, noOfTasks, alpha)
#     dag.randomInitLayerBased(id, noOfTasks, alpha)
#     dag.exportDag('generated-task-dags/' + str(dag.id) + '.dag')
#     print(str(id) + ": " + str(alpha))
#     # dag.printDag()


id = 111
alpha = random.choice(randomAlphas)
dag = TaskDAG()
# dag.randomInitProb(id, noOfTasks, alpha)
# dag.randomInitLayerBased(id, noOfTasks, alpha)
# # dag.randomInitAjacentLayer(id, noOfTasks, alpha)
# dag.exportDag('generated-task-dags/' + str(dag.id) + '.dag')
# print("len dag: " + str(len(dag.layers)))

importedDag = TaskDAG()
importedDag.importDag('generated-task-dags/' + str(id) + '.dag')
print("len dag: " + str(len(importedDag.layers)))

importedDag.removeTransitivity()

# print(str(id) + ": " + str(alpha))