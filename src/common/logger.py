import logging

class Logger:
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.DEBUG

    @staticmethod
    def getLogger(loggerName):
        logger = logging.getLogger(loggerName)
        logger.setLevel(Logger.log_level)
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter(Logger.log_format)
        streamHandler.setFormatter(formatter)

        logger.addHandler(streamHandler)
        return logger