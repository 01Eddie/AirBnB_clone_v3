#!/usr/bin/python3
"""Flask application"""
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS, cross_origin
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
# Is defined in api/v1/views
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exception):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=os.getenv('HBNB_API_PORT', 5000), threaded=True)
