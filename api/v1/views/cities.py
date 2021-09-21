#!/usr/bin/python3
"""cities"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_yaml/city/cities_get.yml', methods=['GET'])
def get_cities(state_id):
    """get cities"""
    objState = storage.get(State, state_id)
    if objState is None:
        abort(404)
    getListC = []
    for city in storage.all("City").values():
        if city.state_id == state_id:
            getListC.append(city.to_dict())
    return jsonify(getListC)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_yaml/city/city_get.yml', methods=['GET'])
def retrieve_City(city_id):
    """get city by id"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('swagger_yaml/city/city_delete.yml', methods=['DELETE'])
def city_delete(city_id):
    """delete a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('swagger_yaml/city/city_post.yml', methods=['POST'])
def city_post(state_id):
    """create a city"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    kCity = request.get_json()
    kCity['state_id'] = state_id
    city = City(**kCity)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_yaml/city/city_put.yml', methods=['PUT'])
def city_put(city_id):
    """update a city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
