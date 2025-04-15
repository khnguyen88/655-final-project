import flask
import json
from flask_cors import CORS
from flask import Flask, request
import requests

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = flask.Flask(__name__)
CORS(app)

@app.get("/")
def hello():
    """Return a friendly HTTP greeting."""
    return "Hello World!\n"

@app.get("/get-image-request-history-collection-from-gcs")
def get_image_request_history_collection_from_gcs():    

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
        
    HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    GET_IMAGE_REQUEST_HISTORY_COLLECTION_URL = #ADD URL OF CLOUD RUN FUNCTION HERE

    print('Flag-A')
    response = requests.get(GET_IMAGE_REQUEST_HISTORY_COLLECTION_URL, headers=HEADERS)

    print('Flag-B')
    return response.json()

@app.post("/get-image-property-from-vision") #This is a POST despite the name because data will be processed and stored in storage bucket eventually
def get_image_property_from_vision():

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
        
    HEADERS = {
        "Access-Control-Allow-Origin": "*",
        "Content-Type": "application/json"
    }

    print('Flag-1')
    client_request_data = request.json #parsed json data, py obj
    
    CLOUD_RUN_FUNC_GET_IMAGE_PROPERTY_FROM_VISION = #ADD URL OF CLOUD RUN FUNCTION HERE

    # Be sure to add try/except error handling in the future
    print('Flag-2')
    response = requests.post(CLOUD_RUN_FUNC_GET_IMAGE_PROPERTY_FROM_VISION, json=client_request_data, headers=HEADERS)

    print('Flag-3')
    return (response.json(), 200, HEADERS)
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))