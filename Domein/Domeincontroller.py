import json
import time
import traceback
from typing import Any
from GlobalSettings import statuses
from Infrastructure.BewellApi.Model.MessagePost import Content, File, MessagePost
from Infrastructure.SQLServer_QueueDB.Model.Task import Task
from Infrastructure.BewellApi.MessageController import MessageController
from Infrastructure.BewellApi.PatientController import PatientController
from Domein.LogController import LoggingController
from Infrastructure.SQLServer_QueueDB.TaskService import TaskService


class DomeinController:
    def __init__(
        self,
        loggingService: LoggingController,
        taskService: TaskService,
        messageService: MessageController,
        patientservice: PatientController,
    ) -> None:
        # services
        self._loggingService = loggingService
        self._taskService = taskService
        self._messageService = messageService
        self._patientService = patientservice

        # ---settings---
        # dit zijn alle types van tasks de kunnen uitgevoerd worden: ze worden gelinkt aan een methode
        self._taskDict: dict[str, function] = {
            "send_message": self._sendMessage,
            "test_task": self._testTask,
            "get_logs": self._getLogs,
        }
        self._statuses = statuses

    def __del__():
        pass

    # 1 actie van de queueManager
    def process_task(self) -> str:
        # get the Task uit de queue
        firstQueueTask = None
        try:
            firstQueueTask = self._taskService.getNextQueueItem()
        except Exception as e:
            self._loggingService.error(
                f"er ging iets mis bij het opvragen van de task uit de queue: {traceback.format_exception(e)}"
            )
            return "error"

        # als er geen task is gevonden(alles is afgehandeld) ga in standby modus anders wordt de gevonden task afgehandeld
        if firstQueueTask == None:
            self._loggingService.info("geen task gevonden")
            return "standby"
        else:
            self._handleTask(firstQueueTask)
            return "active"

    def _updateStatus(self, status: str, message: str, task: Task):
        task.update_status([status, message])
        self._taskService.updateTask(task)

    # logged de status en de message en update de
    def _logStatus(self, status: str, loggingMessage: str, task: Task):
        message = loggingMessage
        self._updateStatus(status, message, task)
        self._loggingService.error(loggingMessage)

    # behandeld de doorgestuurde task
    def _handleTask(self, task: Task) -> None:
        self._loggingService.info(f"task wordt behandelt met id: {task.id}")
        task.start_process()
        self._taskService.updateTask(task)
        # get the function from taskdict that is linked to the task type name and execute it if it exists,
        functionToExecute = self._taskDict.get(task.task_type)
        statusToUpdate = None
        if functionToExecute == None or not callable(functionToExecute):
            self._logStatus(
                self._statuses["failed"],
                f"dit task type wordt niet ondersteund: {task.task_type}",
                task,
            )
        else:
            try:
                # execute the task based on task type
                statusToUpdate = functionToExecute(task.payload)
                self._updateStatus(
                    status=statusToUpdate[0],
                    message=statusToUpdate[1],
                    task=task,
                )
            except Exception as e:
                self._logStatus(
                    self._statuses["failed"],
                    f"{functionToExecute.__name__} failed, {e}",
                    task,
                )

    # taskdict methods, should all look the same
    def _sendMessage(self, payload: Any) -> list[str]:
        log = ""
        self._loggingService.info(f"executing send message task")
        # check wether payload is the correct type
        if not isinstance(payload, dict):
            errormessage = """
                foutieve payload: geef een juiste payload terug de payload voor send_message moet er zo uitzien: 		{
		        "hospital_id" : "7402241006",
		        "message" : "Graag je huisarts contacteren voor meer info"
		        "title" : "nip test informering"
		        "files" : [{
		        	"filename" : "nip_test.pdf",
		        	"data" : "<encoded file>"
		        	},
		        	{
		        	"filename" : "nip_test2.pdf",
		        	"data" : "<encoded file>"
		        	}]}"""
            self._loggingService.error(errormessage)
            return [
                self._statuses["failed"],
                errormessage,
            ]
        strictpayload: dict[str, Any] = payload

        # get the patient from the bewell api
        hospitalId = int(strictpayload["hospital_id"])
        self._loggingService.info(f"searching for patient met hospital_id: {hospitalId}")
        patient = self._patientService.getPatientHospitalId(
            hospitalId
        )  # get recipient patient

        # als er geen patient gevonden is geef een gepaste status en statuslog mee
        if patient == None:
            errormessage = "deze patient bestaat niet in de bewell omgeving"
            self._loggingService.error(errormessage)
            return [
                self._statuses["failed"],
                errormessage,
            ]
        # als er wel een patient gevonden is ga je verder
        else:
            message = f"patient gevonden met id: {patient.id} "
            self._loggingService.info(message)
            log = log + message

            # send message to the found patient
            # construct the content of the message
            message = strictpayload["message"]
            title = strictpayload["title"]
            content = Content(text=message, title=title)
            # construct the files of the message
            res = strictpayload.get("files")
            files: list[File] = []
            if res == None:
                pass
            else:
                filepayload: list[dict] = res
                for file in filepayload:
                    filename = file["filename"]
                    data = file["data"]
                    file = File(filename=filename, data=data)
                    files.append(file)
            newMessage = MessagePost(
                recipient_id=patient.id, content=content, files=files
            )
            response = self._messageService.PostNewMessage(newMessage)  # send the message
            message = f"bericht is verstuurd, id van verstuurde message: {response} "
            log = log + message
            self._loggingService.info(message)
            return [self._statuses["completed"], log]

    # een task om te testen of taskhandling werkt
    def _testTask(self, payload: list[dict[str, str]]) -> list[str]:
        self._loggingService.info(f"executing test task")
        time.sleep(2)
        return [self._statuses["completed"], "succesvol getest"]

    # todo: een gebruiker kan de logs van de api en van de middleware opvragen via een task
    def _getLogs(self, payload: list[dict[str, str]]) -> list[str]:
        raise NotImplementedError()
