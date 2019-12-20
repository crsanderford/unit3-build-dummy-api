import csv
from decouple import config
import json
from flask import Flask, jsonify
import pandas as pd
import sqlite3
from sqlalchemy import func

from .models import DB, Comment
from .make_dummies import dummy_output, dummy_user_output
from .load_comments import load_from_csv, insert_comment


    

def create_app():
    app = Flask(__name__)
    app.config['ENV'] = config('ENV')
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    DB.init_app(app)

    """temp_dummy = dummy_output()"""

    @app.route('/')
    def index():
        return "...hello."

    """@app.route('/dummyfeed')
    def dummyfeed():

        return jsonify(temp_dummy)

    @app.route('/dummyuser/<username>')
    def dummyuser(username):

        return jsonify(dummy_user_output(username, temp_dummy))"""

    @app.route('/dbload')
    def dbload():
        data = load_from_csv()
        for d in data:
            insert_comment(d)
        DB.session.commit()
        return "loaded!"

    @app.route('/feed')
    def feed():
        comment_objs = Comment.query.all()
        comments = [tuple([obj.comment_id, obj.text, obj.user, obj.toxicity]) for obj in comment_objs]
        comments = [dict(zip(tuple(['id','text','user','tox']),obj)) for obj in comments]

        return jsonify(comments)

    @app.route('/user/<username>')
    def user(username):
        comment_objs = Comment.query.filter(Comment.user == username).order_by(Comment.toxicity.desc())
        comments = [tuple([obj.comment_id, obj.text, obj.toxicity]) for obj in comment_objs]
        comments = [dict(zip(tuple(['id','text','tox']),obj)) for obj in comments]

        total = Comment.query.with_entities(
             func.sum(Comment.toxicity).label("mySum")
         ).filter_by(
             user=username
         ).first()

        avg = Comment.query.with_entities(
             func.sum(Comment.toxicity).label("myAvg")
         ).filter_by(
             user=username
         ).first()

        return jsonify(dict(zip(tuple(['username','avg_tox','total_tox','top_ten_tox']),
        tuple([username,float(total.mySum),float(avg.myAvg),comments[:10]]))))

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return "database reset."


    return app