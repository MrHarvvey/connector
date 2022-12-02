""""
Tests for getting secrets
"""

from unittest.mock import (
    patch,
    Mock,
)

from django.test import SimpleTestCase

from app.app import secrets

MOCK_GCP_PROJECT = 'test-project'


@patch.dict(
    'os.environ', {
        'GOOGLE_CLOUD_PROJECT': MOCK_GCP_PROJECT,
        'GAE_APPLICATION': 'yes'
    }
)
@patch('app.secrets.SecretManagerServiceClient')
class TestSecretManagerTests(SimpleTestCase):
    """
    Test getting secrets
    """

    def test_retrieve_secret(self, mock_sm):
        mock_client = Mock()
        mock_sm.return_value = mock_client
        mock_version_res = Mock()
        secret = 'sample'
        secrets_bytes = bytes(secret, 'utf-8')
        mock_version_res.payload.data = secrets_bytes
        mock_client.access_secret_version.return_value = mock_version_res

        name = 'SampleBouncer'
        ret = secrets.get(name)

        exp_path = (
            f'projects/{MOCK_GCP_PROJECT}/secrets'
            f'/{name}/version/latest'
        )
        mock_client.access_secret_version.assert_called_once_with(
            request={
                'name': exp_path
            }
        )

        self.assertEqual(ret, secret)


class TestLocalDevModelTests(SimpleTestCase):
    @patch('app.secrets.SecretManagerServiceClient')
    def test_retrieve_from_env(self, mock_sm):
        secret = 'SampleSecret'
        name = 'secretname'
        with patch.dict('os.environ', {name: secret}):
            val = secrets.get(name)

        self.assertEqual(val)
        mock_sm.assert_not_called()
