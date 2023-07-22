from flask import Blueprint
from controllers.userAuth import (login, signup)

# create a new instance
auth = Blueprint('auth', __name__)

# User Authentication
@auth.route('/user/login', methods=['POST'])
def login_route():
    return login()

@auth.route('/user/signup', methods=['POST'])
def signup_route():
    return signup()

# Venue Provider Authentication
@auth.route('/venue/provider/login', methods=['POST'])
def venue_provider_login_route():
    return login()

@auth.route('/venue/provider/signup', methods=['POST'])
def venue_provider_signup_route():
    return signup()

# Event Organizer Authentication
@auth.route('/event/organizer/login', methods=['POST'])
def event_organizer_login_route():
    return login()

@auth.route('/event/organizer/signup', methods=['POST'])
def event_organizer_signup_route():
    return signup()