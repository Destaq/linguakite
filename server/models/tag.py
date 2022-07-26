from extensions import db


class Tag(db.Model):
    """
    Holds tags from the article, either those from Medium or those from the user.
    """
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    texts = db.relationship("TextTag", back_populates="tag")

    def __init__(self, name):
        self.name = name
