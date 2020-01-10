import csv
from .models import DB, Comment
from .prediction import MLStripper, strip_tags, preprocess, vectorize, model_predict_single, model_predict_df, pd

def load_from_csv():
    """loads a csv as a list of tuples, drops the header."""
    with open('hackernews_comments_with_model.csv', encoding='utf-8') as f:
        data = [tuple(line) for line in csv.reader(f)]
    data = data[1:]
    return data

def load_into_df():
    """loads a csv into a dataframe, drops unused columns"""
    df = pd.read_csv('hackernews_comments_with_model.csv')
    df.drop(labels=['by','parent','deleted','dead','ranking','neg','neu',
                    'pos','compound','tb_polarity','tb_subjectivity','toxicity'],
                    axis=1, inplace=True)
    return df

def add_df_prediction(df_in):
    """adds a column called 'toxicity' to a dataframe, predicting from column named 'text'"""
    df = df_in.copy()
    model_output = model_predict_df(df)
    df['toxicity'] = model_output
    return df

def insert_comments_from_df(df):
    """inserts comments from dataframe.itertuples() into the database."""
    for row in df.itertuples(index=False):
        try:
            comment_id = row[0]
            author = row[1]
            text = row[4]
            toxicity = round(float(row[5]), 2)
            db_comment=Comment(comment_id=comment_id, author=author, text=text, toxicity=toxicity)
            DB.session.add(db_comment)
        except Exception as e:
            print(f'Error processing{comment_id}: {e}')
            raise e


def insert_comment(comment_tuple):
    "add a comment to the database"
    try:
        comment_id = comment_tuple[0]
        author = comment_tuple[1]
        text = comment_tuple[5]
        toxicity = round(float(comment_tuple[16]), 2)
        db_comment=Comment(comment_id=comment_id, author=author, text=text, toxicity=toxicity)
        DB.session.add(db_comment)
    
    except Exception as e:
        print(f'Error processing{comment_id}: {e}')
        raise e


def insert_comment_with_model(comment_tuple):
    "add a comment to the database"
    try:
        comment_id = comment_tuple[0]
        author = comment_tuple[1]
        text = comment_tuple[5]
        toxicity = round(float(comment_tuple[17]), 2)
        db_comment=Comment(comment_id=comment_id, author=author, text=text, toxicity=toxicity)
        DB.session.add(db_comment)
    
    except Exception as e:
        print(f'Error processing{comment_id}: {e}')
        raise e
