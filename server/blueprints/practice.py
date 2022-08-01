import re
import random
import nltk

from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.text import Text
from models.associations.user_text import UserText
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from string import punctuation

from flask_jwt_extended import jwt_required, current_user

# we are generating four types of questions

# 1. Multiple Choice (via synonyms)
# 2. Arrange sentences
# 3. Arrange words
# 4. Define (and manually compare)

lem = WordNetLemmatizer()
practice_bp = Blueprint("practice", __name__)


def order_puzzler(inp_type, text, default_elements):

    text = re.findall(".*?[.!\?]", text)
    text = [s.strip() for s in text]

    if inp_type == "Order Words":
        choice = random.choice(text)
        text = choice.split()

    ELEMENTS_TO_TAKE = default_elements if len(text) >= default_elements else len(text)
    ELEMENT_STARTING_INDEX = random.randint(0, len(text) - ELEMENTS_TO_TAKE) - 1

    # take said random number of sentences and shuffle
    preserved = text[ELEMENT_STARTING_INDEX : ELEMENT_STARTING_INDEX + ELEMENTS_TO_TAKE]
    shuffled = preserved.copy()
    random.shuffle(shuffled)

    if len(shuffled) == 0:
        return None

    if inp_type == "Order Words":
        context = " ".join(
            text[:ELEMENT_STARTING_INDEX]
            + [" ... "]
            + text[ELEMENT_STARTING_INDEX + ELEMENTS_TO_TAKE :]
        )
    else:
        context = None

    # now return the order of shuffled elements in the order of preserved elements
    answer = ""
    for e in preserved:
        answer += str(shuffled.index(e) + 1)

    output = {
        "type": inp_type,
        "question": shuffled,
        "answer": answer,
        "context": context,
    }


    return output


# cloze puzzler helper
def get_synonyms(word, pos):
    pos = pos2wordnetpos(pos)
    if pos != "":  # don't want synonyms for the etc.
        synset_output = wn.synsets(word, pos=pos)
        synonyms = [synonym.name().split(".")[0] for synonym in synset_output]
        # replace _ in synonym with " "
        synonyms = [synonym.replace("_", " ") for synonym in synonyms]
        return synonyms
    else:
        return []


# cloze puzzler helper
def pos2wordnetpos(penntag):
    if penntag == "NNP":
        # this is a person, skip
        return ""
    morphy_tag = {"NN": wn.NOUN, "JJ": wn.ADJ, "VB": wn.VERB, "RB": wn.ADV}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return ""


def define_puzzler(text):
    text = re.findall(".*?[.!\?]", text)
    text = [s.strip() for s in text]

    chosen_sentence = random.choice(text)

    words = nltk.word_tokenize(chosen_sentence)
    words = nltk.pos_tag(words)

    words = [word for word in words if word[0] not in punctuation]

    try:
        random_index = random.randint(0, len(words) - 1)
    except ValueError:
        return None

    word, tag = words[random_index]

    try:
        definition = wn.synsets(word, pos2wordnetpos(tag))[0].definition()
    except IndexError:
        definition = "Unavailable, confer your dictionary."

    return {
        "type": "Define",
        "question": f"Define '{word}' in the context: \"{chosen_sentence}\"",
        "answer": definition,
    }


def cloze_puzzler(text):
    # pick a random sentence
    text = re.findall(".*?[.!\?]", text)
    text = [s.strip() for s in text]
    choice = random.choice(text)

    # word_tokenize the choice
    words = nltk.word_tokenize(choice)
    words = nltk.pos_tag(words)

    found_potential = False
    i = 0
    chosen_word_answer = None

    while not found_potential and i < len(words):
        word, tag = words[i]
        chosen_word_answer = lem.lemmatize(word.lower())

        synonyms = get_synonyms(word, tag)
        synonyms = [lem.lemmatize(synonym.lower()) for synonym in synonyms]
        synonyms = list(set(synonyms))

        options = []

        if chosen_word_answer in synonyms:
            synonyms.remove(chosen_word_answer)

        if len(synonyms) > 2:  # at least three options
            options = synonyms
            random.shuffle(options)
            options.append(chosen_word_answer)
            found_potential = True

        i += 1

    if not found_potential:
        return None  # will lead to this being called again, as a while loop
    else:
        if len(options) > 4:
            options = options[-4:]
        question = (
            " ".join([word[0] for word in words[: i - 1]])
            + " _____ "
            + " ".join([word[0] for word in words[i:]])
        )

        # if we have any floating punctuation, connect it to the word before it with regex
        # for example, 'by two mathematicians , Stuart Haber and W. Jones' -> 'by two mathematicians, Stuart Haber and W. Jones'
        # so essentially finding floating dots and commas
        question = re.sub(r"\s([',.;?!’]\s)", r"\1", question)
        question = re.sub(r"\’ \s(\S)", r"’\1", question)

        return {
            "type": "Multiple Choice",
            "question": question,
            "options": options,
            "answer": chosen_word_answer,
        }


# https://stackoverflow.com/a/33583008/12876940
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only


def get_optimized_random_text():
    return (
        Text.query.options(load_only("id"))
        .offset(func.floor(func.random() * db.session.query(func.count(Text.id))))
        .limit(1)
        .first()
    )


@practice_bp.route("get-user-library", methods=["GET"])
@jwt_required()
def get_user_library():

    # get all the texts from the UserTexts where the user is the current user and the text has not been finished
    library = (
        UserText.query.filter_by(user_id=current_user.id)
        .filter(UserText.current_page < UserText.total_pages)
        .all()
    )

    # get the text ids and titles from the library
    library = [
        {
            "id": text.text_id,
            "title": text.text.title,
        }
        for text in library
    ]

    return jsonify(user_library=library)


@practice_bp.route("/fetch-quiz", methods=["POST"])
@jwt_required()
def make_n_puzzles():
    puzzles = []

    text_id = request.json["text_id"]
    input_types = request.json["input_types"]
    n = int(request.json["n"])

    if text_id == -1:
        # fetch random puzzle
        text = get_optimized_random_text()
    else:
        text = Text.query.filter_by(id=text_id).first()

    text = text.content

    while len(puzzles) < n:
        puzzle_type = random.choice(input_types)
        if puzzle_type == "Multiple Choice":
            out = cloze_puzzler(text)
            if out is not None:
                puzzles.append(out)
        elif puzzle_type == "Order Words":
            out = order_puzzler(puzzle_type, text, 6)
            if out is not None:
                puzzles.append(out)
        elif puzzle_type == "Order Sentences":
            out = order_puzzler(puzzle_type, text, 4)
            if out is not None:
                puzzles.append(out)
        elif puzzle_type == "Define":
            out = define_puzzler(text)
            if out is not None:
                puzzles.append(out)

    return jsonify(puzzles=puzzles)
