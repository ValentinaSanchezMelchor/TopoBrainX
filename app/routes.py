from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def hello():
    return jsonify({"message": "Hello, World!"})