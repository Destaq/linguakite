import spacy
import deepl
import ast
import os
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.word import Word
from models.associations.user_word import UserWord
from flask_jwt_extended import (
    unset_jwt_cookies,
    create_access_token,
    set_access_cookies,
    current_user,
    jwt_required,
    get_jwt_identity,
    get_jwt_header,
    get_jwt,
)

load_dotenv()

translator = deepl.Translator(
    os.environ.get("DEEPL_API_KEY"),
)

nlp = spacy.load("en_core_web_sm")
vocab_bp = Blueprint("vocab", __name__)


def lemmatize(word):
    return nlp(word)[0].lemma_


@vocab_bp.route("/update-vocab-estimate", methods=["POST"])
@jwt_required()
def estimate_vocab_from_frequency():
    """
    Post request contains `vocab_size`, an integer parameter of the user's vocab size. Word lemmas from the first N most frequent words in a frequency list are then added to their wordbank.
    """
    vocab_size = int(request.json.get("vocab_size"))

    # select all words from Word where the word_rank is equal to or below vocab_size
    words = Word.query.filter(Word.word_rank <= vocab_size).all()

    # add all words to the user's wordbank
    for word in words:
        # check if the user already has the word in their wordbank
        if (
            UserWord.query.filter_by(user_id=current_user.id, word_id=word.id).first()
            is None
        ):
            # if not, add it
            user_word = UserWord(
                user_id=current_user.id, word_id=word.id, number_of_times_seen=0
            )
            db.session.add(user_word)
            db.session.commit()
        else:
            # if they do, do nothing
            pass

    return jsonify({"success": True})


@vocab_bp.route("/upload-vocab-file", methods=["POST"])
@jwt_required()
def update_vocab_from_file():
    """
    Updates user wordbank from a `.txt` file of newline-separated English words.
    """

    file = request.files["file"]

    # read newline-separated words from file into list
    words = file.read().decode("utf-8").split("\n")
    words = [lemmatize(word) for word in words]

    # for each word in words
    for word in words:
        # lemmatize the word

        # check for word lemma in Word DB
        if Word.query.filter_by(lemma=word).first() is None:
            # if not, add it
            new_word = Word(
                lemma=word
            )  # with maximally high = low lemma_rank and word_rank by default
            db.session.add(new_word)
        else:
            new_word = Word.query.filter_by(lemma=word).first()

    db.session.commit()

    # then create association between word and user
    # doing this outside of the loop because otherwise can't link new ones
    for word in words:
        # check if the user already has the word in their wordbank
        if (
            UserWord.query.filter_by(
                user_id=current_user.id, word_id=new_word.id
            ).first()
            is None
        ):
            # if not, add it
            user_word = UserWord(
                user_id=current_user.id, word_id=new_word.id, number_of_times_seen=0
            )
            db.session.add(user_word)
            db.session.commit()
        else:
            # if they do, do nothing
            pass

    return jsonify({"success": True})


# there will also be a route to upload an individual word
# which is done by clicking in the `/read` page
@vocab_bp.route("/manage-individual-word", methods=["POST"])
@jwt_required()
def manage_single_word():
    """
    A word can be toggled as known (in UserWord Association) or not known (not in it) via click.
    """

    lemma = lemmatize(request.json.get("lemma"))  # don't forget to always lemmatize!

    # check if the user already has the word in their wordbank
    # should it not be...
    if UserWord.query.filter_by(user_id=current_user.id, lemma=lemma).first() is None:

        # it could either not exist
        if Word.query.filter_by(lemma=lemma).first() is None:
            new_word = Word(lemma=lemma)
            db.session.add(new_word)
            db.session.commit()

        # or it could exist but not be associated with the user
        else:
            new_word = Word.query.filter_by(lemma=lemma).first()

            # create association
            user_word = UserWord(
                user_id=current_user.id, word_id=new_word.id, number_of_times_seen=0
            )
            db.session.add(user_word)
            db.session.commit()

    # if it is...
    else:
        # delete association
        word = Word.query.filter_by(lemma=lemma).first()
        user_word = UserWord.query.filter_by(
            user_id=current_user.id, word_id=word.id
        ).first()
        db.session.delete(user_word)
        db.session.commit()

    return jsonify({"success": True})


