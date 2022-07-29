from typing import Text
from flask import Blueprint, request, jsonify
from itsdangerous import json
from extensions import db
from models.user import User
from models.tag import Tag
from models.word import Word
from models.text import Text, text_tag_association_table
from models.associations.user_word import UserWord
from models.associations.user_text import UserText
from flask_jwt_extended import (
    current_user,
    jwt_required,
)
from sqlalchemy import func
from datetime import datetime
from collections import Counter
import spacy
import re

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

    # get the text
    text = Text.query.filter_by(id=text_id).first()

    # replace all 2x newlines with a space and a newline
    text.content = text.content.replace("\n\n", " \n")


    output_content = []
    for word in re.split(" ", text.content):
        # check if word is whitespace with regex
        if not len(word) == 0:
            lemma = nlp(word)[0].lemma_  # TODO: do in a faster way, now problem with numbering (perhaps just newlines)
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

    return jsonify(title=text.title, content=output_content)


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
