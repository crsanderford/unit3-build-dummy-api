from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class Comment(DB.Model):
    comment_id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(9000))
    user = DB.Column(DB.String(20), nullable=False)
    toxicity = DB.Column(DB.Float)

    def __repr__(self):
        return f'<comment {self.comment_id}: {self.text}'