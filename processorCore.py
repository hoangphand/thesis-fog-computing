from __future__ import division
import sys

class ProcessorCore(object):
    """docstring for Schedule"""
    def __init__(self, processor, coreId, schedulePositionId):
        super(ProcessorCore, self).__init__()
        self.processor = processor
        self.coreId = coreId
        self.schedulePositionId = schedulePositionId