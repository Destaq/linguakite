from extensions import db


class UserText(db.Model):
    """
    Association object between users and texts.
    """

    __tablename__ = "user_text"

    user = db.relationship("User", back_populates="texts")
    text = db.relationship("Text", back_populates="users")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    text_id = db.Column(db.Integer, db.ForeignKey("text.id"), primary_key=True)

    current_page = db.Column(db.Integer, index=True, nullable=False)  # 0 = not started, X/Y = finished X pages out of Y (so calculate percentage), (Y + 1) / Y = completed
    # percentage is always calculated as (current - 1) / Y, because e.g. opening book does not mean that they read to the bottom of it

    def __init__(self, user_id, text_id, current_page=0):  # val of 0 means not started
        self.user_id = user_id
        self.text_id = text_id
        # total pages is already an attribute of the text
        self.current_page = current_page
