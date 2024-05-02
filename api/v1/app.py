#!/usr/bin/python3
"""
File contains script to run flask app
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def downtear(exception):
    """
    Function that runs when application is closed
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors with JSON response."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=HOST, port=PORT, threaded=True)
