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
from pyatome.client import LOGIN_URL, API_BASE_URI, API_ENDPOINT_LIVE, API_ENDPOINT_CONSUMPTION

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
        with open(os.path.join(__location__, 'data/login.json'), 'r') as f:
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
        with open(os.path.join(__location__, 'data/live.json'), 'r') as f:
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

    @requests_mock.Mocker()
    def test_relog_after_session_down(self, m):
        # we login
        client = self.test_login()
        # # then we erase the session
        #     # client._session.cookies = None
        # # so that we can ask for data and see if it logs back
        # __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        # with open(os.path.join(__location__, 'live.json'), 'r') as f:
        #     live_answer = json.load(f)

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'data/login.json'), 'r') as f:
            login_answer = json.load(f)

        live_url = (
            API_BASE_URI
            + "/api/subscription/"
            + client._user_id
            + "/"
            + client._user_reference
            + API_ENDPOINT_LIVE
            )

        m.post(LOGIN_URL, status_code=200, cookies={'PHPSESSID': 'TEST'}, text=json.dumps(login_answer))
        m.get(live_url, text="Wrong session", status_code=403)

        # shall generate an exception
        with self.assertRaises(Exception): client.get_live()

    @requests_mock.Mocker()
    def test_consumption(self, m):

        client = self.test_login()

        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with open(os.path.join(__location__, 'data/consumption_sod.json'), 'r') as f:
            consumption_sod = json.load(f)
        with open(os.path.join(__location__, 'data/consumption_sow.json'), 'r') as f:
            consumption_sow = json.load(f)
        with open(os.path.join(__location__, 'data/consumption_som.json'), 'r') as f:
            consumption_som = json.load(f)
        with open(os.path.join(__location__, 'data/consumption_soy.json'), 'r') as f:
            consumption_soy = json.load(f)

        period_url = (
            API_BASE_URI
            + "/api/subscription/"
            + client._user_id
            + "/"
            + client._user_reference
            + API_ENDPOINT_CONSUMPTION
            + '?period='
            )

        m.get(period_url + 'sod', status_code=200, text=json.dumps(consumption_sod))
        liveData = client.get_consumption(period='day')
        assert liveData['total'] == 10

        m.get(period_url + 'sow', status_code=200, text=json.dumps(consumption_sow))
        liveData = client.get_consumption(period='week')
        assert liveData['total'] == 70
        
        m.get(period_url + 'som', status_code=200, text=json.dumps(consumption_som))
        liveData = client.get_consumption(period='month')
        assert liveData['total'] == 300
        
        m.get(period_url + 'soy', status_code=200, text=json.dumps(consumption_soy))
        liveData = client.get_consumption(period='year')
        assert liveData['total'] == 3650

    # TODO: test get_consumption with proper period, or with unproper period



    def test(self):
        data = None
        if not data:
            assert True
        else:
            assert False


if __name__ == "__main__":
    unittest.main()