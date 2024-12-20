import requests
from .Model.PatientGet import PatientGet
from requests.auth import HTTPBasicAuth
from functools import cache, lru_cache
from .Settings import *


class PatientController:
    def __init__(self):
        # de basis url voor alle calls die met patienten te maken hebben
        self.apiurl: str = apiurl + "patients"
        self.basicauth: HTTPBasicAuth = basicauth
        # cache voor caching, wordt opgeruimd als de klasse wordt opgeruimd
        self.cache = {}
        self.getPatienten(parameters="")

    # todo: geef een patient op basis van een meegegeven hospital_id
    def getPatientHospitalId(self, hospital_id: int) -> PatientGet | None:
        response = self.getPatienten(f"?hospital_id={hospital_id}")
        if response.__len__() > 1:
            raise TooManyResultsDBException(
                "er zijn meerdere patienten met dit hospital_id"
            )
        elif response.__len__() <= 0:
            return None
        else:
            return response[0]

    # geef een specifieke patient op basis van zijn id in de bewell api
    def getPatient(self, id) -> PatientGet:
        if id in self.cache:
            return self.cache[id]
        else:
            parameters = f"/{id}"
            url = f"{self.apiurl}{parameters}"
            headers = {"Accept": "application/json"}

            response = requests.get(url, auth=self.basicauth, headers=headers)
            patient: PatientGet = PatientGet.from_dict(response.json())
            self.cache[id] = patient
            return patient

    # geef een lijst van patienten op basis van een aantal parameters bvb ?hospital_id=101 , zie bewell documentatie. geef een lege string voor alle patienten
    def getPatienten(self, parameters: str) -> list[PatientGet]:
        returnType = PatientGet
        url = f"{str(self.apiurl)}{str(parameters)}"
        # print("-requesting: ", url)
        headers = {"Accept": "application/json"}
        response = requests.get(url, auth=self.basicauth, headers=headers)
        # print("-responseStatus: ", response.status_code)
        if response.status_code == 200:
            responseDict = response.json()
            patients = []
            for patient in responseDict:
                patients.append(returnType.from_dict(patient))
            return patients
        else:
            raise ConnectionError(
                f"could not get patienten from request:{url} {response.reason}"
            )
            return []


# errors
class TooManyResultsDBException(Exception):
    # raised when the database returns too many results
    def __init__(self, message: str) -> None:
        self.description = "raised when the database returns too many results"
        self.message = message
        super().__init__(message)