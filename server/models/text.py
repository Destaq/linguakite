from extensions import db
import ast
import spacy
import string

nlp = spacy.load("en_core_web_sm")

text_tag_association_table = db.Table(
    "text_tag_association",
    db.Column("text_id", db.Integer, db.ForeignKey("text.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Text(db.Model):
    """
    A class that stores details about all texts in the database, including private texts.

    However, the texts will actually be accessed through the UserText Association Object once more, as there is an additional property (page_progress, which is then used to calculate normal progress ~> the final 'finished' button updates pages > # of pages, and hence means it was completed).

    (Everything is sent to the client, but # words as function of characters is calculated by both).

    Will only be using the Medium articles.
    """

    __tablename__ = "text"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, index=True)
    content = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=True)
    authors = db.Column(db.String, nullable=True)  # just concatenate the list of names
    date = db.Column(db.DateTime, nullable=True)

    # now the 'special' details
    total_pages = db.Column(
        db.Integer, nullable=False
    )  # this is calculated using math logic from text size
    unique_words = db.Column(db.Integer, nullable=False)
    average_sentence_length = db.Column(db.Float, nullable=False)
    average_word_length = db.Column(db.Float, nullable=False)
    lemmatized_content = db.Column(
        db.String, nullable=False
    )  # used for 'percentage words/content known'
    total_words = db.Column(db.Integer, nullable=False)

    difficulty = db.Column(
        db.Float, nullable=True
    )  # only bc. of the migration when there were already texts in the db

    # finally we have tags, which have a many-many relationship to this model
    tags = db.relationship(
        "Tag", secondary=text_tag_association_table, back_populates="texts"
    )
    users = db.relationship("UserText", back_populates="text")

    def __init__(self, title, content, url, authors, date):
        self.title = title
        self.content = content
        self.url = url
        self.date = date

        authors = ast.literal_eval(authors)
        # now we have a list of author names, let's convert it to a string
        # using appropriate English grammar
        if len(authors) == 1:
            self.authors = authors[0]
        elif len(authors) == 2:
            self.authors = "{} and {}".format(authors[0], authors[1])
        elif len(authors) > 2:
            self.authors = "{}, and {}".format(", ".join(authors[:-1]), authors[-1])

        # now the 'special' details
        self.total_pages = self.calculate_total_pages(content)
        self.average_sentence_length = self.calculate_average_sentence_length(content)
        self.average_word_length = self.calculate_average_word_length(content)
        self.total_words = len(content.split())
        self.lemmatized_content = self.lemmatize_content(content)
        self.unique_words = self.calculate_unique_words(self.lemmatized_content)
        self.difficulty = self.calculate_difficulty(
            self.unique_words,
            self.total_words,
            self.average_word_length,
            self.average_sentence_length,
        )

    def calculate_total_pages(self, content):
        """
        Each one of these will equate to one page on the screen.

        User will have to click buttons to go between pages.

        Same logic is used client-side.

        The logic here is: divide text into chunks where each chunk has
        just that number of words that reach 1000 characters or cross it
        over by one.
        """

        # first of all, split the text into words
        words = content.split()

        # now create the chunks
        chunk_count = 0
        chunk = ""
        chunk_length = 0
        for word in words:
            chunk_length += len(word)
            if chunk_length > 1000:
                chunk += word
                chunk_count += 1
                chunk = ""
                chunk_length = 0
            else:
                chunk += word

        # append final chunk if not empty
        if chunk:
            chunk_count += 1

        return chunk_count

    def calculate_average_sentence_length(self, content):
        """
        Calculate the average sentence length.
        """

        # first of all, split the text into sentences
        sentences = content.split(". ")

        # now calculate the average sentence length
        total_length = 0
        for sentence in sentences:
            total_length += len(sentence)

        return total_length / len(sentences)

    def calculate_average_word_length(self, content):
        """
        Calculate the average word length.
        """

        # first of all, split the text into words
        words = content.split()

        # now calculate the average word length
        total_length = 0
        for word in words:
            total_length += len(word)

        return total_length / len(words)

    def lemmatize_content(self, content):
        """
        Lemmatize the text. This is just used for calculating the percentage of words that are known and unique words, so no need to preserve punctuation.
        """

        # lemmatize the words
        lemmatized_text = nlp(content)
        final_text = ""
        for word in lemmatized_text:
            if word.lemma_ not in string.punctuation and word.lemma_.isspace() == False:
                final_text += word.lemma_ + " "

        print(final_text)

        return final_text

    def calculate_unique_words(self, lemmatized_content):
        # first of all, split the text into words
        words = lemmatized_content.split()

        # now create the chunks
        unique_words = set()
        for word in words:
            unique_words.add(word)

        return len(unique_words)

    def calculate_difficulty(
        self, unique_words, total_words, average_word_length, average_sentence_length
    ):
        return (
            unique_words
            / total_words
            * average_word_length
            * (average_sentence_length ** 0.1)
        )
