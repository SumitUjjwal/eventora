from flask import Blueprint
from controllers.userMethod import (
    get_events,
    get_movies,
    initialize_seats,
    book_seat,
    get_seats,
    )

user = Blueprint('user', __name__)

@user.route('/events', methods=['GET'])
def get_events_route():
    return get_events()


@user.route('/movies', methods=['GET'])
def get_movies_route():
    return get_movies()

@user.route('/initialize_seats', methods=['GET'])
def initialize_seats_route():
    return initialize_seats()

@user.route('/book_seat', methods=['POST'])
def book_seat_route():
    return book_seat()

@user.route('/seats', methods=['GET'])
def get_seats_route():
    return get_seats()