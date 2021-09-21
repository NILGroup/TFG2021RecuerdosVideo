from google.cloud import storage
from google.cloud.exceptions import NotFound
import logging
from constants.messages import messages
from resources import bucket_name


def delete_blob(blob_name):
    
    # Deletes a blob from the bucket
    storage_client = storage.Client()
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        logging.info(messages.INFO_BLOB_DELETED.value + blob_name)
    except NotFound:
        logging.info(messages.INFO_BLOB_NOT_FOUND.value + blob_name)


def upload_blob(source_file_name, destination_name):
    # Uploads a file to the bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(source_file_name)
    
    print(
       logging.info(str(messages.INFO_FILE_UPLOADED_BUCKET.value).format(
            source_file_name, bucket_name, destination_name))
    )
    return 'gs://' + bucket_name + '/' + destination_name
