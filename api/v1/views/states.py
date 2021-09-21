#!/usr/bin/python3
"""states"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/state/states_get.yml', methods=['GET'])
def states():
    """get states"""
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/state/state_get.yml', methods=['GET'])
def state_get(state_id):
    """get state by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('swagger_yaml/state/state_delete.yml', methods=['DELETE'])
def state_delete(state_id):
    """delete a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('swagger_yaml/state/state_post.yml', methods=['POST'])
def state_post():
    """create a state"""
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_yaml/state/state_put.yml', methods=['PUT'])
def state_put(state_id):
    """update a state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
