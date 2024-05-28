#!/usr/bin/python3
"""API Routes for Cities.

This module defines the API routes for handling cities in the Flask app.
Routes:
- GET /states/<state_id>/cities: Retrieve all cities for a specific state.
- GET /cities/<city_id>: Retrieve a specific city by ID.
- DELETE /cities/<city_id>: Delete a city.
- POST /states/<state_id>/cities: Create a new city for a specific state.
- PUT /cities/<city_id>: Update an existing city.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.engine.db_storage import classes


@app_views.route("states/<state_id>/cities",
                 strict_slashes=False, methods=["GET"])
def get_cities(state_id):
    """Retrieve all cities for a specific state.

    Args:
        state_id: The ID of the state.

    Returns:
        A JSON response containing a list
        of all cities for the specified state.

    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city(city_id):
    """Retrieve a specific city by ID.
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=["DELETE"])
def del_city(city_id):
    """Delete a city.

    Args
        An empty JSON response.

    Raises:
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def post_city(state_id):
    """Create a new city for a specific state.

    Args:
        state_id: The ID of the state field is missing.
    """
    state = storage.get(classes["State"], state_id)
    if state is None:
        abort(404)

    city_data = request.get_json(force=True, silent=True)
    if type(city_data) is not dict:
        abort(400, "Not a JSON")

    if "name" in city_data:
        city = classes["City"](state_id=state_id, **city_data)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    else:
        abort(400, "Missing name")


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def put_city(city_id):
    """Update an existing:
        404: If the city with the specified ID does not exist.
        400: If the request data is not a valid JSON.
    """
    city = storage.get(classes["City"], city_id)
    if city is None:
        abort(404)

    city_data = request.get_json(force=True, silent=True)
    if type(city_data) is not dict:
        abort(400, "Not a JSON")

    for key, value in city_data.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict())
