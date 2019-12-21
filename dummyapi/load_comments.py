import csv
from .models import DB, Comment

def load_from_csv():
    """loads a .csv as a list of tuples, drops the header."""
    with open('hackernews_comments.csv', encoding='utf-8') as f:
        data = [tuple(line) for line in csv.reader(f)]
    data = data[1:]
    return data


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
