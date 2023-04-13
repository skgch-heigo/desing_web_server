from flask import abort
from flask import jsonify
from data.models.user import User
from data.models import db_session
from .user_parser import parser, parser2
from flask_restful import reqparse, abort, Api, Resource


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, message=f"User {users_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        for _ in session.query(User).filter(User.deleted == 1, User.id == users_id):
            return jsonify({f'user {users_id}': 'deleted'})
        else:
            users = session.query(User).get(users_id)
            return jsonify({'user': users.to_dict(
                only=('name', 'email'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, users_id):
        abort_if_users_not_found(users_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
        if args['hashed_password']:
            user.hashed_password = args['hashed_password']
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).filter(User.deleted == 0)
        if users:
            return jsonify({'users': [item.to_dict(
                only=('name', 'email',)) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            id=args['id'],
            name=args['name'],
            email=args['email'],
            hashed_password=args['hashed_password']
        )
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})
