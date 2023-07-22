from config.mongo import db

User = db['users']
EventOrganizer = db['eventOrganizers']
VenueProvider = db['venueProviders']
Event = db['events']
Venue = db['venue']
Movie = db['movie']
MovieShow = db['movieShow']
Ticket = db['ticket']
Seat = db['seats']
TimeSlot = db['timeSlot']