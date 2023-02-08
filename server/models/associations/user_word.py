from extensions import db


class UserWord(db.Model):
    """
    This is an association table that allows a many-to-many relationship between users
    and their words, and allows for an additional column (# of times word was seen by
    a specific user).

    Each entry represents a word that a user knows. One user can have many words, and
    one word can be known by many users.
    """

    __tablename__ = "user_word"  # generated Postgres table name

    user = db.relationship("User", back_populates="words")
    word = db.relationship("Word", back_populates="users")

    # `user_id` and `word_id` form a composite primary key.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey("word.id"), primary_key=True)

    # Keeps track of how many times a user has seen a word.
    number_of_times_seen = db.Column(db.Integer, index=True, nullable=False)

    def __init__(self, user_id, word_id, number_of_times_seen):
        """
        A constructor method for a new word-user association object.
        """
        self.user_id = user_id
        self.word_id = word_id
        self.number_of_times_seen = number_of_times_seen
