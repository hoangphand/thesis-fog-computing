from __future__ import print_function
import random
from processor import Processor

class ProcessorDAG(object):
    NUMBER_OF_FOGS_LOWER_BOUND = 15
    NUMBER_OF_FOGS_UPPER_BOUND = 15
    NUMBER_OF_CLOUDS_LOWER_BOUND = 25
    NUMBER_OF_CLOUDS_UPPER_BOUND = 25

    """docstring for ProcessorDAG"""
    def __init__(self, noOfFogs = 0, noOfClouds = 0):
        super(ProcessorDAG, self).__init__()
        self.noOfFogs = noOfFogs
        self.noOfClouds = noOfClouds
        self.processors = []
        
    def randomInit(self):
        # self.noOfFogs = int(random.uniform(self.__class__.NUMBER_OF_FOGS_LOWER_BOUND, 
        #     self.__class__.NUMBER_OF_FOGS_UPPER_BOUND))
        # self.noOfClouds = int(random.uniform(self.__class__.NUMBER_OF_CLOUDS_LOWER_BOUND, 
        #     self.__class__.NUMBER_OF_CLOUDS_UPPER_BOUND))

        index = 0
        for i in range(0, self.noOfFogs):
            newFog = Processor(i, True)
            newFog.generateRandomValues()
            self.processors.append(newFog)
            index = i

        for i in range(index, self.noOfFogs + self.noOfClouds):
            newCloud = Processor(i, False)
            newCloud.generateRandomValues()
            self.processors.append(newCloud)

    def exportDag(self, outputFilePath):
        with open(outputFilePath, "w") as output:
            output.write(str(self.noOfFogs))
            output.write("\n")
            output.write(str(self.noOfClouds))
            output.write("\n")
            maxIdWidth = len("id")
            maxIsFogWidth = len("is fog?")
            maxProcRateWidth = len("proc. rate")
            maxRamWidth = len("ram   ")
            maxStorageWidth = len("storage")
            maxUpBandwidth = len("up band.")
            maxDownBandwidth = len("down band.")

            output.write("{1:<{0}s}\t\t{3:<{2}s}\t\t{5:<{4}s}\t\t{7:<{6}s}\t\t{9:<{8}s}\t\t{11:<{10}s}\t\t{13:<{12}s}"
                .format(
                    maxIdWidth, "id",
                    maxIsFogWidth, "is fog?",
                    maxProcRateWidth, "proc. rate",
                    maxRamWidth, "ram   ",
                    maxStorageWidth, "storage",
                    maxUpBandwidth, "up band.",
                    maxDownBandwidth, "down band."))

            output.write("\n")

            maxWidthPred = maxIdWidth + maxIsFogWidth + maxProcRateWidth + maxRamWidth + maxStorageWidth + maxUpBandwidth + maxDownBandwidth + 12 * len("\t")

            for index in range(0, len(self.processors)):
                output.write("{1:<{0}s}".format(maxIdWidth, str(index)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxIsFogWidth, str(self.processors[index].isFog)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxProcRateWidth, str(self.processors[index].processingRate)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxRamWidth, str(self.processors[index].ram)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxStorageWidth, str(self.processors[index].storage)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxUpBandwidth, str(self.processors[index].wanUploadBandwidth)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxDownBandwidth, str(self.processors[index].wanDownloadBandwidth)))
                output.write("\n")

    def importDag(self, inputFilePath):
        with open(inputFilePath, "r") as input:
            lines = input.readlines()
            self.noOfFogs = int(''.join(char for char in lines[0] if char.isdigit()))
            self.noOfClouds = int(''.join(char for char in lines[1] if char.isdigit()))

            currentLineIndex = 3

            self.processors = []
            for i in range(0, self.noOfFogs + self.noOfClouds):
                detailsOfRow = [int(number) for number in lines[currentLineIndex].split()[2:7]]

                isFog = lines[currentLineIndex].split()[1] == "True"

                newProcessor = Processor(i, isFog)
                newProcessor.processingRate = detailsOfRow[0]
                newProcessor.ram = detailsOfRow[1]
                newProcessor.storage = detailsOfRow[2]
                newProcessor.wanUploadBandwidth = detailsOfRow[3]
                newProcessor.wanDownloadBandwidth = detailsOfRow[4]

                self.processors.append(newProcessor)

                currentLineIndex += 1

    def getMostPowerfulProcessor(self):
        mostPowerfulProcessor = self.processors[0]

        for i in range(1, len(self.processors)):
            if self.processors[i].processingRate > mostPowerfulProcessor.processingRate:
                mostPowerfulProcessor = self.processors[i]
        
        return mostPowerfulProcessor

    def getBandwidthToUse(self, fromProcessor, toProcessor):
        bandwidthToUse = 0

        if fromProcessor.isFog and toProcessor.isFog:
            bandwidthToUse = Processor.BANDWIDTH_LAN
        else:
            bandwidthToUse = min(fromProcessor.wanUploadBandwidth, toProcessor.wanDownloadBandwidth)
        
        # print(bandwidthToUse)
        return bandwidthToUse

    def getCommunicationTime(self, fromProcessor, toProcessor, amountOfData):
        communicationTime = 0

        if fromProcessor.id == toProcessor.id:
            communicationTime = 0
        else:           
            bandwidthToUse = self.getBandwidthToUse(fromProcessor, toProcessor)
            
            communicationTime = amountOfData / bandwidthToUse
        
        return communicationTime

    def getTotalUploadBandwidth(self):
        totalBandwidth = 0

        for i in range(0, self.noOfFogs + self.noOfClouds):
            totalBandwidth += self.processors[i].wanUploadBandwidth

        return totalBandwidth

    def getTotalDownloadBandwidth(self):
        totalBandwidth = 0

        for i in range(0, self.noOfFogs + self.noOfClouds):
            totalBandwidth += self.processors[i].wanDownloadBandwidth

        return totalBandwidth

    def getTotalProcessingRate(self):
        totalProcessingRate = 0

        for i in range(0, self.noOfFogs + self.noOfClouds):
            totalProcessingRate += self.processors[i].processingRate

        return totalProcessingRate

    def getAvgProcessingRate(self):
        return self.getTotalProcessingRate() / (self.noOfClouds + self.noOfFogs)

    def getAvgUploadBandwidth(self):
        return self.getTotalUploadBandwidth() / (self.noOfClouds + self.noOfFogs)

    def getAvgDownloadBandwidth(self):
        return self.getTotalDownloadBandwidth() / (self.noOfClouds + self.noOfFogs)