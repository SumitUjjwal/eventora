from config.mongo import db

User = db['users']
EventOrganizer = db['eventOrganizers']
VenueProvider = db['venueProviders']
Event = db['events']
Venue = db['venue']
Movie = db['movie']
MovieShow = db['movie_show']
Ticket = db['ticket']