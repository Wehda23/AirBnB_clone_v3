#!/usr/bin/python3
"""
Contains apis
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def OKStatus():
    """Function to return ok status"""
    return jsonify(status="OK")
