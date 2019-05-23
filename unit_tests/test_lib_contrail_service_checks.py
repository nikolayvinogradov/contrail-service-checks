import unittest
from mock import patch

from lib_contrail_service_checks import CSCHelper, CSCCredentialsError

CRED_DICT_V3 = {
    'os-credentials': ('auth_url=http://localhost/v3, '
                       'username=admin, '
                       'password=password, '
                       'region_name=region, '
                       'credentials_project=project, '
                       'domain=somedomain'),
    'contrail_analytics_vip': '1.1.1.1',
}

CRED_DICT_V3_OUT = {
    'auth_version': 3,
    'username': 'admin',
    'password': 'password',
    'project_name': 'project',
    'user_domain_name': 'somedomain',
    'project_domain_name': 'somedomain',
    'contrail_analytics_vip': '1.1.1.1',
    'auth_url': 'http://localhost/v3',
    'region_name': 'region',
}

CRED_DICT_V3_NO_USERNAME = {
    'os-credentials': ('auth_url=http://localhost/v3, '
                       'password=password, '
                       'region_name=region, '
                       'credentials_project=project, '
                       'domain=somedomain'),
    'contrail_analytics_vip': '1.1.1.1',
}

CRED_DICT_V3_NO_DOMAIN = {
    'os-credentials': ('auth_url=http://localhost/v3, '
                       'username=admin, '
                       'password=password, '
                       'region_name=region, '
                       'credentials_project=project, '),
    'contrail_analytics_vip': '1.1.1.1',
}

CRED_DICT_LEGACY = {
    'os-credentials': ('auth_url=http://localhost/v2.0, '
                       'username=admin, '
                       'password=password, '
                       'region_name=region, '
                       'credentials_project=project, '),
    'contrail_analytics_vip': '1.1.1.1',
}

CRED_DICT_LEGACY_OUT = {
    'username': 'admin',
    'password': 'password',
    'contrail_analytics_vip': '1.1.1.1',
    'auth_url': 'http://localhost/v2.0',
    'region_name': 'region',
    'tenant_name': 'project',
}

CRED_DICT_NO_AUTH_URL = {
    'os-credentials': ('username=admin, '
                       'password=password, '
                       'region_name=region, '
                       'credentials_project=project, '),
    'contrail_analytics_vip': '1.1.1.1',
}


class CSCHelperTest(unittest.TestCase):

    @patch('lib_contrail_service_checks.hookenv.config')
    def test_get_os_credentials_no_auth_url(self, hookenv):
        hookenv.return_value = CRED_DICT_NO_AUTH_URL
        self.assertRaises(CSCCredentialsError, CSCHelper().get_os_credentials)

    @patch('lib_contrail_service_checks.hookenv.config')
    def test_get_os_credentials_v3(self, hookenv):
        hookenv.return_value = CRED_DICT_V3
        creds = CSCHelper().get_os_credentials()
        self.assertDictEqual(CRED_DICT_V3_OUT, creds)

    @patch('lib_contrail_service_checks.hookenv.config')
    def test_get_os_credentials_v3_no_domain(self, hookenv):
        hookenv.return_value = CRED_DICT_V3_NO_DOMAIN

        self.assertRaises(CSCCredentialsError, CSCHelper().get_os_credentials)

    @patch('lib_contrail_service_checks.hookenv.config')
    def test_get_os_credentials_legacy(self, hookenv):
        hookenv.return_value = CRED_DICT_LEGACY

        CSCHelper().get_os_credentials()

    @patch('lib_contrail_service_checks.hookenv.config')
    def test_get_os_credentials_attr_missing(self, hookenv):

        for k in CSCHelper.common_attrs():
            d = CRED_DICT_V3.copy()
            d['os-credentials'] = d['os-credentials'].replace(k, k + 'abc')
            hookenv.return_value = d
            i = CSCHelper()
            self.assertRaisesRegex(CSCCredentialsError, "^{}$".format(k),
                                   i.get_os_credentials)

    @patch('lib_contrail_service_checks.hookenv.config')
    def test_get_os_credentials_final_dict(self, hookenv):
        hookenv.return_value = CRED_DICT_LEGACY
        creds = CSCHelper().get_os_credentials()
        self.assertDictEqual(CRED_DICT_LEGACY_OUT, creds)
