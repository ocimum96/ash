
'''
Params: 
--config-file : config file
--scheduler : type of scheduler [optional;defaults from configfile]
--action : what action to run. (eg: scan-sbom points to actions.scan-sbom.py action file)

Wrapper file which reads the configs and schedule a job based on input params.

'''

from scheduler.factory import SchedulerFactory
import argparse

if __name__ == "__main__":
    argParse = argparse.ArgumentParser()
    argParse.add_argument("--config-file", metavar='-c', nargs=1, default="config.json", required=False, \
        help="pass config file path")
    argParse.add_argument("--scheduler", default="PyGenericScheduler", \
        help="scheduler name to be used.", metavar='-s', required=False)
    argParse.add_argument("--action", nargs='+', default=["SimpleLogAction", "Hello, world."], \
        required=False, metavar='-a', help="action to be executed.")
    # argParse.add_argument()
    args = argParse.parse_args()
    
    s = SchedulerFactory.GetScheduler(args.scheduler, taskName=args.action[0])
    thisActionArgsDict = {}
    for actionArgMap in args.action[1:] :
        (k, x, v) = actionArgMap.rpartition('=')
        thisActionArgsDict[k] = v
    s.Schedule(**thisActionArgsDict)