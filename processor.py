import random
from processorCore import ProcessorCore

class Processor(object):
    # metrics: Mbps (megabit per second)
    BANDWIDTH_FOG_LAN = 1024
    BANDWIDTH_CLOUD_LAN = 256
    # BANDWIDTH_LAN_LOWER_BOUND = 1024
    # BANDWIDTH_LAN_UPPER_BOUND = 1024
    BANDWIDTH_WAN_LOWER_BOUND = 10
    BANDWIDTH_WAN_UPPER_BOUND = 100
    BANDWIDTH_WAN = [10, 100, 512, 1024]

    # metrics: MB (megabyte)
    RAM_FOG = [512, 1024]
    # RAM_FOG_LOWER_BOUND = 512
    # RAM_FOG_UPPER_BOUND = 1024
    RAM_CLOUD = [2048, 3072, 4096, 6144, 8192]
    # RAM_CLOUD_LOWER_BOUND = 2048
    # RAM_CLOUD_UPPER_BOUND = 8192

    # metrics: MB (megabyte)
    STORAGE_FOG_LOWER_BOUND = 100
    STORAGE_FOG_UPPER_BOUND = 1024
    STORAGE_CLOUD_LOWER_BOUND = 8192
    STORAGE_CLOUD_UPPER_BOUND = 102400

    FOG_TYPE_1 = 1
    FOG_TYPE_2 = 2
    FOG_TYPE_3 = 3
    FOG_TYPE_4 = 4
    CLOUD_TYPE_1 = 5
    CLOUD_TYPE_2 = 6
    CLOUD_TYPE_3 = 7
    CLOUD_TYPE_4 = 8
    CLOUD_TYPE_5 = 9
    CLOUD_TYPE_6 = 10

    # metrics: GHz (10^9 Hz)
    PROCESSING_RATES = [0, 1.6, 1.8, 2.0, 2.2, 2.6, 2.6, 3.0, 3.0, 3.4, 3.4]
    NO_OF_CORES = [0, 1, 1, 1, 1, 2, 4, 2, 4, 2, 4]
    COST_PER_TIME_UNIT = [0, 0, 0, 0, 0, 1.0, 1.3, 1.6, 1.9, 2.3, 2.6]
    """docstring for Processor"""
    def __init__(self, id, isFog, processorType = 0):
        super(Processor, self).__init__()
        self.id = id
        self.isFog = isFog
        self.processingRate = 0
        self.ram = 0
        self.storage = 0
        self.wanUploadBandwidth = 0
        self.wanDownloadBandwidth = 0
        self.noOfCores = 0
        self.costPerTimeUnit = 0

        if (processorType != 0):
            self.noOfCores = self.__class__.NO_OF_CORES[processorType]
            self.processingRate = self.__class__.PROCESSING_RATES[processorType]
            self.costPerTimeUnit = self.__class__.COST_PER_TIME_UNIT[processorType]
            self.generateRandomValues()

    def generateRandomValues(self):
        if (self.isFog):
            # self.ram = int(random.uniform(self.__class__.RAM_FOG_LOWER_BOUND, 
            #                             self.__class__.RAM_FOG_UPPER_BOUND))
            self.ram = random.choice(self.__class__.RAM_FOG)
            self.storage = int(random.uniform(self.__class__.STORAGE_FOG_LOWER_BOUND, 
                                        self.__class__.STORAGE_FOG_UPPER_BOUND))
        else:
            # self.ram = int(random.uniform(self.__class__.RAM_CLOUD_LOWER_BOUND, 
            #                             self.__class__.RAM_CLOUD_UPPER_BOUND))
            self.ram = random.choice(self.__class__.RAM_CLOUD)
            self.storage = int(random.uniform(self.__class__.STORAGE_CLOUD_LOWER_BOUND, 
                                        self.__class__.STORAGE_CLOUD_UPPER_BOUND))

        # self.wanUploadBandwidth = random.choice(self.__class__.BANDWIDTH_WAN)
        # self.wanDownloadBandwidth = random.choice(self.__class__.BANDWIDTH_WAN)
        self.wanUploadBandwidth = int(random.uniform(self.__class__.BANDWIDTH_WAN_LOWER_BOUND, 
                                                    self.__class__.BANDWIDTH_WAN_UPPER_BOUND))
        self.wanDownloadBandwidth = int(random.uniform(self.__class__.BANDWIDTH_WAN_LOWER_BOUND, 
                                                    self.__class__.BANDWIDTH_WAN_UPPER_BOUND))