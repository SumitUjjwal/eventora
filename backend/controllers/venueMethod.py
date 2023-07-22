# list of functionalities for Venue Providers:

# Venue Provider Registration: Venue Providers can register themselves with the system, providing necessary details such as their name, contact information, and other required information. Upon registration, Venue Providers will be marked as not verified.

# Add New Venue: Venue Providers can add a new venue with the name of the venue, address, capacity, and time slots.

# Update Venue Details: Venue Providers can edit and update the details of a venue they have added. This includes updating the venue name, address, capacity, and time slots.

# Remove Venue: Venue Providers can remove a venue they have added using the venue ID.

# View Venue List: Venue Providers can view a list of all the venues they have added along with their demographic details and the booked slots.

# Search and Filter Venues: Implement a search and filtering functionality for Venue Providers to easily find their venues based on different criteria such as venue name, location, capacity, etc.

# Venue Verification: Admins can verify Venue Providers manually. After verification, Venue Providers will be marked as verified, and they can perform other tasks in the system.


from flask import request, jsonify
from models.model import Venue, TimeSlot
from datetime import datetime, timedelta
import pytz
from bson.objectid import ObjectId

# Create time slots for venue
def create_time_slots_for_venue(venue_id, date, start_time, end_time, interval=2):
    num_slots = (end_time - start_time) // interval

    for i in range(num_slots):
        time_slot_start = start_time + i * interval
        time_slot_end = start_time + (i + 1) * interval

        time_slot = TimeSlot.insert_one(
                {
                    'venue_id': venue_id, 
                    'date': date, 
                    'start_time': time_slot_start, 
                    'end_time': time_slot_end,
                    'is_booked': False
                }
            )

    return num_slots

# Add New Venue
def add_new_venue():
    try:
        data = request.json
        venue_name = data.get("venue_name")
        address = data.get("address")
        city = data.get("city")
        state = data.get("state")
        opening_time = data.get("opening_time")
        closing_time = data.get("closing_time")
        venue_provider = request.user_id
        is_verified = False

        venue_data = {
            'venue_name': venue_name,
            'address': address,
            'city': city,
            'state': state,
            'opening_time': opening_time,
            'closing_time': closing_time,
            'venue_provider': venue_provider,
            'is_verified': is_verified
        }

        if Venue.find_one({'venue_name': venue_name}):
            return jsonify({'error': 'Venue already exists'}), 409

        venue_id = Venue.insert_one(venue_data).inserted_id

        ist = pytz.timezone('Asia/Kolkata')
        current_date = datetime.now(ist)

        for i in range(7):
            date = (current_date + timedelta(days=i)).strftime('%Y-%m-%d')
            create_time_slots_for_venue(venue_id, date, opening_time, closing_time, interval=2)

        return (
                jsonify(
                    {
                        "OK": True,
                        "message": "Venue created successfully",
                        "venue_id": str(venue_id),
                    }
                ),
                201,
            )
    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )

# Update a venue
def update_venue(venue_id):
    try:
        data = request.json
        new_venue_name = data.get("venue_name")
        new_address = data.get("address")
        new_city = data.get("city")
        new_state = data.get("state")
        new_opening_time = data.get("opening_time")
        new_closing_time = data.get("closing_time")

        # Find the venue by its ID in the database
        venue = Venue.find_one({'_id': ObjectId(venue_id)})

        if not venue:
            return jsonify({'error': 'Venue not found'}), 404

        # Create a dictionary containing the updated fields
        updated_fields = {}
        if new_venue_name:
            updated_fields['venue_name'] = new_venue_name
        if new_address:
            updated_fields['address'] = new_address
        if new_city:
            updated_fields['city'] = new_city
        if new_state:
            updated_fields['state'] = new_state        
        if new_opening_time:
            updated_fields['opening_time'] = new_opening_time
        if new_closing_time:
            updated_fields['closing_time'] = new_closing_time

        # Update the venue with the new details
        Venue.update_one({'_id': ObjectId(venue_id)}, {'$set': updated_fields})

        return jsonify({"OK": True, "message": "Venue updated successfully"}), 200

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )

# Remove a venue
def remove_venue(venue_id):
    try:
        # Find the venue by its ID in the database
        venue = Venue.find_one({'_id': ObjectId(venue_id)})

        if not venue:
            return jsonify({'error': 'Venue not found'}), 404

        # Remove the venue from the database
        Venue.delete_one({'_id': ObjectId(venue_id)})

        return jsonify({"OK": True, "message": "Venue removed successfully"}), 200

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )

# Get venue
def get_venues_by_provider():
    try:
        venue_provider_id = request.user_id
        search_query = request.args.get('search')
        filter_capacity = request.args.get('capacity')
        filter_city = request.args.get('city')
        filter_state = request.args.get('state')

        query = {'venue_provider': venue_provider_id}

        if search_query:
            query['venue_name'] = {'$regex': search_query, '$options': 'i'}

        if filter_capacity:
            query['capacity'] = int(filter_capacity)
        if filter_city:
            query['city'] = int(filter_city)
        if filter_state:
            query['state'] = int(filter_state)        

        venues = list(Venue.find(query))

        for venue in venues:
            venue['_id'] = str(venue['_id'])

        return jsonify(venues), 200

    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )
    
