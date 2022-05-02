from flask_sqlalchemy import SQLAlchemy

user_db = SQLAlchemy()

class User(user_db.Model):
    __tablename__ = 'user'

    id = user_db.Column(user_db.String(36), primary_key=True)
    username = user_db.Column(user_db.String(24), nullable=False, unique=True)
    labels = user_db.relationship('Label', backref='user', lazy=True)
    score = user_db.Column(user_db.Integer, nullable=False)
