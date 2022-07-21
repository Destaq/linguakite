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

vocab_bp = Blueprint("vocab", __name__)
