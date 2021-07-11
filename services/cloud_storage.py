from google.cloud import storage
from google.cloud.exceptions import NotFound

from resources import bucket_name, project_id
import os

def delete_blob(blob_name):
    """Deletes a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # blob_name = "your-object-name"

    storage_client = storage.Client()
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    except NotFound:
        print("Error: Blob {} not found.". format(blob_name))





def upload_blob(source_file_name, destination_name):
    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The path to your file to upload
    # source_file_name = "local/path/to/file"
    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to bucket {} as {}.".format(
            source_file_name, bucket_name, destination_name)
    )
    return 'gs://' + bucket_name + '/' + destination_name