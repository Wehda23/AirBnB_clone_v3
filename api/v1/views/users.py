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
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route(prefix + "/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user by ID."""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        abort(404)


@app_views.route(
    prefix + "/<user_id>", methods=["DELETE"], strict_slashes=False
)
def delete_user(user_id):
    """Deletes a user by ID."""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(prefix, methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new user."""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "email" not in data:
        abort(400, description="Missing email")
    if "password" not in data:
        abort(400, description="Missing password")
    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(prefix + "/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update an existing user."""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    ignore_keys = ["id", "email", "password", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
