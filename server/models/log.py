from extensions import db


class Log(db.Model):
    """
    Tracks the user's daily reading times.
    """
    __tablename__ = "log"

    id = db.Column(db.Integer, primary_key=True)
    elapsed_time_seconds = db.Column(db.Integer, index=True, nullable=True)
    date = db.Column(db.DateTime, index=True, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user = db.relationship("User", back_populates="logs")

    def __init__(self, user, date, elapsed_time_seconds):
        self.user = user
        self.date = date
        self.elapsed_time_seconds = elapsed_time_seconds
