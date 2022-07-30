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

    total_pages = db.Column(db.Integer, index=True, nullable=False)
    current_page = db.Column(db.Integer, index=True, nullable=False)
    # used to calculate percentage progress
    # percentage calculation = current_page/total_pages * 100

    def __init__(self, user_id, text_id, current_page, total_pages):
        self.user_id = user_id
        self.text_id = text_id
        # total pages is already an attribute of the text
        self.total_pages = total_pages
        self.current_page = current_page
