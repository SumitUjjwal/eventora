# 1. Event organizer will register and log in.
# 2. can get a list of verified venue providers and verified venues.
# 3. view venue availability
# 4. able to book one or more than one vacant slot in verified venues.
# 5. can cancel any booking only if there is a difference greater than 24 hours between booked slot's time and current time (Time Zone: 'Asia/Kolkata').
# 6. view their own events.
# 7. update event details.
# 8. view booking history

from flask import request, jsonify
from models.model import Venue, TimeSlot, EventOrganizer
from datetime import datetime, timedelta
import pytz
from bson.objectid import ObjectId

# Get venue
def get_venue():
    try:
        search_query = request.args.get('search')
        filter_capacity = request.args.get('capacity')
        filter_city = request.args.get('city')
        filter_state = request.args.get('state')

        query = {'is_verified': True, 'city': filter_city, 'state': filter_state}

        if search_query:
            query['venue_name'] = {'$regex': search_query, '$options': 'i'}

        if filter_capacity:
            query['capacity'] = int(filter_capacity)

        venues = list(Venue.find(query))

        for venue in venues:
            venue['_id'] = str(venue['_id'])

        return jsonify(venues), 200

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )
    
# Get available slots
def get_available_slots(id):
    try:
        venue_id = ObjectId(id)
        date = request.args.get('date')

        venue = Venue.find_one({"_id": ObjectId(venue_id)})
        if not venue:
            return jsonify({"error": "Venue not found"}), 404

        # Get the venue's available time slots for the specified date
        available_slots = list(TimeSlot.find({'venue_id': venue_id, 'date': date, 'is_booked': False}))
        for slot in available_slots:
            slot['_id'] = str(slot['_id'])
            slot['venue_id'] = str(slot['venue_id'])

        return jsonify({"venue_id": str(venue_id), "date": date, "available_slots": available_slots}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Book available slots
def book_available_slots():
    try: 
        selected_slots = request.json.get('selected_slots')
        organizer_id = request.user_id
        
        for slot in selected_slots:
            timeSlot = TimeSlot.find_one({'_id': ObjectId(slot)})
            print(timeSlot)
            if timeSlot['is_booked'] == True:
                return ({'error': 'Sorry, selected slot is no longer available'})

        for slot in selected_slots:
            timeSlot = TimeSlot.find_one_and_update({'_id': ObjectId(slot)}, {'$set': {'is_booked': True, 'organizer_id': ObjectId(organizer_id)}})

        return jsonify({'OK': True, 'message': 'Slot booked successfully'}), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    
# cancel a booked slot
def cancel_booked_slot(slot_id):
    try:
        slot = TimeSlot.find_one({"_id": ObjectId(slot_id)})
        if not slot:
            return jsonify({"error": "Slot not found"}), 404

        ist = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(ist).date()
        booking_date = datetime.strptime(slot['date'], "%Y-%m-%d").date()

        if booking_date == current_date:
            return jsonify({"error": "Cannot cancel the slot on the day of the event"}), 400
        elif booking_date < current_date:
            return jsonify({"error": "Cannot cancel a slot for a past event"}), 400
        
        # Update the slot to mark it as available for booking
        TimeSlot.update_one({"_id": ObjectId(slot_id)}, {"$set": {"is_booked": False, "organizer_id": None}})

        return jsonify({"OK": True, "message": "Slot canceled successfully"}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500
    

# Get Booking history
def get_booking_history():
    try:
        filter_date = request.args.get('date')
        organizer_id = request.user_id

        query = {'organizer_id': ObjectId(organizer_id)}

        if filter_date:
            query['date'] = filter_date

        booked_slots = list(TimeSlot.find(query))
        for booked_slot in booked_slots:
            booked_slot['_id'] = str(booked_slot['_id'])
            booked_slot['venue_id'] = str(booked_slot['venue_id'])
            booked_slot['organizer_id'] = str(booked_slot['organizer_id'])
            
            venue_cursor = Venue.find_one({'_id': ObjectId(booked_slot['venue_id'])})
            if venue_cursor:
                venue_cursor['_id'] = str(venue_cursor['_id'])
                booked_slot['venue_details'] = venue_cursor
                
            organizer_cursor = EventOrganizer.find_one({'_id': ObjectId(booked_slot['organizer_id'])})
            if organizer_cursor:
                organizer_cursor['_id'] = str(organizer_cursor['_id'])
                booked_slot['organizer_details'] = organizer_cursor

        return jsonify(booked_slots), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500