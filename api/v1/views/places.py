#!/usr/bin/python3
"""
File that contains view for Place object that handles all RESTFul API Actions
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User

prefix = "/places"


@app_views.route(
    "/cities/<city_id>/places", methods=["GET"], strict_slashes=False
)
def get_places(city_id):
    """Retrieve all places of a city."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places), 200


@app_views.route(prefix + "/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieve a place by ID."""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route(
    prefix + "/<place_id>", methods=["DELETE"], strict_slashes=False
)
def delete_place(place_id):
    """Deletes a place by ID."""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Create a new place."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    if "name" not in data:
        abort(400, description="Missing name")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route(prefix + "/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update an existing place."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
