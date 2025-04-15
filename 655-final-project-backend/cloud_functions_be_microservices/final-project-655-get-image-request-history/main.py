import functions_framework
import json

from google.cloud import storage

@functions_framework.http
def get_image_request_history(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    # The ID of your GCS bucket
    BUCKET_NAME = #REPLACE WITH YOUR GCS BUCKET NAME

    # The ID of your GCS object
    FILE_OBJECT_NAME = "image-collection.json" #REPLACE WITH YOUR FILE NAME (IF CHANGED)

    print('flag-1')
    json_byte_data = download_json_blob_into_memory(BUCKET_NAME, FILE_OBJECT_NAME)
    print('flag-2')
    json_str = convert_byte_to_string(json_byte_data)
    print('flag-3')
    py_object = convert_json_str_to_object(json_str)
    print('flag-4')
    return py_object

def download_json_blob_into_memory(bucket_name, blob_name):
    """Downloads a blob into memory."""
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(blob_name)
    contents = blob.download_as_bytes()

    print(
        "Downloaded storage object {} from bucket {} as the following bytes object: {}.".format(
            blob_name, bucket_name, contents.decode("utf-8")
        )
    )

    return contents

def convert_byte_to_string(byte_data):
    """Converts byte data into (json) string"""
    return byte_data.decode('utf8')
    
def convert_json_str_to_object(json_str):
    """Converts json string into an object"""
    py_object = json.loads(json_str)
    print(json.dumps(py_object))
    print(py_object)
    return py_object