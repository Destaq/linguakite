from extensions import db
import ast
import spacy
import string

nlp = spacy.load("en_core_web_sm")


class Text(db.Model):
    """
    A class that stores details about all texts in the database, including private texts.

    However, the texts will actually be accessed through the UserText Association Object once more, as there is an additional property (page_progress, which is then used to calculate normal progress ~> the final 'finished' button updates pages > # of pages, and hence means it was completed).

    (Everything is sent to the client, but # words as function of characters is calculated by both).

    Will only be using the Medium articles.
    """

    __tablename__ = "text"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=True, unique=True)
    text = db.Column(db.String, nullable=False)
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
    lemmatized_text = db.Column(
        db.String, nullable=False
    )  # used for 'percentage words/content known'
    total_words = db.Column(db.Integer, nullable=False)

    # finally we have tags, which have a many-many relationship to this model
    tags = db.relationship("TextTag", back_populates="text")
    users = db.relationship("UserText", back_populates="text")

    def __init__(self, title, text, url, authors, date):
        self.title = title
        self.text = text
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
        self.total_pages = self.calculate_total_pages(text)
        self.average_sentence_length = self.calculate_average_sentence_length(
            text
        )
        self.average_word_length = self.calculate_average_word_length(text)
        self.total_words = len(text.split())
        self.lemmatized_text = self.lemmatize_text(text)
        self.unique_words = self.calculate_unique_words(self.lemmatized_text)

    def calculate_total_pages(self, text):
        """
        Each one of these will equate to one page on the screen.

        User will have to click buttons to go between pages.

        Same logic is used client-side.

        The logic here is: divide text into chunks where each chunk has
        just that number of words that reach 1000 characters or cross it
        over by one.
        """

        # first of all, split the text into words
        words = text.split()

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

    def calculate_average_sentence_length(self, text):
        """
        Calculate the average sentence length.
        """

        # first of all, split the text into sentences
        sentences = text.split(". ")

        # now calculate the average sentence length
        total_length = 0
        for sentence in sentences:
            total_length += len(sentence)

        return total_length / len(sentences)

    def calculate_average_word_length(self, text):
        """
        Calculate the average word length.
        """

        # first of all, split the text into words
        words = text.split()

        # now calculate the average word length
        total_length = 0
        for word in words:
            total_length += len(word)

        return total_length / len(words)

    def lemmatize_text(self, text):
        """
        Lemmatize the text. This is just used for calculating the percentage of words that are known and unique words, so no need to preserve punctuation.
        """

        # lemmatize the words
        lemmatized_text = nlp(text)
        final_text = ""
        for word in lemmatized_text:
            if word.lemma_ not in string.punctuation and word.lemma_.isspace() == False:
                final_text += word.lemma_ + " "

        return final_text

    def calculate_unique_words(self, lemmatized_text):
        # first of all, split the text into words
        words = lemmatized_text.split()

        # now create the chunks
        unique_words = set()
        for word in words:
            unique_words.add(word)

        return len(unique_words)
