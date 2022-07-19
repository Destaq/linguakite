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
    get_jwt_header
)

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
    Login user
    """
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and user.verify_password(password):
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
