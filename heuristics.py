from schedule import Schedule

class Heuristics(object):
    """docstring for Heuristics"""
    def __init__(self):
        super(Heuristics, self).__init__()
        pass

    def HEFT(dag, processor_dag):
        new_schedule = Schedule(dag, processor_dag)

        # prioritize tasks
        pass