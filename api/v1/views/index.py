#!/usr/bin/python3
"""Index file for views module"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Status route of API v1"""
    status_data = {"status": "OK"}
    return jsonify(status_data)