#!/usr/bin/python3
"""
File that contains view for Amenity object that handles all RESTFul API Actions
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

prefix = "/amenities"


@app_views.route(prefix, methods=["GET"], strict_slashes=False)
def get_amenities():
    """Retrieve all amenities."""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities]), 200


@app_views.route(
    prefix + "/<amenity_id>", methods=["GET"], strict_slashes=False
)
def get_amenity(amenity_id):
    """Retrieve an amenity by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)


@app_views.route(
    prefix + "/<amenity_id>", methods=["DELETE"], strict_slashes=False
)
def delete_amenity(amenity_id):
    """Deletes an amenity by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(prefix, methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a new amenity."""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    prefix + "/<amenity_id>", methods=["PUT"], strict_slashes=False
)
def update_amenity(amenity_id):
    """Update an existing amenity."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
