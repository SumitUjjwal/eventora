from flask import Blueprint
from controllers.userAuth import (login, signup)

# create a new instance
auth = Blueprint('auth', __name__)

@auth.route('/user/login', methods=['POST'])
def login_route():
    return login()

@auth.route('/user/signup', methods=['POST'])
def signup_route():
    return signup()