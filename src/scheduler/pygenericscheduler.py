'''
Use the importlib to import the action module and run it.
'''

from scheduler.basescheduler import BaseScheduler
from actions.factory import ActionFactory
from common.logger import Logger


class PyGenericScheduler(BaseScheduler):
    def __init__(self, actionName, description=None):
        super().__init__("Py-Generic", actionName, True, description=description)
    
    def Schedule(self, **kwargs):
        l = Logger.getLogger(__name__)
        try:
            action = ActionFactory.GetAction(self.ActionName)       
            if action is not None:
                try:
                    action.exec(**kwargs)
                except Exception as e:
                    l.critical("Exception on running action {} ".format(self.ActionName))
                    l.warn(e)
                else:
                    return super().Schedule(**kwargs)
        except Exception as e:
            l.critical("Error while creating action object. {}".format(self.ActionName))
            l.debug(e)