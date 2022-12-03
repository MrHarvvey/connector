"""
Retrieve secrets from Manager
"""

import os

from google.cloud.secretmanager import SecretManagerServiceClient


def get(name):
    project = os.environ.get('GOOGLE_CLOUD_PROJECT')
    is_gae = os.environ.get('GAE_APPLICATION')
    if is_gae:
        client = SecretManagerServiceClient()
        secret_path = f'projects/{project}/secrets/{name}/versions/latest'

        res = client.access_secret_version(request={'name': secret_path})
        return res.payload.data.decode('utf-8')
    return os.environ.get(name)