@vocab_bp.route("/delete-word", methods=["DELETE"])
@jwt_required()
def delete_word():
    """
    Deletes a word (lemma) from the UserWord AssociationObject table, so that it appears that the user no longer knows that word (although it will remain in the Word table).

    This is already in the lemmatized form so no need to lemmatize the input.

    This is for the /wordbank route and the delete icon.
    """
    dict_str = request.data.decode("utf-8")
    data = ast.literal_eval(dict_str)

    lemma = data["lemma"]

    word = Word.query.filter_by(lemma=lemma).first()
    word_association = UserWord.query.filter_by(
        user_id=current_user.id, word_id=word.id
    ).first()

    if word is None or word_association is None:  # non-existence, client messed around
        return (
            jsonify(
                {"success": False, "message": "Word does not exist in user wordbank."}
            ),
            400,
        )

    db.session.delete(word_association)
    db.session.commit()

    return jsonify({"success": True})


@vocab_bp.route("/fetch-wordbank", methods=["GET"])
@jwt_required()
def fetch_wordbank():
    """
    This function will return 20 of the user's known words, in alphabetical order.

    The 'page' param will show where to start from, as the user might not want to explicitly see the first 20 words.
    """
    page = request.args.get("page")
    if page is None:
        page = 0
    else:
        page = int(page) - 1

    # get all words in user's wordbank by using only the User class
    user_words = User.query.filter_by(id=current_user.id).first().words

    user_words = [
        {
            "lemma": user_word.word.lemma,
            "number_of_times_seen": user_word.number_of_times_seen,
            "word_rank": user_word.word.word_rank,
            "lemma_rank": user_word.word.lemma_rank,
        }
        for user_word in user_words
    ]

    # get all words in user's wordbank, in alphabetical order
    user_words = sorted(user_words, key=lambda x: x["lemma"].lower())

    # add an index to each word in user_words based on its position in the list
    for i, word in enumerate(user_words):
        word["index"] = i
    
    total_elements = len(user_words)

    # get the words at indexes between (inclusive at start)
    # page * 20 - (page + 1) * 20
    user_words = user_words[page * 20 : (page + 1) * 20]


    words_for_dict = [word["lemma"] for word in user_words]

    translations = translator.translate_text(
        words_for_dict, target_lang="zh", source_lang="en"
    )

    for i in range(len(user_words)):
        if translations[i].text != user_words[i]["lemma"] and translations[i].text != "":
            user_words[i]["translation"] = translations[i].text
        else:
            user_words[i]["translation"] = "N/A"


    # return success message + data
    return jsonify({"success": True, "words": user_words, "total_elements": total_elements})



# this is a one-off function that will be used to update the database
# and then later commented out
import csv
import ast
from models.tag import Tag
from models.text import Text, text_tag_association_table

@vocab_bp.route("/update-database-with-medium", methods=["GET"])
def update_db_with_medium():
    with open("/Users/simonilincev/Desktop/School/IA/CS/Code/linguakite/server/data/medium_articles.csv") as file:
        reader = csv.reader(file)
        i = 1
        for row in reader:
            print(f"{i:06d}" + " ----- ", end="\r")
            if row[0] == "title":
                # skip the first line
                continue
            else:
                text = Text(title=row[0], content=row[1], url=row[2], authors=row[3], date=row[4])
                db.session.add(text)
                db.session.commit()
                tags = ast.literal_eval(row[5])

                for tag in tags:
                    # check if tag in db already
                    if Tag.query.filter_by(name=tag).first() is None:
                        tag_link = Tag(name=tag)
                        db.session.add(tag_link)
                        db.session.commit()
                    else:
                        tag_link = Tag.query.filter_by(name=tag).first()

                    # now add them as relevant tags and texts to each other
                    tag_link.texts.append(text)
                    text.tags.append(tag_link)
                    db.session.commit()

            i += 1
        
        print("\n")
        return jsonify({"success": True})
