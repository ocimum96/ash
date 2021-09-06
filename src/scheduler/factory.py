'''
Helper class to create scheduler instances required.
'''

from common.application import Application
from common.logger import Logger
from common.utils import PluginHelper
from scheduler.basescheduler import BaseScheduler

class SchedulerFactory:
    
    @staticmethod
    def GetScheduler(name, taskName):
        l = Logger.getLogger(__name__)
        if name is None or name == '':
            return None
        config = {}
        try:
            config = Application.GetInstance().ConfigData["schedulers"][name]
            l.debug("Config for {}".format(name))
            l.debug(config)
        except Exception as e:
            l.warning("Config err for scheduler : {} ".format(name))
            return None
        
        if config["enabled"] == False :
            l.debug("Scheduler {} is disabled.".format(name))
            return None
        
        registered_scheduler = None
        
        try:
            schedulerModuleName = config["module"]
            klass = PluginHelper.GetPlugin(schedulerModuleName)
            registered_scheduler = klass(actionName = taskName, description=None)  #duck typing here
        except Exception as e:
            l.error("Error creating scheduler instance {} ".format(name))
            return None
        
        if registered_scheduler is None:
            l.error("Could not enable module {} ".format(schedulerModuleName))
            raise Exception("Module created is None.")
        else:
            if isinstance(registered_scheduler, BaseScheduler):
                l.info("Created instace for scheduler {} ".format(name))
                return registered_scheduler
            else:
                l.critical("Failed to create an action instance.")
                raise Exception("Not a Scheduler type instance")
        
            
        