import time
import traceback
from Domein.Domeincontroller import DomeinController
from Infrastructure.BewellApi.MessageController import MessageController
from Infrastructure.BewellApi.PatientController import PatientController
from Infrastructure.SQLServer_QueueDB.SQLLogService import LogService
from Infrastructure.SQLServer_QueueDB.connectionproviders.SQlServerConnectionProvider import (
    SQLServerConnectionProvider,
)
from Domein.LogController import LoggingController
from GlobalSettings import standbyDelay, maindelay
from Infrastructure.SQLServer_QueueDB.TaskService import TaskService
from GlobalSettings import quedb_settings


# als er niets wordt gevonden
class Program:
    def __init__(self) -> None:
        sqlServerConnectionData=quedb_settings
        connectionprovider=SQLServerConnectionProvider(
                    server=sqlServerConnectionData["server"],
                    database=sqlServerConnectionData["database"],
                    username=sqlServerConnectionData["username"],
                    password=sqlServerConnectionData["password"],
                    driver=sqlServerConnectionData["driver"])
        self.logger = LoggingController(
            persitencelogService = LogService(
                connectionprovider= connectionprovider))
        self.active = True
        self.running=True
            

    def standBy(self):
        if self.active == True:
            self.logger.info("standing by")
            self.active = False
        time.sleep(standbyDelay)

    # als er een task gevonden is
    def activate(self):
        if self.active == False:
            self.logger.info("activating")
            self.active = True
        time.sleep(maindelay)

    def stop(self):
        self.running=False
        self.logger.warning("terminating")
        del self
    
    # main program logic
    def main(self):
        """the main initialization and programloop for the taskmanager_queueManager logic"""
        # service injection
        try:
            sqlServerConnectionData=quedb_settings
            taskService = TaskService(
                connectionprovider=SQLServerConnectionProvider(
                    server=sqlServerConnectionData["server"],
                    database=sqlServerConnectionData["database"],
                    username=sqlServerConnectionData["username"],
                    password=sqlServerConnectionData["password"],
                    driver=sqlServerConnectionData["driver"]))

            messageService = MessageController()
            patientService = PatientController()
            queuemanager = DomeinController(
                loggingService=self.logger,
                taskService=taskService,
                messageService=messageService,
                patientservice=patientService,
            )
        except Exception as e:
            self.logger.error(f"er ging iets mis bij het initializeren van de taskmanager: {traceback.format_exception(e)}")
            self.stop()
        # program loop
        while self.running:
            try:
                response = queuemanager.process_task()
            except Exception as e:
                self.logger.error(f"er ging iets mis bij het het runnen van het programma: {traceback.format_exception(e)}")
            if response == "active":
                self.activate()
            else:
                self.standBy()
