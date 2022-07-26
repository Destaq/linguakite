from extensions import db
from models.text import text_tag_association_table

class Tag(db.Model):
    """
    Holds tags from the article, either those from Medium or those from the user.
    """
    __tablename__ = "tag"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)

    texts = db.relationship("Text", secondary=text_tag_association_table, back_populates="tags")

    def __init__(self, name):
        self.name = name
