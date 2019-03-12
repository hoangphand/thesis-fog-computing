from taskDag import TaskDAG

sizeOfDataSet = 100
poissonArrivalRate = 0.4
arrivalTime = poissonArrivalRate
dirDataSet = 'dataset'

for id in range(2, sizeOfDataSet + 1):
	print(id)
	taskDag = TaskDAG()
	taskDag.importDag(dirDataSet + '/' + str(id) + '.dag')
	taskDag.arrivalTime = arrivalTime 
	taskDag.exportDag(dirDataSet + '/' + str(id) + '.dag')

	arrivalTime = arrivalTime + poissonArrivalRate