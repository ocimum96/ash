
from importlib import import_module
from common.logger import Logger

               
class PluginHelper:
    @staticmethod
    def GetPlugin(name):
        l = Logger.getLogger(__name__)
        klass = None
        if name is None or name == '':
            raise Exception("Module name cannot be empty.")
        try:
            (module, x, classname) = name.rpartition('.')

            if module == '' or module is None:
                raise Exception("Module name {} is invalid".format(name))
            mod = import_module(module)
            klass = getattr(mod, classname)
        except Exception as ex:
            l.error("Could not enable module %s - %s" % (name, str(ex)))
            return None
        return klass
