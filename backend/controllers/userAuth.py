from flask import Flask, jsonify, request
from models.model import User, VenueProvider, EventOrganizer
from pymongo.errors import DuplicateKeyError
from bson.json_util import dumps
from bson.objectid import ObjectId
import bcrypt
import jwt
import datetime
from dotenv import load_dotenv
import os

# Environment variables
load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

# Token expiration time
JWT_EXPIRATION_DELTA = datetime.timedelta(days=1)


# User Signup
def signup():
    try:
        data = request.get_json()
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")

        if not first_name or not last_name or not email or not password:
            return jsonify({"error": "All fields are required"}), 400

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        collection = User

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,
        }

        # checking whether the request is from venue provider
        request_url = request.url
        if 'venue/provider/signup' in request_url:
            user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": hashed_password,
                "is_verified": False
            }
            collection = VenueProvider
        elif 'event/organizer/signup' in request_url:
            user_data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": hashed_password,
                "is_verified": True
            }
            collection = EventOrganizer

        # Check if the email already exists
        if collection.find_one({"email": email}):
            return jsonify({"error": "Email already registered"}), 409

        # Insert the new user into the database
        user_id = collection.insert_one(user_data).inserted_id

        return (
            jsonify(
                {
                    "OK": True,
                    "message": "User registered successfully",
                    "user_id": str(user_id),
                }
            ),
            201,
        )
    except DuplicateKeyError:
        return jsonify({"error": "Email already registered"}), 409
    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )


# User login
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # checking whether the request is from venue provider
        collection = User
        request_url = request.url
        if 'venue/provider/login' in str(request_url):
            collection = VenueProvider
        elif 'event/organizer/signup' in request_url:
            collection = EventOrganizer

        # Check if the user exists and the provided password matches
        user = collection.find_one({"email": email})
        if user:
            if bcrypt.checkpw(password.encode("utf-8"), user["password"]):
                # Generate a JWT token
                token_payload = {
                    "user_id": str(user["_id"]),
                    "exp": datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA,
                }

                if collection == VenueProvider:
                    token_payload = {
                        "user_id": str(user["_id"]),
                        "is_verified": user["is_verified"],
                        "exp": datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA
                    }
                elif collection == EventOrganizer:
                    token_payload = {
                        "user_id": str(user["_id"]),
                        "is_verified": user["is_verified"],
                        "exp": datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA
                    }
                jwt_token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm="HS256")

                return (
                    jsonify(
                        {
                            "OK": True,
                            "message": "Login successful",
                            "user_id": str(user["_id"]),
                            "token": jwt_token,
                        }
                    ),
                    200,
                )
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return (
            jsonify({"error": "An unexpected error occurred", "details": str(e)}),
            500,
        )
