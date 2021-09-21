#!/usr/bin/python3
"""places amenities"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review
from flasgger.utils import swag_from

TYPE_STORAGE = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_yaml/places_amenity/place_amenities_get.yml',
           methods=['GET'])
def retrieve_Amenity_for_place(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    getListA = []
    if TYPE_STORAGE == 'db':
        amenitiesObjs = place.amenities
    else:
        amenitiesObjs = place.amenity_ids
    for placeA in amenitiesObjs:
        getListA.append(placeA.to_dict())
    return jsonify(getListA)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('swagger_yaml/places_amenity/place_amenity_delete.yml',
           methods=['DELETE'])
def place_amenity_delete(place_id, amenity_id):
    """delete a amenity object from a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if TYPE_STORAGE == 'db':
        placeAmenityObj = place.amenities
    else:
        placeAmenityObj = place.amenity_ids
    if amenity not in placeAmenityObj:
        abort(404)
    placeAmenityObj.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
@swag_from('swagger_yaml/places_amenity/place_amenity_post.yml',
           methods=['POST'])
def amenity_place_post(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if TYPE_STORAGE == 'db':
        placeAmenityObj = place.amenities
    else:
        placeAmenityObj = place.amenity_ids
    if amenity in placeAmenityObj:
        return jsonify(amenity.to_dict())
    placeAmenityObj.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
