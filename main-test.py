from task_dag import TaskDAG

dag = TaskDAG()
dag.import_dag('generated_dags/1.dag')
dag.export_dag('exported.dag')