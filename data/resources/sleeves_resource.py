from flask import abort
from flask import jsonify
from data.models.simple_tables import Sleeves
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .simple_table_parser import parser, parser2


def abort_if_sleeves_not_found(sleeves_id):
    session = db_session.create_session()
    sleeves = session.query(Sleeves).get(sleeves_id)
    if not sleeves:
        abort(404, message=f"Sleeves {sleeves_id} not found")


class SleevesResource(Resource):
    def get(self, sleeves_id):
        abort_if_sleeves_not_found(sleeves_id)
        session = db_session.create_session()
        for _ in session.query(Sleeves).filter(Sleeves.deleted == 1, Sleeves.id == sleeves_id):
            return jsonify({f'sleeves {sleeves_id}': 'deleted'})
        else:
            sleeves = session.query(Sleeves).get(sleeves_id)
            return jsonify({'sleeves': sleeves.to_dict(
                only=('name', 'picture'))})

    def delete(self, sleeves_id):
        abort_if_sleeves_not_found(sleeves_id)
        session = db_session.create_session()
        sleeves = session.query(Sleeves).get(sleeves_id)
        session.delete(sleeves)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, sleeves_id):
        abort_if_sleeves_not_found(sleeves_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        sleeves = session.query(Sleeves).get(sleeves_id)
        if args['name']:
            sleeves.name = args['name']
        if args['picture']:
            sleeves.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class SleevesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        sleeves = session.query(Sleeves).filter(Sleeves.deleted == 0)
        if sleeves:
            return jsonify({'sleeves': [item.to_dict(
                only=('id', 'name', 'picture')) for item in sleeves]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        sleeves = Sleeves(
            name=args['name'],
            picture=args['picture'])
        session.add(sleeves)
        session.commit()
        return jsonify({'success': 'OK'})