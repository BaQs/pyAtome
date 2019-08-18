import json
import simplejson
# import pickle
# from dateutil.relativedelta import relativedelta
import requests
from fake_useragent import UserAgent


# ATOME_COOKIE = "atome_cookies.pickle"
# ATOME_USER_ID = "atome_user_id.pickle"
# ATOME_USER_REFERENCE = "atome_user_reference.pickle"


COOKIE_NAME = "PHPSESSID"
API_BASE_URI = "https://esoftlink.esoftthings.com"
API_ENDPOINT_LOGIN = "/api/user/login.json"
API_ENDPOINT_LIVE = "/measure/live.json"
LOGIN_URL = API_BASE_URI + API_ENDPOINT_LOGIN

DEFAULT_TIMEOUT = 10

# LOGIN_URL = "https://espace-client-connexion.enedis.fr/auth/UI/Login"
# HOST = "https://espace-client-particuliers.enedis.fr/group/espace-particuliers"
# DATA_URL = "{}/suivi-de-consommation".format(HOST)

# REQ_PART = "lincspartdisplaycdc_WAR_lincspartcdcportlet"

# HOURLY = "hourly"
# DAILY = "daily"
# MONTHLY = "monthly"
# YEARLY = "yearly"


# _DELTA = 'delta'
# _FORMAT = 'format'
# _RESSOURCE = 'ressource'
# _DURATION = 'duration'
# _MAP = {
#     _DELTA: {HOURLY: 'hours', DAILY: 'days', MONTHLY: 'months', YEARLY: 'years'},
#     _FORMAT: {HOURLY: "%H:%M", DAILY: "%d %b", MONTHLY: "%b", YEARLY: "%Y"},
#     _RESSOURCE: {HOURLY: 'urlCdcHeure', DAILY: 'urlCdcJour', MONTHLY: 'urlCdcMois', YEARLY: 'urlCdcAn'},
#     _DURATION: {HOURLY: 24, DAILY: 30, MONTHLY: 12, YEARLY: None}
# }


class PyAtomeError(Exception):
    pass


class AtomeClient(object):
    def __init__(self, username, password, session=None, timeout=None):
        """Initialize the client object."""
        self.username = username
        self.password = password
        self._user_id = None
        self._user_reference = None
        self._session = session
        self._data = {}
        self._timeout = timeout

    def login(self):
        """Set http session."""
        if self._session is None:
            self._session = requests.session()
            # adding fake user-agent header
            self._session.headers.update({'User-agent': str(UserAgent().random)})
        return self._login()

    def _login(self):
        """Login to Atome's API."""
        payload = {"email": self.username, "plainPassword": self.password}

        try:
            req = self._session.post(LOGIN_URL,
                               json=payload,
                               headers={"content-type": "application/json"},
                               timeout=self._timeout)
        except OSError:
            raise PyAtomeError("Can not login to API")
        if "PHPSESSID" not in self._session.cookies:
            raise PyAtomeError("Login error: Please check your username/password." + str(self._session.cookies))
        response_json = req.json()

        user_id = str(response_json["id"])
        user_reference = response_json["subscriptions"][0]["reference"]

        self._user_id = user_id
        self._user_reference = user_reference

        return True

    def _get_live(self):
        """Get data."""

        live_url = (
            API_BASE_URI
            + "/api/subscription/"
            + self._user_id
            + "/"
            + self._user_reference
            + API_ENDPOINT_LIVE
        )
        try:
            req = self._session.get(live_url,
                                    timeout=self._timeout)

        except OSError as e:
            raise PyAtomeError("Could not access Atome's API: " + str(e))

        if req.text is "":
            raise PyAtomeError("No data")

        try:
            json_output = req.json()
        except (OSError, json.decoder.JSONDecodeError, simplejson.errors.JSONDecodeError) as e:
            raise PyAtomeError("Impossible to decode response: " + str(e) + "\nResponse was: " + str(req.text))

        return json_output
        

    def get_live(self):
        """Get current data."""
        # return {"live": self._get_live}
        return self._get_live()

    def close_session(self):
        """Close current session."""
        self._session.close()
        self._session = None

