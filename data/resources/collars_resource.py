from flask import abort
from flask import jsonify
from data.models.simple_tables import Collars
from data.models import db_session
from flask_restful import abort, Resource, reqparse

from .simple_table_parser import parser, parser2


def abort_if_collars_not_found(collars_id):
    session = db_session.create_session()
    collars = session.query(Collars).get(collars_id)
    if not collars:
        abort(404, message=f"Collar {collars_id} not found")


class CollarsResource(Resource):
    def get(self, collars_id):
        abort_if_collars_not_found(collars_id)
        session = db_session.create_session()
        for _ in session.query(Collars).filter(Collars.deleted == 1, Collars.id == collars_id):
            return jsonify({f'collar {collars_id}': 'deleted'})
        else:
            collars = session.query(Collars).get(collars_id)
            return jsonify({'collar': collars.to_dict(
                only=('name', 'picture'))})

    def delete(self, collars_id):
        abort_if_collars_not_found(collars_id)
        session = db_session.create_session()
        collars = session.query(Collars).get(collars_id)
        session.delete(collars)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, collars_id):
        abort_if_collars_not_found(collars_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        collars = session.query(Collars).get(collars_id)
        if args['name']:
            collars.name = args['name']
        if args['picture']:
            collars.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class CollarsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        collars = session.query(Collars).filter(Collars.deleted == 0)
        if collars:
            return jsonify({'collars': [item.to_dict(
                only=('id', 'name', 'picture')) for item in collars]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        collars = Collars(
            name=args['name'],
            picture=args['picture'])
        session.add(collars)
        session.commit()
        return jsonify({'success': 'OK'})