import functions_framework
import requests
import pickle
import json
from google.cloud import storage


@functions_framework.http
def update_image_request_history(request):
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

    #------------

    # Google Template Code + Extra. CORS is required for more complex HTTP/S REQUESTS
    # Set CORS headers for the preflight request
    # https://cloud.google.com/functions/docs/writing/write-http-functions#functions-http-cors-python
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        HEADERS = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, HEADERS)

    # Set CORS headers for the main request
    HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    # Attempt to (1) retrieve image from URL as bytes and upload into google cloud storage to and (2) send image file name and API response to another backend server for additional processing.
    # Note: did not realize python class object is not serializable like JS/TS. Use Dictionary objects instead. There are other conversion options too.
    try:
        # Obtain the Image Request History object from the request body
        print('Flag-1: Extract the imageUrl and visionApiResults properties from request body')
        if request_json and ('imageUrl' in request_json and request_json['imageUrl'] != "") and ('visionApiResults' in request_json):
            image_request_history_dict = request_json

        else:
            # Client Request Error Handling
            error_message = "None"

            if (request_json is None):
                error_message = "Bad Request. No data provided in the Request Body."
                
            elif (request_json) and ('imageUrl' not in request_json or 'visionApiResults' not in request_json):
                error_message = "Bad Request. Request Body (image request history data) is missing some required properties."

            elif (request_json) and ('imageUrl' in request_json) and (not request_json['imageUrl'] or request_json['imageUrl'] == ""):
                error_message = "Bad Request. Request Body (image request history data) is missing the image url." 

            elif (request_json) and ('visionApiResults' in request_json) and (not request_json['visionApiResults']):
                error_message = "Bad Request. Request Body (image request history data) is missing the vision api results."

            error_response = CustomResponse(error_message, error_message, 400)
            return (json.dumps(error_response.to_dict()), 400, HEADERS)
        
        # Obtain the Image Request History Collection as Python List Object
        print('Flag-2: Obtain the Image Request History Collection as Python List Object')
        image_request_history_list = get_image_request_history_collection()
  
        # Append the Image Request History dictionary object to the Image Request History list
        print('Flag-3a: Append the Image Request dictionary object to the Image Request History list')
        append_history_list(image_request_history_dict, image_request_history_list)

        # Convert the python list object back into a JSON string (serialize it)
        print('Flag-3b: Convert the python list object back into a JSON string (serialize it)')
        image_request_history_list_json = convert_data_to_json(image_request_history_list)

        # Overwrite the existing json file in the project GCS bucket with the latest json string
        print('Flag-4: Overwrite the existing json file in the project GCS bucket with the latest json string')
        upload_blob_from_memory(image_request_history_list_json)

        ok_response = CustomResponse(f"The latest image request history data has been appended to the json file!", "None", 200)
        return (json.dumps(ok_response.to_dict()), 200, HEADERS)

    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        error_response = {"message": "An error occurred", "error": str(e), "status": 500}
        return (json.dumps(error_response), 500, HEADERS)

    #------------

def get_image_request_history_collection():
    GET_IMAGE_REQUEST_HISTORY_COLLECTION_URL = #ADD URL OF CLOUD RUN FUNCTION HERE
    response = requests.get(GET_IMAGE_REQUEST_HISTORY_COLLECTION_URL)

    if response:
        py_object = response.json() # should load/outputs as a list of dictionary objects 
        print(json.dumps(py_object)) # converts to string JSON and prints it
        return py_object
    else:
        return [] # if there is no response, return an empty array. Which would allow us to build a new json collection.


def append_history_list(image_request_history_dict, image_request_history_list):
    print(f"image request history list length, before appending dict: {len(image_request_history_list)}")
    image_request_history_list.append(image_request_history_dict)
    print(f"image request history list length, after appending dict: {len(image_request_history_list)}")

    return image_request_history_list


def convert_data_to_json(image_request_history_list):
    return json.dumps(image_request_history_list)


def upload_blob_from_memory(contents):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    STORAGE_BUCKET_NAME = #REPLACE WITH YOUR GCS BUCKET NAME

    # The contents to upload to the file
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name" 
    FILE_OBJECT_NAME = "image-collection.json"

    storage_client = storage.Client()
    bucket = storage_client.bucket(STORAGE_BUCKET_NAME)
    blob = bucket.blob(FILE_OBJECT_NAME)

    blob.upload_from_string(contents) #can be string or bytes. If a file exist, it wil be overwritten. If it does not exist, it will be created.

    print(
        f"{FILE_OBJECT_NAME} with contents {contents} uploaded to {STORAGE_BUCKET_NAME}."
    )


class CustomResponse:
    def __init__(self, message="", error="none", status=200):
        self.message = message
        self.error = error
        self.status = status

    def __str__(self):
        return f"{self.message}, {self.error}, {self.status}"

    # Used to convert and make Class Object serializable.
    def to_dict(self):
        return {
            "message": self.message,
            "error": self.error,
            "status": self.status
        }