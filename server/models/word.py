from extensions import db

class Word(db.Model):
    __tablename__ = "word"

    id = db.Column(db.Integer, primary_key=True)
    lemma = db.Column(db.String(64), index=True, unique=True)  # lemmatized form of word, this should probably just be called lemma to be accurate
    lemma_rank = db.Column(db.Integer, nullable=False)  # how frequent (rank) this lemma is in the lemma frequency list (used for difficulty underlining). Total of 56276 from wiki-100k
    word_rank = db.Column(db.Integer)  # in the word frequency list, what is the frequency rank of the 1st word that lemmatizes to this?

    # NOTE: definition will be taken from https://dictionaryapi.dev/ without DB entry
    # NOTE: translation will be taken from https://www.deepl.com/pro-api?cta=header-pro-api/ without DB entry
    # the above two notes are only for when a single one is being clicked

    # for one we are grabbing multiple ones, where we don't care as much for the definition
    # then we will use some Python libraries

    users = db.relationship("UserWord", back_populates="word")

    def __init__(self, lemma, lemma_rank=60_000, word_rank=999_999):
        self.lemma = lemma  # the word is already inputted lemmatized via spacy. This is done because it means you can check in the other functions to see whether to place new words in Word + UserWord or just word.
        self.lemma_rank = lemma_rank  # 56 276 entries in pre-made lemma wordbank, 60k = any new words added will be added to the end of the list. Generic marker of *quite* unknown.
        self.word_rank = word_rank  # any user-added words to the Words table are assumed to be very difficult, as they aren't present in the first 100k

        # going over the logic to make it easier for myself:
        # a word is added as a lemma here, and Word is a false friend name
        # this means that lemma_rank is the only important thing to check for when checking difficulty
        # word_rank ONLY serves to establish a base vocabulary

    def __repr__(self):
        return f"<Word (lemmatized form): {self.lemma}>"
