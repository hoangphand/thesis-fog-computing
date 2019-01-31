from __future__ import division
from __future__ import print_function
from task import Task
import random
import math

class TaskDAG(object):
    """docstring for TaskDAG"""
    # Attributes

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

        pass

    def random_init(self, id, no_of_tasks, alpha):
        self.id = id
        # generate randomly number of layers of the graph
        min_layers = 3
        max_layers = round(math.sqrt(no_of_tasks) / alpha * 2 - min_layers)
        self.height = int(round(random.uniform(min_layers, max_layers)))

        # determine the min and max number of task nodes per layer
        min_nodes_per_layer = 1
        max_nodes_per_layer = round(math.sqrt(no_of_tasks) * alpha * 2 - min_nodes_per_layer)

        # probability of having an edge from a node to another one
        probability = (1 + math.exp(1)) * math.log(no_of_tasks) / no_of_tasks

        # initialize a list of empty tasks (with 2 dummy tasks: entry and exit)
        for i in range(0, no_of_tasks + 2):
            self.tasks.append(Task(i, 0, 0, 0, 0))

        # add the 'dummy' entry task into the 0th 'dummy' layer
        self.layers.append([self.tasks[0]])
        # a counter to keep track of the current task node
        current_node_id = 1
        # loop through the graph height to assign task nodes
        # but leave the last one for 'special' assignments
        total_nodes = 0
        for i in range(1, self.height):
            # generate randomly number of nodes for each graph layer
            layer_width = int(round(random.uniform(min_nodes_per_layer, max_nodes_per_layer)))
            new_layer = []

            for j in range(0, layer_width):
                new_layer.append(self.tasks[current_node_id])
                # generate random constraint values for tasks
                self.tasks[current_node_id].generate_random_values()
                # set layer id to task in which task belongs to
                self.tasks[current_node_id].layer_id = i

                current_node_id += 1

                if (current_node_id == no_of_tasks):
                    break

            # add the new layer into the graph
            self.layers.append(new_layer)

            # stop when the total number of tasks reach the pre-defined number
            if (current_node_id == no_of_tasks):
                break

        # add all the tasks left to the 'last' layer
        new_layer = []
        for i in range(current_node_id, no_of_tasks + 1):
            new_layer.append(self.tasks[current_node_id])
            self.tasks[current_node_id].generate_random_values()
            self.tasks[current_node_id].layer_id = self.height
            current_node_id += 1

        self.layers.append(new_layer)

        # add a 'dummy' layer for 'dummy' exit task
        self.layers.append([self.tasks[no_of_tasks + 1]])
        self.tasks[no_of_tasks + 1].layer_id = self.height + 1

        # generate edges for the graph
        for i in range(1, no_of_tasks + 1):
            for j in range(i, no_of_tasks + 1):
                if self.tasks[i].layer_id < self.tasks[j].layer_id:
                    random_probability = random.random()

                    if random_probability < probability:
                        self.tasks[i].add_edge_random_constraint(self.tasks[j])

        for i in range(1, no_of_tasks + 1):
            if (len(self.tasks[i].predecessors) == 0):
                self.tasks[0].add_edge(self.tasks[i], 0)

            if (len(self.tasks[i].successors) == 0):
                self.tasks[i].add_edge(self.tasks[no_of_tasks + 1], 0)

        self.height = len(self.layers)

        pass

    def print_dag(self):
        print("height: " + str(self.height))
        for i in range(0, len(self.layers)):
            for j in range(0, len(self.layers[i])):
                print(self.layers[i][j].id, end=' ')
            print()

    def export_dag(self, output_path):
        with open(output_path, "w") as output:
            output.write(str(len(self.tasks) - 2))
            output.write("\n")
            max_id_width = len("id")
            max_computation_width = len("computation")
            max_storage_width = len("storage")
            max_memory_width = len("memory")
            max_pred_width = len("no_of_preds")

            output.write("{1:<{0}s}\t\t{3:<{2}s}\t\t{5:<{4}s}\t\t{7:<{6}s}\t\t{9:<{8}s}"
                .format(
                    max_id_width, "id",
                    max_computation_width, "computation",
                    max_storage_width, "storage",
                    max_memory_width, "memory",
                    max_pred_width, "no_of_preds"))

            output.write("\n")

            max_width_pred = max_id_width + max_computation_width + max_memory_width + max_pred_width + 6 * len("\t")

            for index in range(0, len(self.tasks)):
                output.write("{1:<{0}s}".format(max_id_width, str(index)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_computation_width, str(self.tasks[index].computation_required)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_storage_width, str(self.tasks[index].storage_required)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_memory_width, str(self.tasks[index].memory_required)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(max_pred_width, str(len(self.tasks[index].predecessors))))
                output.write("\n")
                for i in range(0, len(self.tasks[index].predecessors)):
                    output.write("{1:<{0}s}\t\t\t\t\t{2}\t\t{3}".format(max_width_pred, " ", 
                                                                str(self.tasks[index].predecessors[i][0].id),
                                                                str(self.tasks[index].predecessors[i][1])))
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

    def import_dag(self, input_file_path):
        with open(input_file_path, "r") as input:
            lines = input.readlines()
            no_of_tasks = int(''.join(char for char in lines[0] if char.isdigit()))

            self.tasks = []
            for i in range(0, no_of_tasks + 2):
                self.tasks.append(Task(i, 0, 0, 0, 0))

            current_line_index = 3
            for i in range(1, no_of_tasks + 2):
                details_of_row = [float(number) for number in lines[current_line_index].split()]

                current_task = self.tasks[int(details_of_row[0])]

                current_task.computation_required = details_of_row[1]
                current_task.storage_required = details_of_row[2]
                current_task.memory_required = details_of_row[3]

                # number of predecessors of the current task
                no_of_predecessors = int(details_of_row[4])
                current_line_index += 1

                for j in range(0, no_of_predecessors):
                    precedent_constraints = [float(number) for number in lines[current_line_index].split()]

                    current_precedence = self.tasks[int(precedent_constraints[0])]
                    current_precedence.add_edge(current_task, precedent_constraints[1])
                    current_line_index += 1

            # line of alpha
            self.alpha = float(lines[current_line_index].split()[1])
            current_line_index += 1

            self.height = int(lines[current_line_index].split()[1])
            current_line_index += 1

            for i in range(0, self.height):
                new_layer = []
                details_of_row = [int(number) for number in lines[current_line_index].split()]

                for task_id in details_of_row:
                    new_layer.append(self.tasks[task_id])
                    self.tasks[task_id].layer_id = i

                self.layers.append(new_layer)

                current_line_index += 1

        pass