from flask import Blueprint
from controllers.venueMethod import (
        add_new_venue,
        update_venue,
        remove_venue,
        get_venues_by_provider,
    )
from middlewares.authenticator import token_required

# create a new instance
venue = Blueprint('venue', __name__)

# Add a new venue
@venue.route('/provider/add', methods=['POST'])
@token_required
def add_new_venue_route():
    return add_new_venue()

# Update a venue
@venue.route('/provider/update/<venue_id>', methods=['PATCH'])
@token_required
def update_venue_route(venue_id):
    return update_venue(venue_id)

# Remove a venue
@venue.route('/provider/remove/<venue_id>', methods=['DELETE'])
@token_required
def remove_venue_route(venue_id):
    return remove_venue(venue_id)

# Get list of venue
@venue.route('/provider/list', methods=['GET'])
@token_required
def get_venue_by_provider_route():
    return get_venues_by_provider()