from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    words = db.relationship("UserWord", back_populates="user")
    texts = db.relationship("UserText", back_populates="user")
    logs = db.relationship("Log", back_populates="user")

    quizzes_done = db.Column(db.Integer, default=0)  # used for statistics
    goal_length_minutes = db.Column(db.Integer, default=15)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
