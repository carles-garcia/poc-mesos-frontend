import json
import os

import requests
from flask import Flask, request
from flask.json import jsonify
from werkzeug.exceptions import BadRequest, HTTPException

app = Flask(__name__)

MARATHON = os.getenv("MARATHON_URL")


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps(
        {"status": f"{e.code} {e.name}", "message": e.description,}
    )
    response.content_type = "application/json"
    return response


@app.route("/application", methods=["POST"])
def start():
    try:
        name = request.json["name"]
    except KeyError:
        raise BadRequest("missing application name")
    replicas = request.json.get("replicas", 1)
    command = request.json.get("command", None)
    dockerImage = request.json.get("dockerImage", None)
    if not command and not dockerImage:
        raise BadRequest("missing command and/or dockerImage")
    json_params = {"id": name, "instances": replicas}
    if command:
        json_params["cmd"] = command
    if dockerImage:
        json_params["container"] = {
            "docker": {"image": dockerImage},
            "type": "DOCKER",
        }
    response = requests.post(MARATHON + "/v2/apps", json=json_params)
    return response.json()


@app.route("/application", methods=["GET"])
def list():
    response = requests.get(MARATHON + "/v2/apps")
    json_response = response.json()
    if response.status_code == 200:
        app_names = []
        for app in json_response["apps"]:
            app_names.append(app["id"])
        return jsonify(app_names)
    else:
        return json_response


@app.route("/application/<name>", methods=["GET"])
def show(name):
    response = requests.get(MARATHON + "/v2/apps/" + name)
    return response.json()


@app.route("/application/<name>", methods=["DELETE"])
def stop(name):
    response = requests.delete(MARATHON + "/v2/apps/" + name)
    return response.json()
