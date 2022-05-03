import os
from flask import Flask
from flask_cors import CORS
from models import db
from user import user
from title import title

def create_app():
    app = Flask('clickbait-backend')
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('CLICKBAIT_DATABASE_URI')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv('SECRET_KEY')

    db.init_app(app)
    db.create_all(app=app)

    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(title, url_prefix='/title')

    return app
