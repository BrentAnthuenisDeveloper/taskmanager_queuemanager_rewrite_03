from requests.auth import HTTPBasicAuth
from GlobalSettings import api_login_data,apiurl


apiurl = apiurl
_config = api_login_data
_user = _config["username"].__str__()
_psswd = _config["password"].__str__()
basicauth: HTTPBasicAuth = HTTPBasicAuth(_user, _psswd)
