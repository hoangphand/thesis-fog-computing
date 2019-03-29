from __future__ import division
from __future__ import print_function
from taskGHz import Task
import random
import math

class TaskDAG(object):
    """docstring for TaskDAG"""
    # Attributes
    MIN_LAYERS = 5
    MIN_NODES_PER_LAYER = 1
    MIN_OUT_DEGREE = 1

    # Methods
    def __init__(self):
        super(TaskDAG, self).__init__()
        self.id = -1
        self.alpha = 1.0
        self.tasks = []
        # no of layers in the graph
        self.height = 0
        # no of nodes in each layer
        self.width = 0
        # layers of nodes in the graph
        self.layers = [];
        # deadline requirements
        self.makespanHEFT = 0
        self.k = 0
        self.deadline = 0
        self.arrivalTime = 0
        # ccr
        self.processorDag = None
        self.ccr = 0

        pass

    def randomInitLayerBased(self, id, noOfTasks, alpha, processorDag, ccr):
        self.id = id
        self.alpha = alpha
        # generate randomly number of layers of the graph
        minLayers = self.__class__.MIN_LAYERS
        maxLayers = round(math.sqrt(noOfTasks) / alpha * 2 - minLayers)
        self.height = int(round(random.uniform(minLayers, maxLayers)))

        # determine the min and max number of task nodes per layer
        minNodesPerLayer = self.__class__.MIN_NODES_PER_LAYER
        maxNodesPerLayer = round(math.sqrt(noOfTasks) * alpha * 2 - minNodesPerLayer)

        # initialize a list of empty tasks (with 2 dummy tasks: entry and exit)
        for i in range(0, noOfTasks + 2):
            self.tasks.append(Task(i, 0, 0, 0, 0))

        # add the 'dummy' entry task into the 0th 'dummy' layer
        self.layers.append([self.tasks[0]])
        # a counter to keep track of the current task node
        currentNodeId = 1
        # loop through the graph height to assign task nodes
        # but leave the last one for 'special' assignments
        for i in range(1, self.height):
            # generate randomly number of nodes for each graph layer
            layerWidth = int(round(random.uniform(minNodesPerLayer, maxNodesPerLayer)))
            newLayer = []

            for j in range(0, layerWidth):
                newLayer.append(self.tasks[currentNodeId])
                # generate random constraint values for tasks
                self.tasks[currentNodeId].generateRandomValues()
                # set layer id to task in which task belongs to
                self.tasks[currentNodeId].layerId = i

                currentNodeId += 1

                if (currentNodeId == noOfTasks):
                    break

            # add the new layer into the graph
            self.layers.append(newLayer)

            # stop when the total number of tasks reach the pre-defined number
            if (currentNodeId == noOfTasks):
                break

        # add all the tasks left to the 'last' layer
        newLayer = []
        for i in range(currentNodeId, noOfTasks + 1):
            newLayer.append(self.tasks[currentNodeId])
            self.tasks[currentNodeId].generateRandomValues()
            self.tasks[currentNodeId].layerId = self.height
            currentNodeId += 1

        self.layers.append(newLayer)

        # add a 'dummy' layer for 'dummy' exit task
        self.layers.append([self.tasks[noOfTasks + 1]])
        self.tasks[noOfTasks + 1].layerId = self.height + 1

        # ccr
        self.ccr = ccr
        self.processorDag = processorDag

        # generate edges for the graph
        for i in range(1, len(self.layers) - 2):
            possibleDestinationNodes = []

            # collect all nodes in the higher layers and make them as potential destination nodes
            for j in range(i + 1, len(self.layers) - 1):
                possibleDestinationNodes.extend(self.layers[j])

            # loop through all nodes of the current layer
            for j in range(0, len(self.layers[i])):
                # generate randomly number of out-links for each node
                outDegree = random.randint(self.__class__.MIN_OUT_DEGREE, len(possibleDestinationNodes))
                # choose a random subset of nodes for the collection of potential destination nodes
                destinationNodes = random.sample(possibleDestinationNodes, outDegree)

                # establish links between the current node to all nodes in the selected subset
                for k in range(0, len(destinationNodes)):
                    self.layers[i][j].addEdgeRandomConstraint(destinationNodes[k], self.ccr, self.processorDag)

        # loop through all the task nodes
        for i in range(1, noOfTasks + 1):
            # create links between nodes with no predecessors to the dummy entry task node
            if (len(self.tasks[i].predecessors) == 0):
                self.tasks[0].addEdge(self.tasks[i], 0)

            # create links between nodes with no successors to the dummy exit task node
            if (len(self.tasks[i].successors) == 0):
                self.tasks[i].addEdge(self.tasks[noOfTasks + 1], 0)

        # update graph's height with 'real' number of layers
        self.height = len(self.layers)

        pass

    def printDag(self):
        print("height: " + str(self.height))
        for i in range(0, len(self.layers)):
            for j in range(0, len(self.layers[i])):
                print(self.layers[i][j].id, end=' ')
            print()

    def exportDag(self, outputPath):
        with open(outputPath, "w") as output:
            output.write(str(len(self.tasks) - 2))
            output.write("\n")
            maxIdWidth = len("id")
            maxComputationWidth = len("computation")
            maxStorageWidth = len("storage")
            maxMemoryWidth = len("memory")
            maxPredWidth = len("no_of_preds")

            output.write("{1:<{0}s}\t\t{3:<{2}s}\t\t{5:<{4}s}\t\t{7:<{6}s}\t\t{9:<{8}s}"
                .format(
                    maxIdWidth, "id",
                    maxComputationWidth, "computation",
                    maxStorageWidth, "storage",
                    maxMemoryWidth, "memory",
                    maxPredWidth, "no_of_preds"))

            output.write("\n")

            maxWidthPred = maxIdWidth + maxComputationWidth + maxMemoryWidth + maxPredWidth + 6 * len("\t")

            for index in range(0, len(self.tasks)):
                output.write("{1:<{0}s}".format(maxIdWidth, str(index)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxComputationWidth, str(self.tasks[index].computationRequired)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxStorageWidth, str(self.tasks[index].storageRequired)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxMemoryWidth, str(self.tasks[index].memoryRequired)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxPredWidth, str(len(self.tasks[index].predecessors))))
                output.write("\n")
                for i in range(0, len(self.tasks[index].predecessors)):
                    if self.tasks[index].predecessors[i][1] == 0:
                        output.write("{1:<{0}s}\t\t\t\t\t{2}\t\t{3}".format(maxWidthPred, " ", 
                                                                    str(self.tasks[index].predecessors[i][0].id),
                                                                    str(0)))
                    else:
                        output.write("{1:<{0}s}\t\t\t\t\t{2}\t\t{3}".format(maxWidthPred, " ", 
                                                                    str(self.tasks[index].predecessors[i][0].id),
                                                                    str(self.tasks[index].predecessors[i][1])))
                    output.write("\n")

            output.write("makespanHEFT: " + str(self.makespanHEFT))
            output.write("\n")
            output.write("k: " + str(self.k))
            output.write("\n")
            output.write("deadline: " + str(self.deadline))
            output.write("\n")
            output.write("arrivalTime: " + str(self.arrivalTime))
            output.write("\n")
            output.write("ccr: " + str(self.ccr))
            output.write("\n")
            output.write("alpha: " + str(self.alpha))
            output.write("\n")
            output.write("height: " + str(self.height))
            output.write("\n")
            for i in range(0, len(self.layers)):
                for j in range(0, len(self.layers[i])):
                    output.write(str(self.layers[i][j].id) + " ")
                output.write("\n")
        pass

    def importDag(self, inputFilePath):
        with open(inputFilePath, "r") as input:
            lines = input.readlines()
            noOfTasks = int(''.join(char for char in lines[0] if char.isdigit()))

            self.tasks = []
            for i in range(0, noOfTasks + 2):
                self.tasks.append(Task(i, 0, 0, 0, 0))

            currentLineIndex = 3
            for i in range(1, noOfTasks + 2):
                detailsOfRow = [float(number) for number in lines[currentLineIndex].split()]

                currentTask = self.tasks[int(detailsOfRow[0])]

                currentTask.computationRequired = detailsOfRow[1]
                currentTask.storageRequired = detailsOfRow[2]
                currentTask.memoryRequired = detailsOfRow[3]

                # number of predecessors of the current task
                noOfPredecessors = int(detailsOfRow[4])
                currentLineIndex += 1

                for j in range(0, noOfPredecessors):
                    precedentConstraints = [float(number) for number in lines[currentLineIndex].split()]

                    currentPrecedence = self.tasks[int(precedentConstraints[0])]
                    currentPrecedence.addEdge(currentTask, precedentConstraints[1])
                    currentLineIndex += 1

            # line of makespanHEFT
            self.makespanHEFT = float(lines[currentLineIndex].split()[1])
            currentLineIndex += 1
            # line of k
            self.k = float(lines[currentLineIndex].split()[1])
            currentLineIndex += 1
            # line of deadline
            self.deadline = float(lines[currentLineIndex].split()[1])
            currentLineIndex += 1
            # line of arrivalTime
            self.arrivalTime = float(lines[currentLineIndex].split()[1])
            currentLineIndex += 1
            # line of ccr
            self.ccr = float(lines[currentLineIndex].split()[1])
            currentLineIndex += 1
            # line of alpha
            self.alpha = float(lines[currentLineIndex].split()[1])
            currentLineIndex += 1
            # line of height
            self.height = int(lines[currentLineIndex].split()[1])
            currentLineIndex += 1

            for i in range(0, self.height):
                newLayer = []
                detailsOfRow = [int(number) for number in lines[currentLineIndex].split()]

                for taskId in detailsOfRow:
                    newLayer.append(self.tasks[taskId])
                    self.tasks[taskId].layerId = i

                self.layers.append(newLayer)

                currentLineIndex += 1

        pass

    def totalLinks(self):
        totalLinks = 0
        for i in range(0, len(self.tasks)):
          for j in range(0, len(self.tasks[i].predecessors)):
              if self.tasks[i].predecessors[j][1] != 0:
                  totalLinks += 1

        return totalLinks

    def removeTransitivity(self):
        for srcLayerIndex in range(1, len(self.layers) - 2):
            srcLayer = self.layers[srcLayerIndex]

            for srcTask in srcLayer:
                # print("from: " + str(srcTask.id))

                for destLayerIndex in range(srcLayerIndex + 2, len(self.layers)):
                    for destTask in self.layers[destLayerIndex]:
                        if destTask.id in [successor[0].id for successor in srcTask.successors]:
                            if self.checkIfTransitivity(srcTask, destTask):
                                # print("Transitivity! From " + str(srcTask.id) + " to " + str(destTask.id))
                                srcTask.removeEdge(destTask)
                        else:
                            continue

    def checkIfTransitivity(self, srcTask, destTask):
        visited = []
        path = []

        for i in range(0, len(self.tasks)):
            visited.append(False)

        for i in range(0, len(self.tasks)):
            path.append(-1)

        pathIndex = 0

        return self.checkIfTransitivityAllUtil(srcTask, destTask, visited, path, pathIndex)

    def checkIfTransitivityAllUtil(self, curTask, destTask, visited, path, pathIndex):
        visited[curTask.id] = True
        path[pathIndex] = curTask.id
        pathIndex = pathIndex + 1

        if curTask.id == destTask.id:
            if pathIndex > 2:
                return True
            else:
                return False
        else:
            miniStack = []

            for task in curTask.successors[:]:
                if task[0].layerId < destTask.layerId or task[0].id == destTask.id:
                    miniStack.append(task[0])

            for i in range(0, len(miniStack)):
                if not visited[miniStack[i].id]:
                    return self.checkIfTransitivityAllUtil(miniStack[i], destTask, visited, path, pathIndex)

        pathIndex = pathIndex - 1
        visited[curTask.id] = False
        pass