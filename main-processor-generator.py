from __future__ import division
from processorDag import ProcessorDAG
import random

processorDag = ProcessorDAG(15, 25)
processorDag.randomInit()
# processorDag.exportDag('exported-processors.dag')
# processorDag.importDag('exported-processors.dag')
# processorDag.exportDag('imported-processors.dag')

print("Up bandwidth:")
totalUploadBandwidth = processorDag.getTotalUploadBandwidth()
print(totalUploadBandwidth)
print("Down bandwidth:")
totalDownloadBandwidth = processorDag.getTotalDownloadBandwidth()
print(totalDownloadBandwidth)
print("Processing rate:")
totalProcessingRate = processorDag.getTotalProcessingRate() / 100
# totalProcessingRate = processorDag.getTotalProcessingRate()
print(totalProcessingRate)
print("Total links:")
totalLinks = 1000

# MIN_COMM = 100
# MAX_COMM = 500
# MIN_COMP = 50
# MAX_COMP = 500
MIN_COMM = 10
MAX_COMM = 100
MIN_COMP = 2
MAX_COMP = 60

CCR = [0.1, 1, 10]

for i in range(0, len(CCR)):
    print("CCR: " + str(CCR[i]))

    if CCR[i] < 1:
        minComp = MIN_COMP
        maxComp = MAX_COMP
        minComm = minComp * ((totalUploadBandwidth / totalLinks) * CCR[i]) / totalProcessingRate
        maxComm = maxComp * ((totalUploadBandwidth / totalLinks) * CCR[i]) / totalProcessingRate
    elif CCR[i] > 1:
        minComm = MIN_COMM
        maxComm = MAX_COMM
        minComp = minComm * totalProcessingRate / ((totalUploadBandwidth / totalLinks) * CCR[i])
        maxComp = maxComm * totalProcessingRate / ((totalUploadBandwidth / totalLinks) * CCR[i])
    else:
        minComp = MIN_COMP
        maxComp = MAX_COMP
        minComm = minComp * ((totalUploadBandwidth / totalLinks) * CCR[i]) / totalProcessingRate
        maxComm = maxComp * ((totalUploadBandwidth / totalLinks) * CCR[i]) / totalProcessingRate

    print("COMP[" + str(minComp) + ", " + str(maxComp) + "] ~ COMM[" + str(minComm) + ", " + str(maxComm) + "]")