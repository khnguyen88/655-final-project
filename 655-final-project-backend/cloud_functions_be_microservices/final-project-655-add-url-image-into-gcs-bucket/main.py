import functions_framework
from google.cloud import storage
from PIL import Image
from urllib.request import urlopen
import os
import base64
import json
import requests
import io

@functions_framework.http
def add_url_image_into_gcs_bucket(request):
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
        # Obtain the 'image_url' and 'vision_api_results' property from the request body
        print('Flag-1: Extract the image_url and vision_api_results properties from request body')
        if request_json and ('image_url' in request_json and request_json['image_url'] != "") and ('vision_api_results' in request_json):
            image_url = request_json['image_url']
            vision_api_results = request_json['vision_api_results']

        else:
            # Client Request Error Handling
            error_message = "None"

            if (request_json is None):
                error_message = "Bad Request. No Data Provided in the Request Body."
                
            elif (request_json) and ('image_url' not in request_json or 'vision_api_results' not in request_json):
                error_message = "Bad Request. Request Body is missing some required properties."

            elif (request_json) and ('image_url' in request_json) and (not request_json['image_url'] or request_json['image_url'] == ""):
                error_message = "Bad Request. Request Body is missing the image url." 

            elif (request_json) and ('vision_api_results' in request_json) and (not request_json['vision_api_results']):
                error_message = "Bad Request. Request Body is missing the vision api results."

            error_response = CustomResponse(error_message, error_message, 400)
            return (json.dumps(error_response.to_dict()), 400, HEADERS)

        print(vision_api_results)
        
        # Extract File Name from Image URL
        print('Flag-2a: Extract File Name from Image URL')
        image_filename = extract_filename_from_image_url(image_url)

        # Extract File Extension from Image URL
        print('Flag-2b: Extract File Extension from Image URL')
        image_file_ext = extract_file_ext_from_image_url(image_url)

        # Format file extension to Pillow library accepted format
        print('Flag-2c: Format file extension to Pillow library accepted format')
        pillow_image_ext = format_file_ext_for_pillow(image_file_ext)

        if not pillow_image_ext:
            error_message = "Bad Request. The image is not an accepted file format"
            error_response = CustomResponse(error_message, error_message, 400)
            return (json.dumps(error_response.to_dict()), 400, HEADERS)

        # Convert image from URL into byte data object using urllib and pillow libraries
        print('Flag-3: Convert image from URL into byte data object')
        image_bytes_content = extract_image_from_url_to_bytes(image_url, pillow_image_ext)

        # Call Google Cloud Storage to insert a file
        print('Flag-4: Call Google Cloud Storage to insert a file!')
        upload_blob_from_memory(image_bytes_content, image_filename)

        # Build Google Storage Bucket URL from for image given filename
        print('Flag-5: Build Google Storage Bucket URL from given filename')
        gcs_image_url = build_google_storage_bucket_url(image_filename)

        # Build request payload data to send to the next backend server(less) function for further processing'
        print('Flag-6: Build request payload data to send to the next backend server(less) function')
        image_request_history_data = build_image_request_history_data(gcs_image_url, vision_api_results)

        # Request a serverless function to update image filename and api re
        print('Flag-7: Add contents of image url to storage bucket')
        put_image_url_content_to_storage_bucket(image_request_history_data)

        ok_response = CustomResponse(f"The image from the url has been successfully inserted into the project's Google Storage Bucket. URL: {image_url}", "None", 200)
        return (json.dumps(ok_response.to_dict()), 200, HEADERS)

    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        error_response = {"message": "An error occurred", "error": str(e), "status": 500}
        return (json.dumps(error_response), 500, HEADERS)


# Template code from google + Extra
# https://cloud.google.com/storage/docs/uploading-objects-from-memory
def upload_blob_from_memory(contents, destination_blob_name):
    """Uploads a file to the bucket."""

    # The ID of your GCS bucket
    PROJECT_BUCKET_NAME = #REPLACE WITH YOUR GCS BUCKET NAME

    # The contents to upload to the file, needs to be in bytes
    # contents = "these are my contents"

    # The ID of your GCS object
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(PROJECT_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(contents) #Note, tested. Works. Also adding the save file, just overrides the existing one! YAY!

    print(f"{destination_blob_name} with contents {contents} uploaded to {PROJECT_BUCKET_NAME}.")


def extract_filename_from_image_url(image_url):
    last_path_occurrence_index = image_url.rfind('/')
    start_of_filename_index = last_path_occurrence_index + 1;

    image_filename = image_url[start_of_filename_index:]
    print(image_filename)

    return image_filename


def extract_file_ext_from_image_url(image_url):
    ext_occurrence_index = image_url.rfind('.')
    start_of_file_ext_index = ext_occurrence_index + 1;

    image_file_ext = image_url[start_of_file_ext_index:]
    print(image_file_ext)

    return image_file_ext

def format_file_ext_for_pillow(image_file_ext):
    ACCEPTED_PILLOW_IMAGE_EXTENSION = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "tif": "TIFF",
        "tiff": "TIFF",
        "gif": "GIF"
    }

    pillow_image_ext = None

    if(image_file_ext.lower() in ACCEPTED_PILLOW_IMAGE_EXTENSION):
        pillow_image_ext = ACCEPTED_PILLOW_IMAGE_EXTENSION[image_file_ext.lower()]

    return pillow_image_ext

def extract_image_from_url_to_bytes(image_url, pillow_image_ext):
    img = Image.open(urlopen(image_url))
    rawBytes = io.BytesIO()
    img.save(rawBytes, pillow_image_ext) #arg1 = bytes, #arg2 = image file extension, i.e. jpg, png
    rawBytes.seek(0)
    content = rawBytes.read()
    print(content)

    return content 


def build_google_storage_bucket_url(image_filename):
    # The ID of your GCS bucket
    GCS_DOMAIN = "https://storage.googleapis.com"
    PROJECT_BUCKET_NAME = #REPLACE WITH YOUR GCS BUCKET NAME
    return f"{GCS_DOMAIN}/{PROJECT_BUCKET_NAME}/{image_filename}"


def build_image_request_history_data(gcs_image_url, vision_api_results):
    image_request_history_obj = ImageRequestHistory(gcs_image_url, vision_api_results)
    image_request_history_dict = image_request_history_obj.to_dict()
    print(image_request_history_dict)

    return image_request_history_dict


def put_image_url_content_to_storage_bucket(image_request_history_data):

    UPDATE_IMAGE_REQUEST_HISTORY_URL = #ADD URL OF CLOUD RUN FUNCTION HERE

    HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    request_body = image_request_history_data

    request_data = json.dumps(request_body)
    print(request_data)

    # Be sure to add try/except error handling in the future
    response = requests.post(UPDATE_IMAGE_REQUEST_HISTORY_URL, data=request_data, headers=HEADERS)

    try:
        data = response.json()
    except requests.JSONDecodeError:
        data = None
    print(data)


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

#Note: ImageRequestHistory properties are formatted for the frontend, uses camelcase instead of snakecase
class ImageRequestHistory:
    def __init__(self, imageUrl, visionApiResults):
        self.imageUrl = imageUrl
        self.visionApiResults = visionApiResults

    def __str__(self):
        return f"{self.imageUrl}, {self.visionApiResults}"

    # Used to convert and make Class Object serializable.
    def to_dict(self):
        return {
            "imageUrl": self.imageUrl,
            "visionApiResults": self.visionApiResults
        }