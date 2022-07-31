import spacy
import re
import deepl
import os

from typing import Text
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.tag import Tag
from models.word import Word
from models.log import Log
from models.text import Text
from models.associations.user_word import UserWord
from models.associations.user_text import UserText
from flask_jwt_extended import (
    current_user,
    jwt_required,
)
from sqlalchemy import func
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv


load_dotenv()

translator = deepl.Translator(
    os.environ.get("DEEPL_API_KEY"),
)

nlp = spacy.load('en_core_web_sm')


textbank_bp = Blueprint("textbank", __name__)

# two routes in databasetable + one route for adding custom file
@textbank_bp.route("/fetch-textbank", methods=["GET"])
def fetch_textbank():
    titleSearchString = request.args.get("titleSearchString")
    if titleSearchString is None:
        titleSearchString = ""
    difficultyType = request.args.get("difficultyType")
    minWordLength = request.args.get("minWordLength")
    maxWordLength = request.args.get("maxWordLength")
    tags = request.args.getlist("tags[]")
    usedIds = request.args.getlist("usedIds[]")
    and_or_or = request.args.get(
        "and_or_or"
    )  # whether a matching row has to have ALL tags listed (and) or ANY tag listed (or)

    if and_or_or == "and":
        # all rows must have ALL tags listed in tags
        rows = Text.query.filter(
            Text.title.ilike("%" + titleSearchString + "%")
            & (Text.total_words >= minWordLength)
            & (Text.total_words <= maxWordLength)
            & (Text.id.notin_(usedIds))
        )
        for tag in tags:
            rows = rows.filter(Text.tags.any(Tag.name.in_([tag])))

    elif and_or_or == "or":
        # find rows that fit the above criteria
        rows = Text.query.filter(
            Text.title.ilike("%" + titleSearchString + "%")
            & (Text.total_words >= minWordLength)
            & (Text.total_words <= maxWordLength)
            & (Text.id.notin_(usedIds))
        )
        if tags != [] and tags != [""]:
            rows = rows.filter(Text.tags.any(Tag.name.in_(tags)))

    # import csv
    # # let's do some exploratory data analysis, write to a csv file
    # with open("textbank.csv", "w") as csv_file:
    #     writer = csv.writer(csv_file)
    #     writer.writerow(["unique_words", "total_words", "average_word_length", "average_sentence_length", "charcount", "lemmatized_content"])
    #     for row in rows:
    #         writer.writerow(
    #             [
    #                 row.unique_words,
    #                 row.total_words,
    #                 row.average_word_length,
    #                 row.average_sentence_length,
    #                 len(row.content),
    #                 row.lemmatized_content[:1000],
    #             ]
    #         )

    # ---------------------- #

    # def calculate_difficulty(row):
    #     return (
    #         row.unique_words
    #         / row.total_words
    #         * row.average_word_length
    #         * (row.average_sentence_length ** 0.1)
    #     )

    # # data analysis done, now let's update the database
    # # select all texts
    # update_rows = Text.query.all()
    # for row in update_rows:
    #     row.difficulty = calculate_difficulty(row)
    #     db.session.add(row)

    # # commit the changes to the database
    # db.session.commit()

    # ---------------------- #

    # just dividing into 5 equally sized quintiles based off the difficulty calculating algorithm
    if difficultyType == "Very Easy":
        rows = rows.filter(Text.difficulty <= 2.67)
    elif difficultyType == "Easy":
        rows = rows.filter(Text.difficulty > 2.67).filter(Text.difficulty <= 3.19)
    elif difficultyType == "Medium":
        rows = rows.filter(Text.difficulty > 3.19).filter(Text.difficulty <= 3.71)
    elif difficultyType == "Hard":
        rows = rows.filter(Text.difficulty > 3.71).filter(Text.difficulty <= 4.53)
    elif difficultyType == "Very Hard":
        rows = rows.filter(Text.difficulty > 4.53)

    ## the below takes too much time, use for individual clicks
    ## but for the actual difficulty — just an estimate from the textbank
    # knowns = []
    # for row in rows:
    #     lemma_counter = Counter(row.lemmatized_content.split(" "))
    #     user_words = User.query.filter_by(id=current_user.id).first().words
    #     user_words = [word.word.lemma for word in user_words]
    #     total_known_words = 0

    #     # calculate percentage known of total lemma content
    #     for user_known_word in user_words:
    #         if user_known_word in lemma_counter:
    #             total_known_words += lemma_counter[user_known_word]

    #     knowns.append(sum(lemma_counter.values()) / row.total_words)

    rows = rows.order_by(func.random()).limit(10)

    return jsonify(
        texts=[
            {
                "id": row.id,
                "title": row.title,
                "content_preview": row.content[:200] + "...",
                "tags": [tag.name for tag in row.tags],
            }
            for row in rows
        ]
    )


