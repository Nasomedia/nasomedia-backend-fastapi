from azure.storage.blob import BlobServiceClient, ContentSettings
from fastapi import UploadFile
from typing import List

from app.core.config import settings
from app import schemas

class DepsAzureBlob():
    def __init__(self):
        """
        Deps object for Auzre Blob API
        """

        self.content_type_png = ContentSettings(content_type='image/png')
        self.blob_service_client = BlobServiceClient.from_connection_string(settings.BLOB_CONNECT_STRING)
        self.blob_container_client = self.blob_service_client.get_container_client(settings.BLOB_CONTAINER_NAME)

    def upload_file(self, file: UploadFile, upload_url):
        self.blob_container_client.upload_blob(
            upload_url, file.file.read(), content_settings=self.content_type_png)

    def delete_file(self, blob):
        print(blob)
        self.blob_container_client.delete_blob(
            blob, 'include'
        )

blob = DepsAzureBlob()

