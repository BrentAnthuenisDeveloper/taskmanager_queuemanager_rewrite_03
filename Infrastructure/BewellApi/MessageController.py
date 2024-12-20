import requests
from .Model.MessagePost import MessagePost
from .Model.MessageGet import MessageGet
from pprint import pprint
from datetime import timedelta, datetime
import json
from dataclasses import asdict
from functools import reduce, lru_cache
from .Settings import *


class MessageController:
    def __init__(self):
        # de basis url voor alle calls die met messages te maken hebben
        self.apiurl = apiurl + "messages?"
        self.basicauth = basicauth
        self.getMostRecentMessage()

    # geeft het meest recent aangemaakte bericht
    def getMostRecentMessage(self) -> MessageGet | None:
        returnType = MessageGet
        today = datetime.today() - timedelta(days=1)
        url = f"{self.apiurl}created_from={datetime.timestamp(today)}"
        # print("-requesting: ", url)
        headers = {"Accept": "application/json"}
        response = requests.get(url, auth=self.basicauth, headers=headers, verify=True)
        # print("responseStatus:", response.status_code)
        if response.status_code == 200:
            responseList = response.json()
            mostRecentMessage: MessageGet = returnType.from_dict(
                dict(
                    reduce(
                        lambda accum, new: accum
                        if accum.get("created_timestamp") > new.get("created_timestamp")
                        else new,
                        responseList,
                    )
                )
            )
            # print("recentste patient", mostRecentMessage)
            return mostRecentMessage
        else:
            # print(response.status_code)
            response.raise_for_status()
            return None

    # maakt een nieuw bericht in de bewell api op basis van de parameter message:MessagePost
    def PostNewMessage(self, Message: MessagePost) -> str | None:
        url = self.apiurl
        headers = {"Content-Type": "application/json;charset=utf-8"}
        messageJson = json.dumps(asdict(Message))
        # api call
        response = requests.post(
            url,
            auth=self.basicauth,
            headers=headers,
            data=messageJson,
        )

        if response.ok:
            return response.json().get("message_id")
        else:
            response.raise_for_status()
