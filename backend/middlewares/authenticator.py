import jwt
from functools import wraps
from flask import request, jsonify
from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check for the token in the Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            # Verify the token and decode the payload
            token_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            # Add the user_id to the request context for further use
            request.user_id = token_payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401

        return f(*args, **kwargs)

    return decorated
