from flask import Blueprint
from controllers.eventMethod import (
        get_venue,
        get_available_slots,
        book_available_slots,
        cancel_booked_slot,
        get_booking_history,
    )
from middlewares.authenticator import token_required

# create a new instance
event = Blueprint('event', __name__)

# Get a list of venue
@event.route('/organizer/venues', methods=['GET'])
@token_required
def get_venue_route():
    return get_venue()

# Get a list of available slots
@event.route('/organizer/venues/<venue_id>', methods=['GET'])
@token_required
def get_available_slots_route(venue_id):
    return get_available_slots(venue_id)

# Book available slots
@event.route('/organizer/venues/slots/book', methods=['PATCH'])
@token_required
def book_available_slots_route():
    return book_available_slots()

# Cancel a booked slot
@event.route('/organizer/venues/slots/cancel/<slot_id>', methods=['PATCH'])
@token_required
def cancel_booked_slot_route(slot_id):
    return cancel_booked_slot(slot_id)

@event.route('/organizer/venues/history', methods=['GET'])
@token_required
def get_booking_history_route():
    return get_booking_history()