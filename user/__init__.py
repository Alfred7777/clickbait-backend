from flask import Blueprint, request, jsonify
from flask_cors import CORS
import regex as re
import uuid
from models import *

user = Blueprint('user', __name__)
CORS(user)

@user.route('/create', methods=['POST'])
def create_user():
    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        return "Content-type not supported!", 400

    request_json = request.json
    if 'username' not in request_json:
        return "Invalid request!", 400

    username = request_json['username']
    if len(username) < 3:
        return "Username is too short!", 400
    if len(username) > 20:
        return "Username is too long!", 400
    if not re.match(r"^[A-Za-z0-9_]+$", username):
        return "Username contains invalid characters!", 400
    if User.query.filter_by(username=username).first():
        return "Username already exists!", 409

    user = User(
        id = str(uuid.uuid4()),
        username = username,
        score = 0
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "user_id": user.id
    }), 201

@user.route('/ranking', methods=['GET'])
def get_user_ranking():
    users = User.query.all()

    users_data = []

    for user in users:
        user_data = {}
        user_data['username'] = user.username
        user_data['score'] = user.score
        users_data.append(user_data)

    return jsonify({
        "users": users_data
    }), 200
