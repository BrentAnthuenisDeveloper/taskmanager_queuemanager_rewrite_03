from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from GlobalSettings import *


@dataclass
class TaskType:
    task_type: str
    description: Optional[str] = None
    api_endpoint: Optional[str] = None


@dataclass
class Task:
    task_type: str
    payload: Any
    status: str
    statuslog: str = ""
    retries: int = 0
    priority: int = 0
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    _logTeller: int = 0
    processed_at: datetime = None
    id: Optional[int] = 0

    def update_status(self, new_status: list[str]):
        if new_status is None:
            raise ValueError("new_status cannot be None")
        self.status = new_status[0]
        self.statuslog = self.statuslog + f"{self._logTeller}: {new_status[1]} "
        self._logTeller = self._logTeller + 1
        self.updated_at = datetime.now()

    def start_process(self):
        self.processed_at = datetime.now()
        self.update_status([statuses["processing"], f"attempt {self.retries}"])
        self.retries = self.retries + 1
