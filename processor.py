import random

class Processor(object):
    # metrics: Mbps (megabit per second)
    BANDWIDTH_LAN = 1024
    # BANDWIDTH_LAN_LOWER_BOUND = 1024
    # BANDWIDTH_LAN_UPPER_BOUND = 1024
    BANDWIDTH_WAN_LOWER_BOUND = 10
    BANDWIDTH_WAN_UPPER_BOUND = 100
    BANDWIDTH_WAN = [10, 100, 512, 1024]

    # metrics: MIPS (millions of instructions per second)
    PROCESSING_RATE_FOG_LOWER_BOUND = 10
    PROCESSING_RATE_FOG_UPPER_BOUND = 500
    PROCESSING_RATE_CLOUD_LOWER_BOUND = 250
    PROCESSING_RATE_CLOUD_UPPER_BOUND = 1500

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
    """docstring for Processor"""
    def __init__(self, id, isFog):
        super(Processor, self).__init__()
        self.id = id
        self.isFog = isFog
        self.processingRate = 0
        self.ram = 0
        self.storage = 0
        self.wanUploadBandwidth = 0
        self.wanDownloadBandwidth = 0

    def generateRandomValues(self):
        if (self.isFog):
            self.processingRate = int(random.uniform(self.__class__.PROCESSING_RATE_FOG_LOWER_BOUND, 
                                                    self.__class__.PROCESSING_RATE_FOG_UPPER_BOUND))
            # self.ram = int(random.uniform(self.__class__.RAM_FOG_LOWER_BOUND, 
            #                             self.__class__.RAM_FOG_UPPER_BOUND))
            self.ram = random.choice(self.__class__.RAM_FOG)
            self.storage = int(random.uniform(self.__class__.STORAGE_FOG_LOWER_BOUND, 
                                        self.__class__.STORAGE_FOG_UPPER_BOUND))
        else:
            self.processingRate = int(random.uniform(self.__class__.PROCESSING_RATE_CLOUD_LOWER_BOUND, 
                                                    self.__class__.PROCESSING_RATE_CLOUD_UPPER_BOUND))
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