from typing import Text
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.word import Word
from models.tag import Tag
from models.text import Text, text_tag_association_table
from models.associations.user_word import UserWord
from models.associations.user_text import UserText
from flask_jwt_extended import (
    current_user,
    jwt_required,
)
from sqlalchemy import func
import time
from collections import Counter


textbank_bp = Blueprint("textbank", __name__)

# two routes in databasetable + one route for adding custom file
@textbank_bp.route("/fetch-textbank", methods=["GET"])
@jwt_required()
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
    # s = time.process_time()
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

    # print(time.process_time() - s)
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
