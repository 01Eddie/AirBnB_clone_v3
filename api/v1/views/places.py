#!/usr/bin/python3
"""places"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place(city_id):
    """get places"""
    objPlace = storage.get("City", city_id)
    if objPlace is None:
        abort(404)
    getListU = []
    for place in storage.all("Place").values():
        if place.city_id == city_id:
            getListU.append(place.to_dict())
    return jsonify(getListU)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_place(place_id):
    """get place by id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """delete a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def place_post(city_id):
    """create a place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    place = request.get_json()
    if place is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in place:
        abort(400, 'Missing user_id')
    user = storage.get("User", place['user_id'])
    if user is None:
        abort(404)
    if 'name' not in place:
        abort(400, 'Missing name')
    place['city_id'] = city_id
    kPlace = Place(**place)
    storage.new(kPlace)
    storage.save()
    return make_response((kPlace.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'created_at', 'updated_at', 'city_id']:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches for a place"""
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        abort(400, 'Not a Json')
