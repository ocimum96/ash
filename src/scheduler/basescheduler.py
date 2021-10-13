'''
Extend BaseScheduler to create a new scheduler.
'''

from abc import ABC, abstractmethod
from common.logger import Logger
import logging

class BaseScheduler(ABC):
    def __init__(self, schedulerName, actionName, isBlocking, description=None):
        self.SchedulerName = schedulerName
        self.ActionName = actionName
        self.IsBlocking = isBlocking
        self.Description = description
        super().__init__()

    @abstractmethod
    def Schedule(self, **kwargs):
        if Logger.log_level <= logging.INFO:
            l = Logger.getLogger(__name__)
            if self.IsBlocking:
                l.info("Ran action {} using scheduler {}.".format(self.ActionName, \
                    self.SchedulerName))
            else:
                l.info("Scheduled action {} using scheduler {}.".format(self.ActionName, \
                    self.SchedulerName))
    
    # @abstractmethod
    # def FallbackScedule(self, **kwargs):
    #     l = Logger.getLogger(__name__)
    #     l.warn("Scheduler {} is not available.".format(self.SchedulerName))
