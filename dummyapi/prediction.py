import pandas as pd
import numpy as np
import re
import spacy
import string
import sklearn

from html.parser import HTMLParser
from joblib import load

import tensorflow as tf

nlp = spacy.load('en_core_web_sm')
tfidf = load('tfidf.joblib')
wordlist = load('wordlist.joblib')

tf.keras.backend.clear_session()
model = tf.keras.models.load_model('simple_nn.h5')
model._make_predict_function()
graph = tf.get_default_graph()

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def preprocess(text):
    """cleans a single text input."""
    text = strip_tags(text)
    text = re.sub('\s+', ' ', text)
    text = text.lower()
    text = str(re.sub('[{}]'.format(string.punctuation), '', text))
    text = text.strip()
    return text

def vectorize(text):
    """vectorizes a single text input."""
    tokens = nlp.tokenizer(text)
    lemmas = [' '.join([token.lemma_ for token in tokens])]

    vec = tfidf.transform(lemmas).todense()
    df = pd.DataFrame(vec, columns=tfidf.get_feature_names())
    return(df[wordlist])

def model_predict(input):
    global graph
    with graph.as_default():
        output = model.predict(input)
    return output

def model_predict_single(text):
    """applies cleaning and vectorizing to a single text input, produces a prediction."""
    text = preprocess(text)
    predicted = np.float64(model.predict([vectorize(
            text)])[0][0])
    
    return predicted

def model_predict_df(df_in):
    """applies cleaning and vectorizing to a dataframe, produces a Series of predictions."""
    df = df_in.copy()
    df['clean_text'] = df['text'].apply(preprocess)
    X_test = df['clean_text'].copy()
    X_test = X_test.apply(nlp.tokenizer)
    X_test = X_test.apply(lambda x: [token.lemma_ for token in x])
    X_vec = tfidf.transform(X_test.astype(str))
    X_vec_frame = pd.DataFrame(X_vec.todense(), columns=tfidf.get_feature_names())
    X_vec_frame = X_vec_frame[wordlist]
    X_pred = model_predict(X_vec_frame)
    X_pred.shape = (9970)
    model_pred = pd.Series(data=X_pred, name='model_output')
    return model_pred

