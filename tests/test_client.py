import unittest
import requests_mock
# import responses

# Our test case class
import requests
from pyatome import AtomeClient
from pyatome.client import LOGIN_URL


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

    # @requests_mock.Mocker()
    # def test_login(self, m):
    #     cookies = {'PHPSESSID': 'test'}

    #     m.register_uri('POST', LOGIN_URL, status_code=200, cookies=cookies)
    #     client = AtomeClient("test_login", "test_password")
    #     client.login()

    def test(self):
        data = None
        if not data:
            assert True
        else:
            assert False


if __name__ == "__main__":
    unittest.main()