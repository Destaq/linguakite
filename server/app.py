from flask import Flask
from extensions import db, jwt
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_cors import CORS
import os
from models.user import *
from datetime import timedelta, datetime, timezone
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    set_access_cookies,
    get_jwt
)

# import blueprints
from blueprints.auth import auth_bp
from blueprints.vocab import vocab_bp
from blueprints.textbank import textbank_bp

# other imports for flask-migrate
from models.user import User
from models.word import Word
from models.text import Text
from models.tag import Tag
from models.log import Log

from models.associations.user_word import UserWord
from models.associations.user_text import UserText
from models.text import text_tag_association_table

load_dotenv()

migrate = Migrate(compare_type=True)
cors = CORS()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get("APP_SETTINGS"))
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/*": {"origins": r"*"}},
        supports_credentials=True,
    )

    # to use current_user
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        if type(user) is not int:
            return user.id
        else:
            return User.query.filter_by(id=user).one_or_none().id

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    # cookie scheme auto-refresh
    # NOTE: mention for my post; complexity point
    @app.after_request
    def refresh_expiring_jwts(response):
        """
        Here we are supporting the implicit cookie refresh mechanism.

        If a not-yet-expired access cookie (token) is sent with a request, it will be replaced
        with one that is newly created, also for two weeks.

        (Note that this will not work just by opening the app, the user also needs to do some actions).
        """
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(days=7))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                access_token = "Bearer " + access_token
                response.set_cookie("auth._token.cookie", access_token, samesite="None", secure=True)  # latter two required to actually set 
                # set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError) as e:
            # Case where there is not a valid JWT. Just return the original respone
            return response
        

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(vocab_bp, url_prefix="/api")
    app.register_blueprint(textbank_bp, url_prefix="/api")
    return app
