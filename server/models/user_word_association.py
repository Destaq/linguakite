from extensions import db


class UserWord(db.Model):
    """
    This is an association object (NOTE: worth complexity point) that allows
    a many-to-many relationship between users and their words to have an additional
    column (user # of times word was seen).
    """

    __tablename__ = "user_word"

    user = db.relationship("User", back_populates="words")
    word = db.relationship("Word", back_populates="users")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"), primary_key=True)

    number_of_times_seen = db.Column(db.Integer, index=True, nullable=False)

    def __init__(self, user, word, number_of_times_seen):
        self.user_id = user.id
        self.word_id = word.id
        self.number_of_times_seen = number_of_times_seen
