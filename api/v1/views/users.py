#!/usr/bin/python3
"""users"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get users"""
    getListU = []
    for user in storage.all("User").values():
        getListU.append(user.to_dict())
    return jsonify(getListU)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_User(user_id):
    """get user by id"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def user_delete(user_id):
    """delete a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def user_post():
    """create a user"""
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json():
        abort(400, 'Missing email')
    if 'password' not in request.get_json():
        abort(400, 'Missing password')
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def user_put(user_id):
    """update a user"""
    user = storage.get("User", user_id)
    if user is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
