import unittest
import requests_mock
import responses
import logging
import json
import os
import sys

# Our test case class
import requests
from pyatome import AtomeClient
from pyatome.client import LOGIN_URL, API_BASE_URI, API_ENDPOINT_LIVE

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

class PyAtomeError(Exception):
    pass


class AtomeClientTestCase(unittest.TestCase):

    def test_AtomeClient(self):
        username = "test_login"
        password = "test_password"
        client = AtomeClient(username, password)
        assert client.username == username
        assert client.password == password
        assert client._timeout is None

    def test_AtomeClientWithTimeout(self):
        username = "test_login"
        password = "test_password"

        client = AtomeClient(username, password, timeout=1)
        assert client.username == username
        assert client.password == password
        assert client._timeout == 1

    def test_AtomeClientWithSession(self):
        username = "test_login"
        password = "test_password"
        session = requests.session()

        client = AtomeClient(username, password, session=session)
        assert client.username == username
        assert client.password == password
        assert client._session == session

    @requests_mock.Mocker()
    def test_login(self, m):
        cookies = {'PHPSESSID': 'TEST'}
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'login.json'), 'r') as f:
            answer = json.load(f)

        m.post(LOGIN_URL, status_code=200, cookies=cookies, text=json.dumps(answer))
        client = AtomeClient("test_login", "test_password")
        client.login()
        
        logging.debug(client)
        
        assert client._user_id          == '12345'
        assert client._user_reference   == '101234567'

        return client


    @requests_mock.Mocker()
    def test_get_live(self, m):

        client = self.test_login()

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'live.json'), 'r') as f:
            answer = json.load(f)

        live_url = (
            API_BASE_URI
            + "/api/subscription/"
            + client._user_id
            + "/"
            + client._user_reference
            + API_ENDPOINT_LIVE
            )

        m.get(live_url, status_code=200, text=json.dumps(answer))
        liveData = client.get_live()
        logging.debug(liveData)
        assert liveData['last'] == 2289

    def test(self):
        data = None
        if not data:
            assert True
        else:
            assert False


if __name__ == "__main__":
    unittest.main()