from extensions import db


class TextTag(db.Model):
    """
    Association object between texts and tags.
    """

    __tablename__ = "text_tag"

    text = db.relationship("Text", back_populates="texts")
    tag = db.relationship("Tag", back_populates="tags")

    text_id = db.Column(db.Integer, db.ForeignKey("text.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)

    def __init__(self, text_id, tag_id):
        self.text_id = text_id
        self.tag_id = tag_id
