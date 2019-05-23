import unittest
import mock
from io import StringIO
from check_contrail_alarms import check_contrail_alarms, NAGIOS_OK, \
    NAGIOS_CRITICAL


class fake_response():

    def __init__(self, resp={}):
        self.resp = resp

    def json(self):
        return self.resp


class MyTest(unittest.TestCase):

    @mock.patch('requests.get')
    def test_check_contrail_alarms_check_auth_header(self, requests_get):
        def check_header(**kwargs):
            x_auth_token = kwargs.get('headers', {}).get('X-Auth-Token')
            self.assertEqual(x_auth_token, 'token')
            return fake_response()

        requests_get.side_effect = check_header
        check_contrail_alarms('1.1.1.1', 'token')

    @mock.patch('sys.stdout', new_callable=StringIO)
    @mock.patch('requests.get')
    def test_check_contrail_alarms_nagios_ok(self, requests_get, stdout):
        requests_get.return_value = fake_response()
        code = check_contrail_alarms('1.1.1.1', 'token')
        self.assertEqual(code, NAGIOS_OK)
        self.assertEqual(stdout.getvalue(), "{}\n")

    @mock.patch('requests.get')
    def test_check_contrail_alarms_nagios_critical(self, requests_get):
        requests_get.return_value = fake_response(resp={'not_good': True})
        code = check_contrail_alarms('1.1.1.1', 'token')
        self.assertEqual(code, NAGIOS_CRITICAL)
