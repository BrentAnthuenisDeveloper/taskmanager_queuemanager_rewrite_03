# todo: implement logging logic
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

from Infrastructure.SQLServer_QueueDB.SQLLogService import LogService
from Infrastructure.SQLServer_QueueDB.Model.Log import Log
from GlobalSettings import loglevel,sqlserverLogLevel,InfoLogFilePath,warningLogFilePath

class LoggingController:
    def __init__(self,persitencelogService:LogService) -> None:
        #handlers
        
        DebugFileHandler=RotatingFileHandler("logs/info.log",maxBytes=1e6, backupCount=3)
        DebugFileHandler.setLevel(logging.INFO)
        WarningFileHandler=RotatingFileHandler("logs/warning.log",maxBytes=1e6, backupCount=3)
        WarningFileHandler.setLevel(logging.WARNING)
        consoleHandler=logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)

        #formatters
        formatter01=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        DebugFileHandler.setFormatter(formatter01)
        WarningFileHandler.setFormatter(formatter01)
        consoleHandler.setFormatter(formatter01)

        #loggers
        taskManagerLogger = logging.getLogger("taskmanager")
        taskManagerLogger.setLevel(loglevel)
        taskManagerLogger.addHandler(DebugFileHandler)
        taskManagerLogger.addHandler(WarningFileHandler)
        taskManagerLogger.addHandler(consoleHandler)

        self.taskManagerLogger=taskManagerLogger
        self.logService=persitencelogService
        
    def _log(self, message: str,level:int) -> None:
        if level<sqlserverLogLevel:
            self.logService.insertLog(Log(message=message,level=logging.getLevelName(level)))
    def debug(self, message: str) -> None:
        self._log(message,10)
        self.taskManagerLogger.debug(message)
    def info(self, message: str) -> None:
        self._log(message,20)
        self.taskManagerLogger.info(message)
    def warning(self, message: str) -> None:
        self._log(message,30)
        self.taskManagerLogger.warning(message)
    def error(self, message: str) -> None:
        self._log(message,40)
        self.taskManagerLogger.error(message)
    def critical(self, message: str) -> None:
        self._log(message,50)
        self.taskManagerLogger.critical(message)
