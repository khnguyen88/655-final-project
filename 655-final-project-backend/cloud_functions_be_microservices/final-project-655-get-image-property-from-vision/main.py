import functions_framework
from google.cloud import vision
from google.protobuf.json_format import MessageToJson
from google.protobuf.json_format import MessageToDict
from google.cloud.vision_v1 import AnnotateImageResponse
from PIL import Image
from urllib.request import urlopen
import os
import io
import base64
import json
import requests
import proto
import re
# import jsonify #Note, could not get to work with functions_framework. So I created my own custom response



@functions_framework.http
def get_image_property_from_vision(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Retrieve request body and arguments
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

    # Attempt to process image URL and send response to the proper client and request to another backend server for additional processing.
    # Note: did not realize python class object is not serializable like JS/TS. Use Dictionary objects instead. There are other conversion options too.
    try:
        # Obtain the urlString property from the request body
        print('Flag-1: Extract urlString property from request body')
        if request_json and 'urlString' in request_json:
            image_url = request_json['urlString']
        else:
            error_response = CustomResponse("No image url was provided. Please try again", "URL is missing", 500)
            return (json.dumps(error_response.to_dict()), 500, HEADERS)

        # Call Vision API to obtain image properties of a given image URL
        print('Flag-2: Obtain image properties from Vision API')
        vision_api_response = detect_properties(image_url)

        # Request a serverless function to add contents of image url to storage bucket
        print('Flag-3: Add contents of image url to storage bucket')
        put_image_url_content_to_storage_bucket(image_url, vision_api_response)

        ok_response = CustomResponse(f"The image from the url has been successfully processed. URL: {image_url}. Note, it may take a few minutes for the results to display in the gallery.", "None", 200)
        return (json.dumps(ok_response.to_dict()), 200, HEADERS)

    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        error_response = {"message": "An error occurred", "error": str(e), "status": 500}
        return (json.dumps(error_response), 500, HEADERS)

# Google Template code + extra
# https://cloud.google.com/vision/docs/detecting-properties
def detect_properties(path):
    """Detects image properties in the file."""

    key_filename = 'service-account-key.json'
    test = open(key_filename)

    # Create a Vision API client
    client = vision.ImageAnnotatorClient.from_service_account_json(key_filename)  #Works, but not needed for services internal to the cloud project. Only for applications external to the cloud network.
    # client = vision.ImageAnnotatorClient() # Works, this should be sufficient for services internal to the cloud project

    #=======================================
    # This simulate if we pass image as bytes from a body request (but we can encode it/decode it as string 64 if needed too)
    #=======================================
    # img = Image.open(urlopen(path))
    # rawBytes = io.BytesIO()
    # img.save(rawBytes, "JPEG") #Change file type
    # rawBytes.seek(0)
    # content = rawBytes.read()

    # image = vision.Image(content=content)
    #=======================================


    #=======================================
    # If this is an image from URL, use this option
    #=======================================
    image = vision.Image()

    image.source.image_uri = path
    #=======================================

    response = client.image_properties(image=image)

    props = response.image_properties_annotation

    print("Properties:")
    for color in props.dominant_colors.colors:
        print(f"fraction: {color.pixel_fraction}")
        print(f"\tr: {color.color.red}")
        print(f"\tg: {color.color.green}")
        print(f"\tb: {color.color.blue}")
        print(f"\ta: {color.color.alpha}")


    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    # Google Cloud Vision Returns Pseudo Object. Cannot be converted to JSON normally. Request additional library to do so.
    # https://stackoverflow.com/questions/76196376/parsing-and-saving-google-vision-api-response-as-json
    # https://stackoverflow.com/questions/52169264/vision-api-how-to-get-json-output
    # https://stackoverflow.com/questions/19734617/protobuf-to-json-in-python
    
    # response_json = AnnotateImageResponse.to_json(response) 

    # Attempts to solve the wrong issue, why image collection.json was storing the cloud vision response weirdly. Showed newlines and unwanted characters. Stored the wrong data format. 
    
    # JSON string is fine. But I needed the VisionApiResults to store a dict of the response object and not json string.
    # response_json = MessageToJson(response) #Creates error, do not use! Need additional properties
    # response_json = json.dumps(MessageToDict(response)) #Creates error, do not use! Need additional properties
    # response_json = proto.Message.to_json(response) #Provides formatted JSON String
    # response_json = MessageToJson(response._pb) #Provides formatted JSON String
    # response_json = json.dumps(MessageToDict(response._pb)) #Provides compacted JSON String

    #DOH - SILLY ME, I NEEDED TO PROVIDE A DICT NOT JSON STRING
    response_dict_obj = MessageToDict(response._pb) # Converts to py obj (dict)
    print(json.dumps(response_dict_obj)) # Converts to JSONs string for printing only
    return response_dict_obj # Returns response py dict obj


def put_image_url_content_to_storage_bucket(image_url, vision_api_response):

    ADD_IMAGE_URL_CONTENT_TO_GCS_URL = #ADD URL OF CLOUD RUN FUNCTION HERE

    HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    request_body = {
        "image_url": image_url,
        "vision_api_results": vision_api_response
    }

    request_data = json.dumps(request_body)
    print(request_data)

    # Be sure to add try/except error handling in the future
    response = requests.post(ADD_IMAGE_URL_CONTENT_TO_GCS_URL, data=request_data, headers=HEADERS)

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