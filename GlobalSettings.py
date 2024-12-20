import json
import os
from pathlib import Path

statuses: dict[str, str] = {
    "in_queue": "in_queue",
    "processing": "processing",
    "completed": "completed",
    "failed": "failed",
}
# program delay in seconds
maindelay = 1
standbyDelay = 3

# config files
_config_path = os.path.join(os.path.dirname(__file__), "secrets.json")
_secretPath = _config_path
with open(_config_path, "r") as f:
    _config = json.load(f)
api_login_data = _config["api"]
quedb_settings = _config["queue_db"]

#api adress
apiurl = "https://mijntest.azstlucas.be/api/v2/"

# logging
## loglevels 0) nothing, 10) critical+, 20) error+, 30) warning+, 40)info+, 50)debug+
loglevel=50
sqlserverLogLevel=30

# filepaths
## config

Path.mkdir(Path("logs"),exist_ok=True,parents=True)
## logging
InfoLogFilePath=Path.absolute(Path("logs/info.log"))
warningLogFilePath=Path.absolute(Path("logs/warning.log"))

