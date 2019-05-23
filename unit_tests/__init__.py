import sys
import mock

# Mock out charmhelpers so that we can test without it.
import charms_openstack.test_mocks  # noqa
charms_openstack.test_mocks.mock_charmhelpers()

sys.path.append('lib')
sys.path.append('reactive')
sys.path.append('files/plugins')

charmsupport = mock.Mock()

sys.modules['charmhelpers.contrib.charmsupport'] = charmsupport
sys.modules['charmhelpers.contrib.charmsupport.nrpe'] = charmsupport.nrpe