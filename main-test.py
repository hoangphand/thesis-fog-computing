from taskDag import TaskDAG

dag = TaskDAG()
dag.importDag('generated_dags/1.dag')
dag.exportDag('exported.dag')