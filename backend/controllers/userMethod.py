from flask import jsonify, request
from models.model import User, Venue, Event, Movie, Ticket, MovieShow, Seat
# from seatMethod import initialize_seat_matrix, update_seat_status
from .seatMethod import initialize_seat_matrix, update_seat_status

# Get List of Events
def get_events():
    # Get query parameters
    city = request.args.get('city')
    date = request.args.get('date')
    language = request.args.get('language')
    search_query = request.args.get('search')

    # Construct the query based on the provided parameters
    query = {}
    if city:
        query['city'] = city
    if date:
        query['date'] = date
    if language:
        query['language'] = language
    if search_query:
        query['title'] = {'$regex': f'.*{search_query}.*', '$options': 'i'}

    # Fetch filtered and searched events from the 'events' collection in MongoDB
    events = list(Event.find(query))

    # Convert the events data to a list of dictionaries and return as JSON
    return jsonify(events), 200

# # Get list of Movies
# def get_movies():
#     # Get query parameters
#     city = request.args.get('city')
#     date = request.args.get('date')
#     language = request.args.get('language')
#     sort_order = request.args.get('sort')
#     search_query = request.args.get('search')

#     # Construct the query based on the provided parameters
#     query = {}
#     if city:
#         query['city'] = city
#     if date:
#         query['date'] = date
#     if language:
#         query['language'] = language
#     if search_query:
#         query['title'] = {'$regex': f'.*{search_query}.*', '$options': 'i'}    

#     # Fetch filtered movies from the 'movies' collection in MongoDB
#     movies = list(Movie.find(query))

#     # Sort movies based on release date
#     if sort_order == 'asc':
#         movies.sort(key=lambda movie: movie['release_date'])
#     elif sort_order == 'desc':
#         movies.sort(key=lambda movie: movie['release_date'], reverse=True)

#     # Convert the movies data to a list of dictionaries and return as JSON
#     return jsonify(movies), 200



# # ******************************ON HOLD**********************************
# def initialize_seats():
#     # Initialize the seat matrix and store it in the database
#     seat_matrix = initialize_seat_matrix()
#     Seat.insert_many([{"row": i, "seats": row} for i, row in enumerate(seat_matrix)])

#     return jsonify({"message": "Seat matrix initialized."}), 200

# def book_seat():
#     data = request.get_json()
#     row = data.get('row')
#     column = data.get('column')

#     # Check if the seat is available (0) in the database
#     seat_status = Seat.find_one({"row": row})['seats'][column]
#     if seat_status != 0:
#         return jsonify({"message": "Seat is not available."}), 400

#     # Update the seat status to booked (1) in the database
#     update_seat_status(row, column, 1)
#     return jsonify({"message": "Seat booked successfully."}), 200

# def get_seats():
#     # Fetch the seat matrix status from the database
#     seat_matrix = list(Seat.find({}, {"_id": 0}))

#     return jsonify({"seats": seat_matrix}), 200
# # ******************************ON HOLD**********************************