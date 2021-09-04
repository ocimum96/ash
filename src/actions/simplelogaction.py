
from actions.baseaction import BaseAction
from common.logger import Logger

class SimpleLogAction(BaseAction):
    def __init__(self, name, description=None):
        super().__init__(name, description=description)

    def exec(self, **kwargs):
        Logger.getLogger(__name__).info("simple log action executed.")
        return super().exec(**kwargs)
