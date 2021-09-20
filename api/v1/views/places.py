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
from os import getenv


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
    places = storage.all(Place).values()
    places_list = []
    states_list = []
    cities_list = []
    amenities_list = []
    slist = []
    clist = []
    alist = []
    plist = []
    slist_two = []
    clist_two = []
    states_len = 0
    cities_len = 0
    amenities_len = 0
    amenity_exists_list = []
    try:
        new_dict = request.get_json()
    except:
        return {"error": "Not a JSON"}, 400
    if request.headers['Content-Type'] != 'application/json':
        return {"error": "Not a JSON"}, 400
    for place in places:
        places_list.append(place.to_dict())
    if len(new_dict) == 0:
        return jsonify(places_list)
    if 'states' in new_dict:
        states_len = len(new_dict['states'])
        states_list = new_dict['states']
    if 'cities' in new_dict:
        cities_len = len(new_dict['cities'])
        cities_list = new_dict['cities']
    if 'amenities' in new_dict:
        amenities_len = len(new_dict['amenities'])
        amenities_list = new_dict['amenities']
    amenity_list_length = len(amenities_list)
    total_len = states_len + cities_len + amenities_len
    if total_len == 0:
        return jsonify(places_list)
    if states_len > 0:
        for state_id in states_list:
            my_state = storage.get(State, state_id)
            if my_state is not None:
                slist.append(my_state)
        for state in slist:
            for city in state.cities:
                for place in city.places:
                    plist.append(place.to_dict())
    if cities_len > 0:
        for city_id in cities_list:
            my_city = storage.get(City, city_id)
            if my_city is not None:
                clist.append(my_city)
        for city in clist:
            for place in city.places:
                plist.append(place.to_dict())
    if amenities_len > 0:
        if len(plist) == 0:
            for place in places:
                amenity_exists_list = []
                for a in place.amenities:
                    for amenity_id in amenities_list:
                        if a.id == amenity_id:
                            amenity_exists_list.append(1)
                            break
                if len(amenity_exists_list) == amenity_list_length:
                    plist.append(place.to_dict())
        else:
            plist_two = []
            if states_len > 0:
                for state_id in states_list:
                    my_state = storage.get(State, state_id)
                    if my_state is not None:
                        slist_two.append(my_state)
                for state in slist_two:
                    for city in state.cities:
                        for place in city.places:
                            amenity_exists_list = []
                            for a in place.amenities:
                                for amenity_id in amenities_list:
                                    if a.id == amenity_id:
                                        amenity_exists_list.append(1)
                                        break
                            if len(amenity_exists_list) == amenity_list_length:
                                plist_two.append(place.to_dict())
            if cities_len > 0:
                for city_id in cities_list:
                    my_city = storage.get(City, city_id)
                    if my_city is not None:
                        clist_two.append(my_city)
                for city in clist_two:
                    for place in city.places:
                        amenity_exists_list = []
                        for a in place.amenities:
                            for amenity_id in amenities_list:
                                if a.id == amenity_id:
                                    amenity_exists_list.append(1)
                                    break
                        if len(amenity_exists_list) == amenity_list_length:
                            plist_two.append(place.to_dict())
            if len(plist_two) > 0:
                return jsonify(plist_two)
    if len(plist) > 0:
        return jsonify(plist)
    return {"error": "Not found"}, 404
