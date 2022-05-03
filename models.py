from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True)
    score = db.Column(db.Integer, nullable=False)
    labels = db.relationship('Label', backref='user', lazy=True)

class Title(db.Model):
    __tablename__ = 'title'

    id = db.Column(db.String(36), primary_key=True)
    content = db.Column(db.String(256), nullable=False)
    origin = db.Column(db.String(32), nullable=False)
    labels = db.relationship('Label', backref='title', lazy=True)

class Label(db.Model):
    __tablename__ = 'label'

    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey(User.id), nullable=False)
    title_id = db.Column(db.String(36), db.ForeignKey(Title.id), nullable=False)
    label = db.Column(db.Boolean, nullable=False)
