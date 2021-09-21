from google.cloud import storage
from google.cloud.exceptions import NotFound

from resources import bucket_name


def delete_blob(blob_name):
    
    # Deletes a blob from the bucket
    storage_client = storage.Client()
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        print("Blob {} deleted.".format(blob_name))
    except NotFound:
        print("Error: Blob {} not found.".format(blob_name))


def upload_blob(source_file_name, destination_name):
    # Uploads a file to the bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_name)
    blob.upload_from_filename(source_file_name)
    
    print(
        "File {} uploaded to bucket {} as {}.".format(
            source_file_name, bucket_name, destination_name)
    )
    return 'gs://' + bucket_name + '/' + destination_name
