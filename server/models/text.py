import ast
import spacy
import re
import nltk
import math
import heapq

from extensions import db
from nltk.corpus import wordnet as wn
from nltk.probability import *
from string import punctuation
from models.word import Word

nlp = spacy.load("en_core_web_sm")

text_tag_association_table = db.Table(
    "text_tag_association",
    db.Column("text_id", db.Integer, db.ForeignKey("text.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


def fixed_lemmatize(content):
    # replace all 2x newlines with a space and a newline
    content = content.replace("\n\n", " \n").rstrip()

    output_content = []

    for word in re.split(" ", content):
        if word.isspace():
            # this means that there was a double space there
            pass
            # output_content.append(
            #     {
            #         "word": normal_split[i],
            #         "lemma": normal_split[i],  # a bit of a problem here, so we just use the word
            #     }
            # )
        elif len(word) > 0:
            # print("Word:", word)
            lemmas = nlp(word)
            lemma = lemmas[0].lemma_

            if set(word).issubset(set(larger_punctuation)) == False:
                i = 0
                while set(lemma).issubset(set(larger_punctuation)) and i < len(lemmas):
                    # this means e.g. (dog) was parsed to ( dog ), we need to get the WORD
                    lemma = lemmas[i].lemma_
                    i += 1
            

            output_content.append(
                {
                    "word": word,
                    "lemma": lemma,  # revert, just testing lookup speed (2x faster)
                }
            )
        
    # print(len(content.split(" ")), len(output_content))

    # print(content, end="\n\n")

    # for i in range(len(content.split(" "))):
    #     print(content.split(" ")[i])
    #     print(output_content[i], end="---\n")

    return " ".join([word["lemma"] for word in output_content])


# SYNONYMIZE HELPER FUNCTIONS

# https://stackoverflow.com/questions/63666191/using-wordnet-with-nltk-to-find-synonyms-that-make-sense
def get_synonyms(word, pos):
    for synset in wn.synsets(word, pos=pos2wordnetpos(pos)):
        for lemma in synset.lemmas():
            yield lemma.name()


def pos2wordnetpos(penntag):
    if penntag == "NNP":
        # this is a person, skip
        return ""
    morphy_tag = {"NN": wn.NOUN, "JJ": wn.ADJ, "VB": wn.VERB, "RB": wn.ADV}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return ""


def rankWrapper(synonym):
    lemma = nlp(synonym)[0].lemma_

    word = Word.query.filter_by(lemma=lemma).first()
    if word:
        return word.word_rank
    else:
        return 999_999


# END SYNONYMIZE HELPER FUNCTIONS

# SYNONYMIZE HELPER DATA
punctuation = list(punctuation)

punctuation.append("“")
punctuation.append("”")
punctuation.append("’")
punctuation.append("‘")
punctuation.append("\n")
punctuation.append("\"")
punctuation.append("\'")

larger_punctuation = punctuation[:]  # includes below

# and remove []() from punctuation
punctuation.remove("[")
punctuation.remove("]")
punctuation.remove("(")
punctuation.remove(")")

punctuation = "".join(punctuation)

# END SYNONYMIZE HELPER DATA

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

    # other lemmatizations and contents
    # the below really should be nullable = False, but it's too late for our DB
    summarized_content = db.Column(db.String, nullable=True)
    synonymized_content = db.Column(db.String, nullable=True)
    lemmatized_summarized_content = db.Column(db.String, nullable=True)
    lemmatized_synonymized_content = db.Column(db.String, nullable=True)

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

        try:
            authors = ast.literal_eval(
                authors
            )  # this is used for loading in directly from the files
        except:
            pass  # authors remains as authors
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
        self.unique_words = self.calculate_unique_words(self.lemmatized_content)
        self.difficulty = self.calculate_difficulty(
            self.unique_words,
            self.total_words,
            self.average_word_length,
            self.average_sentence_length,
        )
        self.synonymized_content = self.synonymize_content(content)
        self.summarized_content = self.summarize_content(content)
        (
            self.lemmatized_content,
            self.lemmatized_synonymized_content,
            self.lemmatized_summarized_content,
        ) = self.lemmatize_all_content(content)

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
            if (
                chunk_length > 1000
            ):  # NOTE: this is 1000 chars of content, excludes spaces
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

    def lemmatize_all_content(self, content):
        """
        Lemmatize the text, summarized text, and synonymized text.
        
        This is just used for calculating the percentage of words that are known and unique words, so no need to preserve punctuation. It is also used for updating words on click.
        """

        lemmatized_normal = fixed_lemmatize(content)
        lemmatized_synonyms = fixed_lemmatize(self.synonymized_content)
        lemmatized_summarized = fixed_lemmatize(self.summarized_content)

        return lemmatized_normal, lemmatized_synonyms, lemmatized_summarized  # NOTE: order matters

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


    def summarize_content(self, content):
        # split text into paragraphs
        paragraphs = re.split("\n\s*", content)
        paragraphs = [paragraph for paragraph in paragraphs if paragraph != ""]

        summary = ""
        CONDENSE_PARAGRAPH_FACTOR = 2

        for paragraph in paragraphs:
            sentence_list = nltk.sent_tokenize(paragraph)

            output_sentence_count = math.ceil(
                len(sentence_list) / CONDENSE_PARAGRAPH_FACTOR
            )
            stopwords = nltk.corpus.stopwords.words("english")

            word_frequencies = {}
            for word in nltk.word_tokenize(paragraph):
                if word not in stopwords:
                    if word not in word_frequencies.keys():
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
                if len(word_frequencies.values()) > 0:
                    maximum_frequency = max(word_frequencies.values())
                else:
                    maximum_frequency = 0

            for word in word_frequencies.keys():
                word_frequencies[word] = word_frequencies[word] / maximum_frequency

            sentence_scores = {}

            for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        # if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

            summary += (
                " ".join(
                    heapq.nlargest(
                        output_sentence_count, sentence_scores, key=sentence_scores.get
                    )
                )
                + "\n\n"
            )

        return summary


    def synonymize_content(self, content):
        paragraphs = re.split("\n\s*", content)
        paragraphs = [paragraph for paragraph in paragraphs if paragraph != ""]

        output_text = ""

        for paragraph in paragraphs:
            paragraph = nltk.word_tokenize(paragraph)

            for word, tag in nltk.pos_tag(paragraph):
                # Filter for unique synonyms not equal to word and sort.
                unique = sorted(
                    set(
                        synonym
                        for synonym in get_synonyms(word, tag)
                        if synonym != word
                        and synonym != word.lower()
                        and "_"
                        not in synonym  # exclude those multi-words as cannot be found in DB
                    )
                )

                # get the highest frequency synonym (aka easiest)
                if len(unique) > 0:
                    highest_freq_synonym = min(unique, key=lambda x: rankWrapper(x))
                    if rankWrapper(highest_freq_synonym) > rankWrapper(
                        word
                    ):  # more freq alternative
                        output_text += highest_freq_synonym + " "
                    else:
                        output_text += word + " "
                else:
                    output_text += word + " "

                if word in punctuation:
                    output_text = output_text[:-3] + word + " "

            output_text = output_text[:-1] + "\n\n"

        output_text = output_text[:-2]  # get rid of final newlines

        return output_text
