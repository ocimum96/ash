'''
Helper class to create action instances required.
'''

from common.application import Application
from common.logger import Logger
from common.utils import PluginHelper
from actions.baseaction import BaseAction

class ActionFactory:
    
    @staticmethod
    def GetAction(name):
        l = Logger.getLogger(__name__)
        if name is None or name == '':
            return None
        config = {}
        try:
            config = Application.GetInstance().ConfigData["actions"][name]
            l.debug("Config for {}".format(name))
            l.debug(config)
        except Exception as e:
            l.warning("Config err for action : {} ".format(name))
            return None
        
        if config["enabled"] == False :
            l.debug("{} is disabled.".format(name))
            return None
        
        registered_action = None
        
        try:
            actionModuleName = config["module"]
            klass = PluginHelper.GetPlugin(actionModuleName)
            registered_action = klass(name=name, description=None)   
        except Exception as e:
            l.error("Error creating action instance {} ".format(name))
            return None
        
        if registered_action is None:
            l.error("Could not enable module {} ".format(actionModuleName))
            raise Exception("Module created is None.")
        else:
            if isinstance(registered_action, BaseAction):
                l.info("Created instace for action {} ".format(name))
                return registered_action
            else:
                raise Exception("Not an Action type instance")
        
            
        