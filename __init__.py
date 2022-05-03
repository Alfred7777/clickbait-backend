import os
from flask import Flask
from flask_cors import CORS
from models import db
from user import user
from title import title

def create_app():
    app = Flask('clickbait-backend')
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Kiepski7890@localhost/clickbait-db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = 'secret string'

    db.init_app(app)
    db.create_all(app=app)

    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(title, url_prefix='/title')

    return app
