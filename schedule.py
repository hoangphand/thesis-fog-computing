class Schedule(object):
	"""docstring for Schedule"""
	def __init__(self, dag, processor_dag):
		super(Schedule, self).__init__()
		self.dag = dag
		self.is_scheduled = False
		self.processor_dag = processor_dag
		self.schedule_details = []

		for i in range(0, len(processor_dag)):
			self.schedule_details.append([])

	def makespan(self):
		pass

	def cloud_cost(self):
		pass

	def print(self):
		pass

	def export(self, output_path):
		pass
		