#!/usr/bin/python3
"""places reviews"""

from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.review import Review

@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """get places reviews"""
    objPlaceReview = storage.get("Review", place_id)
    if objPlaceReview is None:
        abort(404)
    getListPR = []
    for placeR in storage.all("Review").values():
        if placeR.place_id == place_id:
            getListPR.append(placeR.to_dict())
    return jsonify(getListPR)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrieve_place_review(review_id):
    """get place review by id"""
    placeR = storage.get("Review", review_id)
    if placeR is None:
        abort(404)
    return jsonify(placeR.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def place_review_delete(review_id):
    """delete a place review"""
    placeR = storage.get("Review", review_id)
    if placeR is None:
        abort(404)
    placeR.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def place_review_post(place_id):
    """create a place review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    placeR = request.get_json()
    if placeR is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in placeR:
        abort(400, 'Missing user_id')
    user = storage.get("User", placeR.get("user_id"))
    if user is None:
        abort(404)
    if 'text' not in place:
        abort(400, 'Missing password')
    placeR['place_id'] = place_id
    kPlaceR = Review(**placeR)
    storage.new(kPlaceR)
    storage.save()
    return (kPlaceR.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def place_put(review_id):
    """update a place review"""
    placeR = storage.get("Review", review_id)
    if placeR is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for k, v in request.get_json().items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at', 'city_id']:
            setattr(placeR, k, v)
    placeR.save()
    return jsonify(placeR.to_dict()), 200
