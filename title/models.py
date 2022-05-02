from flask_sqlalchemy import SQLAlchemy
from user.models import user_db

title_db = SQLAlchemy()

class Title(title_db.Model):
    __tablename__ = 'title'

    id = title_db.Column(title_db.String(36), primary_key=True)
    content = title_db.Column(title_db.String(256), nullable=False)
    origin = title_db.Column(title_db.String(32), nullable=False)
    labels = title_db.relationship('Label', backref='title', lazy=True)

class Label(title_db.Model):
    __tablename__ = 'label'

    id = title_db.Column(title_db.String(36), primary_key=True)
    user_id = title_db.Column(title_db.String(36), user_db.ForeignKey('user.id'), nullable=False)
    title_id = title_db.Column(title_db.String(36), title_db.ForeignKey('title.id'), nullable=False)
    label = title_db.Column(title_db.Boolean, nullable=False)
    