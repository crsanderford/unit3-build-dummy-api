import csv
from decouple import config
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import sqlite3
from sqlalchemy import func

from .models import DB, Comment
from .make_dummies import dummy_output, dummy_user_output
from .load_comments import load_from_csv, load_into_df, add_df_prediction, insert_comments_from_df, insert_comment, insert_comment_with_model


    

def create_app():
    app = Flask(__name__)
    CORS(app)


    app.config['ENV'] = config('ENV')
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    DB.init_app(app)

    # yes, this is hacky - but Flask has issues with loading/running a model under a decorator.
    # something about threading, I think?
    # it runs, but requires using Heroku's biggest dyno, so the model output has been added to the csv.
    """dataframe = load_into_df()
    dataframe = add_df_prediction(dataframe)"""

    @app.route('/')
    def index():
        return "The not-so-dummy DS API for Saltiest Hackers team 2."

    @app.route('/dbload')
    def dbload():
        """loads HackerNews data from a local .csv file using training toxicity scores."""
        data = load_from_csv()
        for d in data:
            insert_comment(d)
        DB.session.commit()
        return "loaded from csv!"

    """@app.route('/dbload_model')
    def dbload_model():
        """"""loads HackerNews data from csv into dataframe, applies model, stores to db.
              Not in use to avoid dyno costs.""""""
        
        insert_comments_from_df(dataframe)
        DB.session.commit()
        return "loaded with model and dataframe!"""

    @app.route('/dbload_model')
    def dbload_model():
        """loads HackerNews data from a local .csv file using model output."""
        data = load_from_csv()
        for d in data:
            insert_comment_with_model(d)
        DB.session.commit()
        return "loaded from csv, using model!"

    

    @app.route('/smallload')
    def smallload():
        """loads 50 rows of HackerNews data from a local .csv file."""
        data = load_from_csv()
        for ii in range(0,50):
            insert_comment(data[ii])
        DB.session.commit()
        return "small loaded!"

    @app.route('/feed', methods=['GET'])
    def feed():
        """returns a JSON of the 200 most toxic comments in the database, in random order."""
        comment_objs = Comment.query.order_by(Comment.toxicity.desc()).limit(200).from_self().order_by(func.random())
        comments = [tuple([obj.comment_id, obj.text, obj.author, obj.toxicity]) for obj in comment_objs]
        comments = [dict(zip(tuple(['id','text','author','tox']),obj)) for obj in comments]

        return jsonify(comments)

    @app.route('/author', methods=['POST'])
    def authors():
        """returns a JSON containing a comment author's average and total toxicity score, their toxicity rank,
        and their ten most toxic comments."""

        content = request.get_json(force=True)
        author = content['author']

        comment_objs = Comment.query.filter(Comment.author == author).order_by(Comment.toxicity.desc()).limit(10)
        comments = [tuple([obj.comment_id, obj.text, obj.toxicity]) for obj in comment_objs]
        comments = [dict(zip(tuple(['id','text','tox']),obj)) for obj in comments]

        total = Comment.query.with_entities(
             func.sum(Comment.toxicity).label("Sum")
         ).filter_by(
             author=author
         ).first()

        avg = Comment.query.with_entities(
             func.avg(Comment.toxicity).label("Avg")
         ).filter_by(
             author=author
         ).first()

        toxrank_result = DB.session.execute(f"""SELECT tox_rank FROM (
        SELECT author, mean,  RANK () OVER (ORDER BY mean DESC) as tox_rank FROM (
        SELECT author, AVG(toxicity) as mean FROM comment GROUP BY author) AS mean_toxes) AS tox_ranks WHERE author = '{author}';""")
        toxrank_rows = [x for x in toxrank_result]
        toxrank = [x.items() for x in toxrank_rows][0][0][1]

        send_back = dict(zip(tuple(['author','avg_tox','total_tox','tox_rank','top_ten_tox']),
        tuple([author,round(float(avg.Avg),2),round(float(total.Sum),2),int(toxrank),comments])))


        return jsonify(send_back)


    @app.route('/reset')
    def reset():
        """resets the database."""
        DB.drop_all()
        DB.create_all()
        return "database reset."


    return app