from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from GlobalSettings import *

@dataclass
class Log:
    level:str
    message:str
    timestamp:datetime=datetime.now()
    extra_info:str|None=None
    ID:int|None=None