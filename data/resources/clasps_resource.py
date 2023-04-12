from flask import abort
from flask import jsonify
from data.models.simple_tables import Clasps
from data.models import db_session
from flask_restful import abort, Resource, reqparse

from .simple_table_parser import parser, parser2


def abort_if_clasps_not_found(clasps_id):
    session = db_session.create_session()
    clasps = session.query(Clasps).get(clasps_id)
    if not clasps:
        abort(404, message=f"Clasps {clasps_id} not found")


class ClaspsResource(Resource):
    def get(self, clasps_id):
        abort_if_clasps_not_found(clasps_id)
        session = db_session.create_session()
        for _ in session.query(Clasps).filter(Clasps.deleted == 1, Clasps.id == clasps_id):
            return jsonify({f'clasps {clasps_id}': 'deleted'})
        else:
            clasps = session.query(Clasps).get(clasps_id)
            return jsonify({'clasps': clasps.to_dict(
                only=('name', 'picture'))})

    def delete(self, clasps_id):
        abort_if_clasps_not_found(clasps_id)
        session = db_session.create_session()
        clasps = session.query(Clasps).get(clasps_id)
        session.delete(clasps)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, clasps_id):
        abort_if_clasps_not_found(clasps_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        clasps = session.query(Clasps).get(clasps_id)
        if args['name']:
            clasps.name = args['name']
        if args['picture']:
            clasps.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class ClaspsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        clasps = session.query(Clasps).filter(Clasps.deleted == 0)
        if clasps:
            return jsonify({'clasps': [item.to_dict(
                only=('id', 'name', 'picture')) for item in clasps]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        clasps = Clasps(
            name=args['name'],
            picture=args['picture'])
        session.add(clasps)
        session.commit()
        return jsonify({'success': 'OK'})