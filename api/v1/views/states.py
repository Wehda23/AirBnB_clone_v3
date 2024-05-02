#!/usr/bin/python3
"""
File that contains view for States object that handles all RESTFul API Actions
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State


prefix = "/states"


# API to retrieve all states
@app_views.route(prefix, methods=["GET"], strict_slashes=False)
def get_states(*args, **kwargs):
    """
    Retrieve all states
    """
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])


# API to retrieve a state by id
@app_views.route(prefix + "/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(*args, **kwargs):
    """
    Retrieve a state by id
    """
    # Get state_id
    state_id = kwargs.get("state_id")
    # Grab the state object
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    # Incase state is None
    abort(404)


# API to create a state
@app_views.route(prefix, methods=["POST"], strict_slashes=False)
def create_state(*args, **kwargs):
    """
    Create a new state object
    """
    # Get the request data
    data = request.get_json()
    # Check if data is empty
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    # Check if data contains key called `name`
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    # Create a new state object
    new_state = State(**data)
    # Save the new state object
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


# API to update a state
@app_views.route(prefix + "/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(*args, **kwargs):
    """
    Updates an existing state object
    """
    # Grab the id
    state = storage.get(State, kwargs.get("state_id"))
    # Check if id is not in data
    if not state:
        abort(404)
    # Grab the request body
    data = request.get_json()
    # Check if data is empty
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    # update state
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    # Save
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


# API to delete a state
@app_views.route(
    prefix + "/<state_id>", methods=["DELETE"], strict_slashes=False
)
def delete_state(*args, **kwargs):
    """
    Deletes a state by id
    """
    # Get state_id
    state_id = kwargs.get("state_id")
    # Grab the state object
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return make_response(jsonify({}), 200)
    # Incase state is None
    abort(404)
