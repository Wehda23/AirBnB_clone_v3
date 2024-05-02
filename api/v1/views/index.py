#!/usr/bin/python3
"""
Contains apis
"""
from api.v1.views import app_views
import json


@app_views.route("/status")
def stats(self) -> str:
    """
    stats
    """
    return json.dumps({"status": "OK"})
