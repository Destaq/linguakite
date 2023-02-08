from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import (
    unset_jwt_cookies,
    create_access_token,
    set_access_cookies,
    current_user,
    jwt_required,
    get_jwt_identity,
    get_jwt_header,
    get_jwt
)
from datetime import datetime, timedelta, timezone

auth_bp = Blueprint("auth", __name__)


# NOTE: using implicit cookie refresh scheme
# https://flask-jwt-extended.readthedocs.io/en/stable/refreshing_tokens/#implicit-refreshing-with-cookies


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    """
    name = request.json.get("name")
    password = request.json.get("password")
    email = request.json.get("email")
    user = User(name=name, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    # access_token = create_access_token(identity=user.name)
    # set_access_cookies(response, access_token)
    token = create_access_token(identity=user)
    return jsonify({"token": token}), 200


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user using cookies from frontend.
    """
    data = request.get_json()  # parse request JSON

    # Read relevant data from JSON.
    email = data.get("email")
    password = data.get("password")

    # Check database for a user with a matching email and password.
    user = User.query.filter_by(email=email).first()

    # Improved security: only compares and stores the password hash; never the password itself.
    if user and user.verify_password(password):
        # Generate two-week login token.
        token = create_access_token(identity=user)
        return jsonify(message="Login successful", token=token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Logout user
    """
    response = jsonify(message="Logged out")
    unset_jwt_cookies(response)
    return response, 200

@auth_bp.route("/test", methods=["GET"])
@jwt_required()
def this_is_a_test():
    """
    This method demonstrates that you can re-set the JWT cookie on-click.
    """
    return jsonify(message="OK"), 200


@auth_bp.route("/user", methods=["GET"])
@jwt_required()
def user():
    """
    Return current user.
    """
    if current_user:
        return jsonify(user=current_user.name)
    else:
        return jsonify(message="Not logged in"), 401

@auth_bp.errorhandler(Exception)
def print_error(e):
    print(request.headers, "\n", e)
    return {"message": "Something went wrong"}, 500
