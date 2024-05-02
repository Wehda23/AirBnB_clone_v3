#!/usr/bin/python3
"""
Contains apis
"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from models import storage
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=["GET"])
def OKStatus():
    """Function to return ok status"""
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route("/stats", methods=["GET"])
def stats():
    """Function to return stats"""
    models = {
        "states": State,
        "cities": City,
        "amenities": Amenity,
        "places": Place,
        "reviews": Review,
        "users": User,
    }
    for key in models:
        models[key] = storage.count(models[key])
    return jsonify(models)
