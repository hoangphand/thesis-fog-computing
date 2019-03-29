from __future__ import print_function
import random
from processorGHz import Processor

class ProcessorDAG(object):
    """docstring for ProcessorDAG"""
    def __init__(self, inputFilePath = None):
        super(ProcessorDAG, self).__init__()

        if (inputFilePath == None):
            self.noOfFogs = 12
            self.noOfClouds = 5

            self.processors = []

            self.processors.append(Processor(0, True, Processor.FOG_TYPE_1))
            self.processors.append(Processor(1, True, Processor.FOG_TYPE_1))
            self.processors.append(Processor(2, True, Processor.FOG_TYPE_1))
            self.processors.append(Processor(3, True, Processor.FOG_TYPE_2))
            self.processors.append(Processor(4, True, Processor.FOG_TYPE_2))
            self.processors.append(Processor(5, True, Processor.FOG_TYPE_2))
            self.processors.append(Processor(6, True, Processor.FOG_TYPE_3))
            self.processors.append(Processor(7, True, Processor.FOG_TYPE_3))
            self.processors.append(Processor(8, True, Processor.FOG_TYPE_3))
            self.processors.append(Processor(9, True, Processor.FOG_TYPE_4))
            self.processors.append(Processor(10, True, Processor.FOG_TYPE_4))
            self.processors.append(Processor(11, True, Processor.FOG_TYPE_4))
            self.processors.append(Processor(12, False, Processor.CLOUD_TYPE_1))
            self.processors.append(Processor(13, False, Processor.CLOUD_TYPE_2))
            self.processors.append(Processor(14, False, Processor.CLOUD_TYPE_3))
            self.processors.append(Processor(15, False, Processor.CLOUD_TYPE_4))
            self.processors.append(Processor(16, False, Processor.CLOUD_TYPE_5))
        else:
            self.importDag(inputFilePath)

    def exportDag(self, outputFilePath):
        with open(outputFilePath, "w") as output:
            output.write(str(self.noOfFogs))
            output.write("\n")
            output.write(str(self.noOfClouds))
            output.write("\n")
            maxIdWidth = len("id")
            maxIsFogWidth = len("is fog?")
            maxNoOfCoresWidth = len("no of cores")
            maxProcRateWidth = len("proc. rate")
            maxRamWidth = len("ram   ")
            maxStorageWidth = len("storage")
            maxUpBandwidth = len("up band.")
            maxDownBandwidth = len("down band.")
            maxCostPerTimeUnit = len("cost")

            output.write("{1:<{0}s}\t\t{3:<{2}s}\t\t{5:<{4}s}\t\t{7:<{6}s}\t\t{9:<{8}s}\t\t{11:<{10}s}\t\t{13:<{12}s}\t\t{15:<{14}s}\t\t{17:<{16}s}"
                .format(
                    maxIdWidth, "id",
                    maxIsFogWidth, "is fog?",
                    maxProcRateWidth, "proc. rate",
                    maxNoOfCoresWidth, "no of cores",
                    maxRamWidth, "ram   ",
                    maxStorageWidth, "storage",
                    maxUpBandwidth, "up band.",
                    maxDownBandwidth, "down band.",
                    maxCostPerTimeUnit, "cost"))

            output.write("\n")

            maxWidthPred = maxIdWidth + maxIsFogWidth + maxProcRateWidth + maxNoOfCoresWidth + maxRamWidth + maxStorageWidth + maxUpBandwidth + maxDownBandwidth + maxCostPerTimeUnit + 12 * len("\t")

            for index in range(0, len(self.processors)):
                output.write("{1:<{0}s}".format(maxIdWidth, str(index)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxIsFogWidth, str(self.processors[index].isFog)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxProcRateWidth, str(self.processors[index].processingRate)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxNoOfCoresWidth, str(self.processors[index].noOfCores)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxRamWidth, str(self.processors[index].ram)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxStorageWidth, str(self.processors[index].storage)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxUpBandwidth, str(self.processors[index].wanUploadBandwidth)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxDownBandwidth, str(self.processors[index].wanDownloadBandwidth)))
                output.write("\t\t")
                output.write("{1:<{0}s}".format(maxCostPerTimeUnit, str(self.processors[index].costPerTimeUnit)))
                output.write("\n")

    def importDag(self, inputFilePath):
        with open(inputFilePath, "r") as input:
            lines = input.readlines()
            self.noOfFogs = int(''.join(char for char in lines[0] if char.isdigit()))
            self.noOfClouds = int(''.join(char for char in lines[1] if char.isdigit()))

            currentLineIndex = 3

            self.processors = []
            for i in range(0, self.noOfFogs + self.noOfClouds):
                detailsOfRow = [int(number) for number in lines[currentLineIndex].split()[3:8]]

                isFog = lines[currentLineIndex].split()[1] == "True"

                newProcessor = Processor(i, isFog)
                newProcessor.processingRate = float(lines[currentLineIndex].split()[2])
                newProcessor.costPerTimeUnit = float(lines[currentLineIndex].split()[8])
                newProcessor.noOfCores = detailsOfRow[0]
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

    def getCommunicationTimeBetweenProcessors(self, fromProcessor, toProcessor, amountOfData):
        communicationTime = 0

        if fromProcessor.id == toProcessor.id:
            communicationTime = 0
        else:           
            bandwidthToUse = self.getBandwidthToUse(fromProcessor, toProcessor)
            
            communicationTime = amountOfData / bandwidthToUse
        
        return communicationTime

    def getCommunicationTimeBetweenCores(self, fromProcessorCore, toProcessorCore, amountOfData):
        communicationTime = 0

        if fromProcessorCore.processor.id == toProcessorCore.processor.id:
            communicationTime = 0
        else:           
            bandwidthToUse = self.getBandwidthToUse(fromProcessorCore.processor, toProcessorCore.processor)
            
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