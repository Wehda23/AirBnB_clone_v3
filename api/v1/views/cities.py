#!/usr/bin/python3
"""
File that contains view for Cities object that handles all RESTFul API Actions
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


prefix = "/cities"


# API to retrieve all states
@app_views.route(
    "/states/<state_id>" + prefix, methods=["GET"], strict_slashes=False
)
def get_cities(*args, **kwargs):
    """
    Retrieve all cities
    """
    # Grab the state
    state = storage.get(State, kwargs.get("state_id"))
    if not state:
        # Error 404
        abort(404)
    # State exists!!
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


# API to retrieve a city by id
@app_views.route(prefix + "/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(*args, **kwargs):
    """
    Retrieve a city by id
    """
    # Get city_id
    city_id = kwargs.get("city_id")
    # Grab the city object
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    # Incase state is None
    abort(404)


# API to delete a city
@app_views.route(
    prefix + "/<city_id>", methods=["DELETE"], strict_slashes=False
)
def delete_city(*args, **kwargs):
    """
    Deletes a city by id
    """
    # Get city_id
    city_id = kwargs.get("city_id")
    # Grab the city object
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    # Incase city is None
    abort(404)


# API to create a city
@app_views.route(
    "/states/<state_id>" + prefix, methods=["POST"], strict_slashes=False
)
def create_city(*args, **kwargs):
    """
    Create a new city object
    """
    state = storage.get(State, kwargs.get("state_id"))
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = City(**data)
    instance.state_id = state.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


# API to update a city
@app_views.route(prefix + "/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(*args, **kwargs):
    """
    Updates an existing city object
    """
    # Grab the id
    city = storage.get(City, kwargs.get("city_id"))
    # Check if id is not in data
    if not city:
        abort(404)
    # Grab the request body
    data = request.get_json()
    # Check if data is empty
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # update city
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    # Save
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
