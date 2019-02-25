from processorDag import ProcessorDAG
import random

processorDag = ProcessorDAG()
# processorDag.random_init()
# processorDag.exportDag('exported-processors.dag')
processorDag.importDag('exported-processors.dag')
processorDag.exportDag('imported-processors.dag')