@textbank_bp.route("/fetch-text-details", methods=["GET"])
@jwt_required()
def fetch_specific_details():
    text_id = request.args.get("id")

    # get the text
    text = Text.query.filter_by(id=text_id).first()

    return jsonify(
        textDetails={
            "id": text.id,
            "title": text.title,
            "bigContentPreview": text.content[:997] + "...",
            "url": text.url,
            "authors": text.authors,
            # format date to just show day, month, year
            "date": text.date.strftime("%d %b %Y"),
            "unique_words": round(text.unique_words, 3),
            "total_words": text.total_words,
            "average_sentence_length": round(text.average_sentence_length, 3),
            "average_word_length": round(text.average_word_length, 3),
            "percentage_known": None,
        }
    )


@textbank_bp.route("/assess-comprehension", methods=["GET"])
@jwt_required()
def assess_comprehension():
    """
    This function calculates a user's % understanding of a text, and is called
    later as it can take some time for large wordbanks.
    """
    text_id = request.args.get("id")
    text = Text.query.filter_by(id=text_id).first()

    lemma_counter = Counter(text.lemmatized_content.split(" "))
    user_words = User.query.filter_by(id=current_user.id).first().words
    user_words = [word.word.lemma for word in user_words]
    total_known_words = 0

    # calculate percentage known of total lemma content
    for user_known_word in user_words:
        if user_known_word in lemma_counter:
            total_known_words += lemma_counter[user_known_word]

    percentage_known = total_known_words / sum(lemma_counter.values()) * 100

    return jsonify(percentage_known=round(percentage_known, 3))


@textbank_bp.route("/read-text", methods=["GET"])
@jwt_required()
def read_text():
    text_id = request.args.get("id")
    content_type = request.args.get("type")

    # get the text
    text = Text.query.filter_by(id=text_id).first()

    if content_type == "Original Text":
        content = text.content
        lemmatized_content = text.lemmatized_content
    elif content_type == "Synonymized Text":
        content = text.synonymized_text
        lemmatized_content = text.lemmatized_synonymized_content
    elif content_type == "Summarized Content":
        content = text.summarized_content
        lemmatized_content = text.lemmatized_summarized_content

    # replace all 2x newlines with a space and a newline
    content = content.replace("\n\n", " \n")
    content = re.split(" ", content)
    lemmatized_content = re.split(" ", lemmatized_content)  # no newlines here by default


    output_content = []
    for i in range(len(content)):
        word = content[i]
        lemma = lemmatized_content[i]

        if len(word) > 0:
            lemma_ob = Word.query.filter_by(lemma=lemma).first()
            
            known = False
            rank = 60_000

            if lemma_ob != None:
                rank = lemma_ob.lemma_rank
                if UserWord.query.filter_by(user_id=current_user.id, word_id=lemma_ob.id).first() != None:
                    known = True

            output_content.append(
                {
                    "word": word,
                    "lemma": lemma,
                    "known": known,
                    "rank": rank,
                }
            )

    history_match = UserText.query.filter_by(user_id=current_user.id, text_id=text_id).first()
    if history_match:
        # the user is already somewhat through the text, they get pushed to that page
        start_page = history_match.current_page + 1
    else:
        # the user is not yet through the text, they get pushed to the first page
        start_page = 1

    return jsonify(title=text.title, content=output_content, start_page=start_page)


@textbank_bp.route("/add-private-text", methods=["POST"])
@jwt_required()
def add_private_text():
    # get the data
    data = request.get_json()

    title = data["title"]
    content = data["content"]
    url = data["url"]
    authors = [data["authors"]]
    tags = data["tags"]

    # convert date to datetime object, where date looks like '2022-07-28T23:17:36.054Z'
    date = datetime.utcnow()

    # create the text
    text = Text(title, content, url, authors, date)
    db.session.add(text)
    db.session.commit()

    # check if any of the tags don't exist
    for tag in tags:
        if Tag.query.filter_by(name=tag).first() is None:
            new_tag = Tag(tag)
            db.session.add(new_tag)
            db.session.commit()

    # now query for each tag and add to text_tag_association_table
    for tag in tags:
        tag = Tag.query.filter_by(name=tag).first()
        tag.texts.append(text)
        text.tags.append(tag)

        db.session.add(tag)
        db.session.add(text)
        db.session.commit()

    return jsonify(success=True)

