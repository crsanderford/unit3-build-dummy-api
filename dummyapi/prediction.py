import pandas as pd
import numpy as np
import re
import spacy
import string
import sklearn

from html.parser import HTMLParser
from joblib import load

from tensorflow.keras.models import load_model

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
    text = strip_tags(text)
    text = re.sub('\s+', ' ', text)
    text = text.strip()
    return text

def vectorize(text):
    nlp = spacy.load('en_core_web_sm')
    tfidf = load('tfidf.joblib')
    wordlist = load('wordlist.joblib')
    
    text = text.lower()
    text = str(re.sub('[{}]'.format(string.punctuation), '', text))
    text = text.strip()
    
    tokens = nlp.tokenizer(text)
    lemmas = [' '.join([token.lemma_ for token in tokens])]

    vec = tfidf.transform(lemmas).todense()
    df = pd.DataFrame(vec, columns=tfidf.get_feature_names())
    return(df[wordlist])

def model_predict(text):
    model = load_model('simple_nn.h5')
    
    text = preprocess(text)
    predicted = np.float64(model.predict([vectorize(
            text)])[0][0])
    
    return predicted