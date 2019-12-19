from decouple import config
import requests
import random
import json
from flask import Flask
import pandas as pd


users = ['Austen','Connor','Khaled','Elisabeth','Tony','Micah','Daniel']

def dummy_output():
    dummy_output = []

    for ii in range(0,100):
        username = users[random.randint(0, len(users)-1)]
        comment = pork_ipsum = requests.get('https://baconipsum.com/api/?type=all-meat&sentences=1&start-with-lorem=1').json()[0][:100]
        comment_id = ii+1
        toxicity = round(random.uniform(0.0,100.0))

        label_tuple = tuple(['username','comment','comment_id','toxicity'])
        comment_tuple = tuple([username, comment, comment_id, toxicity])

        dummy_output.append(dict(zip(label_tuple,comment_tuple)))

    return dummy_output

temp_dummy = dummy_output()

def dummy_user_output(username, temp_dummy):

    valid_users = set([dummy_entry['username'] for dummy_entry in temp_dummy])
    if username not in valid_users:
        return 'username not in valid users - check /dummyfeed for a valid user.'

    dummyframe = pd.DataFrame(temp_dummy)
    avg_tox = (dummyframe.groupby('username').toxicity.mean().loc[username])
    sum_tox = dummyframe.groupby('username').toxicity.sum().loc[username]
    top_ten_tox = dummyframe[(dummyframe['username'] == username)].sort_values('toxicity', ascending=False).head(10)[['comment', 'toxicity','comment_id']].values.tolist()

    label_tuple = tuple(['username','avg_tox','total_tox','top_ten_tox'])
    data_tuple =  tuple([username, float(avg_tox), int(sum_tox), top_ten_tox])

    return dict(zip(label_tuple,data_tuple))


    

def create_app():
    app = Flask(__name__)
    app.config['ENV'] = config('ENV')

    @app.route('/')
    def index():
        return "...hello."

    @app.route('/dummyfeed')
    def dummyfeed():

        return json.dumps(temp_dummy)

    @app.route('/dummyuser/<username>')
    def dummyuser(username):

        return json.dumps(dummy_user_output(username, temp_dummy))


    return app