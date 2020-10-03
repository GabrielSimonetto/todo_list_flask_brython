from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user
from marshmallow import ValidationError

from .model import Todo
from .serializer import TodoSchema

api = Blueprint('api', __name__)


@api.route('/tasks', methods=['GET'])
def tasks():
    ts = TodoSchema(many=True)
    query_result = Todo.query.filter(
        Todo.state != 'canceled', Todo.user == current_user
    ).all()
    return jsonify(ts.dump(query_result)), 200


@api.route('/tasks', methods=['POST'])
def task_register():
    # quem vigia os vigieiros?
    ts = TodoSchema()
    try:
        task = ts.load(request.json)
        current_app.db.session.add(task)
        current_app.db.session.commit()
        return ts.dump(task), 201
    except ValidationError as err:
        return jsonify(err.messages), 400


@api.route('/tasks/<int:_id>/', methods=['PATCH'])
def change_task_state(_id):
    ts = TodoSchema()

    new_state = request.json.get('state')

    states = ['todo', 'doing', 'done', 'canceled']

    task = Todo.query.filter_by(id=_id).one()

    if new_state in states:
        task.state = new_state
        current_app.db.session.commit()

    return jsonify(ts.dump(task))
