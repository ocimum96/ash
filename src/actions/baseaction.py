''' 
Base action class.
Extend BaseAction class to create a new action.
'''

from abc import ABC, abstractmethod
from common.logger import Logger
import logging

class BaseAction(ABC):

    ERR_CODE_NO_ERROR = 0
    ERR_CODE_INVALID_PARAM = 1
    ERR_CODE_UNKNOWN_ERR = 8
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        super().__init__()
    
    @abstractmethod
    def exec(self, **kwargs):
        logger = Logger.getLogger(__name__)
        if logger.level <= logging.DEBUG:
            for k, v in kwargs.items():
                logger.debug("Passed args key: {}, value: {}".format(k,v))
        logger.info("Ran action: {}".format(self.name))
        return self.ERR_CODE_NO_ERROR
        