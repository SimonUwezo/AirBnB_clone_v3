#!/usr/bin/python3
"""API Routes for Reviews.

This module defines the API routes for handling reviews in the Flask app.
It includes route handlers for retrieving all reviews for a place,
retrieving a specific review by ID, deleting a review, creating a new review,
and updating an existing review."""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("places/<place_id>/reviews",
                 strict_slashes=False, methods=["GET"])
def get_reviews(place_id):
    """Retrieve all reviews for a place.

    Args:
        place_id (str): The ID of the place.

    Returns:
        A JSON response containing a list of all reviews for the place.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)

    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["GET"])
def get_review(review_id):
    """Retrieve a specific review by ID.

    Args:
        review_id (str): The ID of the review.

    Returns:
        A JSON response containing the details of the specified review.

    Raises:
        404: If the review with the specified ID does not exist.
    """
    review = storage.get(classes["Review"], review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_review(review_id):
    """Delete a review by ID.

    Raises:
        404: If the review with the specified ID does not exist.
    """
    review = storage.get(classes["Review"], review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=["POST"])
def post_review(place_id):
    """Create a new review for a place
    Raises:
        400: If the request data is not a valid JSON
             or if the 'user_id' field is missing.
        404: If the place or user with the specified IDs do not exist.
    """
    place = storage.get(classes["Place"], place_id)
    if place is None:
        abort(404)

    place_data = request.get_json(force=True, silent=True)
    if type(place_data) is not dict:
        abort(400, "Not a JSON")
    if "user_id" not in place_data:
        abort(400, "Missing user_id")

    user = storage.get(classes["User"], place_data["user_id"])
    if user is None:
        abort(404)

    if "text" not in place_data:
        abort(400, "Missing text")
    else:
        new_review = classes["Review"](place_id=place_id, **place_data)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=["PUT"])
def put_review(review_id):
    """Update an existing re
    """
    review = storage.get(classes["Review"], review_id)
    if review is None:
        abort(404)

    review_data = request.get_json(force=True, silent=True)
    if type(review_data) is not dict:
        abort(400, "Not a JSON")

    for key, value in review_data.items():
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict())
