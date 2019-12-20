import requests
import random
import pandas as pd

def dummy_output():

    users = ['Austen','Connor','Khaled','Elisabeth','Tony','Micah','Daniel']
    
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

def dummy_user_output(username, temp_dummy):

    valid_users = set([dummy_entry['username'] for dummy_entry in temp_dummy])
    if username not in valid_users:
        return 'username not in valid users - check /dummyfeed for a valid user.'

    dummyframe = pd.DataFrame(temp_dummy)
    avg_tox = (dummyframe.groupby('username').toxicity.mean().loc[username])
    sum_tox = dummyframe.groupby('username').toxicity.sum().loc[username]
    top_ten_tox_list = dummyframe[(dummyframe['username'] == username)].sort_values('toxicity', ascending=False).head(10)[['comment', 'toxicity','comment_id']].values.tolist()
    top_ten_tox = [dict(zip(tuple(['comment','toxicity','comment_id']), tuple(ii))) for ii in top_ten_tox_list]

    label_tuple = tuple(['username','avg_tox','total_tox','top_ten_tox'])
    data_tuple =  tuple([username, float(avg_tox), int(sum_tox), top_ten_tox])

    return dict(zip(label_tuple,data_tuple))