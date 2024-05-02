#!/usr/bin/python3
"""
Contains apis
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def OKStatus():
    """Function to return ok status"""
    response = {"status": "OK"}
    return jsonify(response)
