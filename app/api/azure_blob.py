from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.storage.blob._models import BlobProperties
from fastapi import UploadFile
from typing import List, Union

from app.core.config import settings
from app import schemas


class DepsAzureBlob():
    def __init__(self):
        """
        Deps object for Auzre Blob API
        """

        self.blob_service_client = BlobServiceClient.from_connection_string(
            settings.BLOB_CONNECT_STRING)
        self.blob_container_client = self.blob_service_client.get_container_client(
            settings.BLOB_CONTAINER_NAME)

    def upload_file(self, file_in: UploadFile, upload_url: str):
        self.blob_container_client.upload_blob(
            upload_url, file_in.file.read(), content_settings=ContentSettings(content_type=file_in.content_type))

    def delete_file(self, blob: Union[str, BlobProperties]):
        self.blob_container_client.delete_blob(
            blob, 'include'
        )


blob = DepsAzureBlob()