@textbank_bp.route("/get-translation", methods=["GET"])
@jwt_required()
def get_translation():
    word = request.args.get("word")

    translation = translator.translate_text(word, target_lang="zh", source_lang="en")

    return jsonify(translation=translation.text)

@textbank_bp.route("/update-word-status", methods=["POST"])
@jwt_required()
def update_word_status():
    word_lemma = request.get_json()["word_lemma"]
    known = request.get_json()["known"]

    word_ob = Word.query.filter_by(lemma=word_lemma).first()

    if known == True:
        # we are removing a known word from user wordbank
        user_word = UserWord.query.filter_by(user_id=current_user.id, word_id=word_ob.id).first()
        db.session.delete(user_word)
        db.session.commit()
    elif known == False:
        # we are making a new connection
        # check if the word exists
        if word_ob == None:
            # create the word
            word_ob = Word(word_lemma)
            db.session.add(word_ob)
            db.session.commit()

        # create the user word
        user_word = UserWord(current_user.id, word_ob.id, 0)  # zero because it gets changed on page clicks
        db.session.add(user_word)
        db.session.commit()

    return jsonify(success=True)


@textbank_bp.route("/update-text-progress", methods=["POST"])
@jwt_required()
def update_text_status():
    text_id = request.get_json()["id"]
    current_page = request.get_json()["page"] - 1  # as 1 on frontend, but zero means not started
    total_pages = request.get_json()["totalPages"]
    lemma_list = request.get_json()["chunkLemmas"] # list of lemmas on page

    if current_page == 0:
        # we are discarding the started text
        user_text_match = UserText.query.filter_by(user_id=current_user.id, text_id=text_id).first()
        if user_text_match:
            db.session.delete(user_text_match)
            db.session.commit()
    else:
        user_text_match = UserText.query.filter_by(user_id=current_user.id, text_id=text_id).first()
        if not user_text_match:
            user_text_match = UserText(current_user.id, text_id, current_page, total_pages)
            db.session.add(user_text_match)
            db.session.commit()
        else:
            user_text_match.current_page = current_page
            user_text_match.total_pages = total_pages
            db.session.commit()

    # we also need to update user_word values; update the number_of_times_seen of seeing the words
    for lemma in lemma_list:
        word_ob = Word.query.filter_by(lemma=lemma).first()
        if word_ob:
            user_word_match = UserWord.query.filter_by(user_id=current_user.id, word_id=word_ob.id).first()
            if user_word_match:
                user_word_match.number_of_times_seen += 1
                db.session.commit()
            else:
                # we are not randomly adding words to the bank because they were just seen
                pass


    return jsonify(success=True)


@textbank_bp.route("/log-time", methods=["POST"])
@jwt_required()
def log_time():
    elapsed_time = request.get_json()["elapsed_time"]  # in milliseconds
    
    # convert to seconds
    elapsed_time_seconds = elapsed_time / 1000

    # and round
    elapsed_time_seconds = round(elapsed_time_seconds)

    # get today's date
    date = datetime.utcnow()


    # check if log exists for this date and this user
    # when comparing the date, just compare the date, not full timestamp
    log_match = Log.query.filter(
        Log.user_id == current_user.id,
        Log.date == date.date()).first()

    if not log_match:
        # create a new log
        log_match = Log(current_user, date.date(), elapsed_time_seconds)
        db.session.add(log_match)
        db.session.commit()
    else:
        # update the log
        log_match.elapsed_time_seconds += elapsed_time_seconds
        db.session.commit()

    return jsonify(success=True)


# one-time function
@textbank_bp.route("/text-updater", methods=["GET"])
def update_texts():
    """
    This function will add in all the (3x) lemmas for every text in the database,
    and also their summaries + simplifications.
    """

    all_texts = Text.query.all()

    for i in range(len(all_texts)):
        print(f"{i:06d} / {len(all_texts)}", end="\r")
        text = all_texts[i]
        text.synonymized_content = text.synonymize_content(text.content)
        text.summarized_content = text.summarize_content(text.content)
        (text.lemmatized_content, text.lemmatized_synonymized_content, text.lemmatized_summarized_content) = text.lemmatize_all_content(text.content)
        db.session.add(text)
        db.session.commit()
