from processor_dag import ProcessorDAG
import random

processor_dag = ProcessorDAG()
# processor_dag.random_init()
# processor_dag.export_dag('exported-processors.dag')
processor_dag.import_dag('exported-processors.dag')
processor_dag.export_dag('imported-processors.dag')