#!/usr/bin/python3
"""
File that contains view for User object that handles all RESTFul API Actions
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User

prefix = "/users"


@app_views.route(prefix, methods=["GET"], strict_slashes=False)
def get_users():
    """Retrieve all users."""
    # Grab users
    users = storage.all(User).values()
    # Return response
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route(prefix + "/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(*args, **kwargs):
    """Retrieve a user by ID."""
    # Grab user
    user = storage.get(User, kwargs.get("user_id"))
    # Check if user exists
    if user:
        return jsonify(user.to_dict()), 200
    # User does not exists return page not found
    abort(404)


@app_views.route(
    prefix + "/<user_id>", methods=["DELETE"], strict_slashes=False
)
def delete_user(user_id):
    """Deletes a user by ID."""
    # Get user
    user = storage.get(User, user_id)
    # Check if user object is not None
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    # Return page not found if user does not exists
    abort(404)


@app_views.route(prefix, methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new user."""
    # Grab the data from .get_json() method
    data = request.get_json()
    # If not data
    if not data:
        abort(400, description="Not a JSON")
    # If email does not exist in data
    if "email" not in data:
        abort(400, description="Missing email")
    # If email does not exists in data
    if "password" not in data:
        abort(400, description="Missing password")
    # Create new user
    user = User(**data)
    # Save
    user.save()
    # Return User as a response
    return jsonify(user.to_dict()), 201


@app_views.route(prefix + "/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update an existing user."""
    # Grab user
    user = storage.get(User, user_id)
    # Check if user does not exists
    if not user:
        abort(404)
    # Grab the data
    data = request.get_json()
    # If data is empty
    if not data:
        abort(400, description="Not a JSON")
    # Ignore those keys
    ignore_keys = ["id", "email", "password", "created_at", "updated_at"]
    # loop over the data.
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    # Save new data
    storage.save()
    # Return Response
    return jsonify(user.to_dict()), 200
