from flask import Blueprint, request, jsonify
from flask_cors import CORS
from sqlalchemy.sql.expression import func
import uuid
from models import *

title = Blueprint('title', __name__)
CORS(title)

@title.route('/label', methods=['POST'])
def add_label():
    content_type = request.headers.get('Content-Type')
    if not content_type.startswith('application/json'):
        return "Content-type not supported!", 400

    request_json = request.json
    if 'label' not in request_json or 'user_id' not in request_json or 'title_id' not in request_json:
        print(request_json)
        return "Invalid request!", 400

    label = request_json['label']
    user_id = request_json['user_id']
    title_id = request_json['title_id']
    if not isinstance(label, (bool)):
        return "Label is not boolean!", 400
    if not isinstance(user_id, (str)):
        return "UserID is not string!", 400
    if not isinstance(title_id, (str)):
        return "TitleID is not string!", 400
    if not User.query.filter_by(id=user_id).first():
        return "Given userID does not exist!", 400
    if not Title.query.filter_by(id=title_id).first():
        return "Given titleID does not exist!", 400
    if Label.query.filter_by(user_id=user_id, title_id=title_id).first():
        return "This user already labeled this title!", 409

    label = Label(
        id = uuid.uuid4(),
        user_id = user_id,
        title_id = title_id,
        label = label
    )

    db.session.add(label)
    db.session.commit()

    return "Answer succesfully submitted.", 201 

@title.route('/', methods=['GET'])
def get_title():
    headers = request.headers
    if 'Authorization' not in headers:
        return "Invalid request!", 400

    user_id = headers['Authorization']
    if not isinstance(user_id, (str)):
        return "UserID is not string!", 400
    if not User.query.filter_by(id=user_id).first():
        return "Given userID does not exist!", 400
    
    priority_list = [1, 0, 2, 3]
    subquery_user_id = db.session.query(Label.title_id).filter(Label.user_id == user_id)
    for priority in priority_list:
        if priority != 0:
            subquery_count = db.session.query(Label.title_id).group_by(Label.title_id).having(func.count(Label.title_id) == priority)
            title = Title.query.filter(Title.id.not_in(subquery_user_id), Title.id.in_(subquery_count)).order_by(func.random()).first()
        else:
            subquery_count = db.session.query(Label.title_id).group_by(Label.title_id)
            title = Title.query.filter(Title.id.not_in(subquery_count)).order_by(func.random()).first()
        if title:
            break
    if not title:
        title = Title.query.filter(Title.id.not_in(subquery_user_id)).order_by(func.random()).first()

    if not title:
        return "You labeled all titles in our database!", 204

    return jsonify({
        "id": title.id,
        "content": title.content,
    }), 200
