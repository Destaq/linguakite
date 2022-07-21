from extensions import db

class Word(db.Model):
    __tablename__ = "word"

    id = db.Column(db.Integer, primary_key=True)
    lemma = db.Column(db.String(64), index=True, unique=True)
    definition = db.Column(db.String(512), nullable=False)
    translation = db.Column(db.String(128), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)

    users = db.relationship("UserWord", back_populates="word")

    def __init__(self, word):
        self.lemma = None  # you lemmatize the word via spaCy
        self.definition = None  # this is calculated here
        self.translation = None  # this is calculated here
        self.frequency = None  # this is calculated here

    def __repr__(self):
        return f"<Word (lemmatized form): {self.lemma}>"
