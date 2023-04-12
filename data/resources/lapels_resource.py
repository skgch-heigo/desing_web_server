from flask import abort
from flask import jsonify
from data.models.simple_tables import Lapels
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .simple_table_parser import parser, parser2


def abort_if_lapels_not_found(lapels_id):
    session = db_session.create_session()
    lapels = session.query(Lapels).get(lapels_id)
    if not lapels:
        abort(404, message=f"Lapels {lapels_id} not found")


class LapelsResource(Resource):
    def get(self, lapels_id):
        abort_if_lapels_not_found(lapels_id)
        session = db_session.create_session()
        for _ in session.query(Lapels).filter(Lapels.deleted == 1, Lapels.id == lapels_id):
            return jsonify({f'lapel {lapels_id}': 'deleted'})
        else:
            lapels = session.query(Lapels).get(lapels_id)
            return jsonify({'lapels': lapels.to_dict(
                only=('name', 'picture'))})

    def delete(self, lapels_id):
        abort_if_lapels_not_found(lapels_id)
        session = db_session.create_session()
        lapels = session.query(Lapels).get(lapels_id)
        session.delete(lapels)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, lapels_id):
        abort_if_lapels_not_found(lapels_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        lapels = session.query(Lapels).get(lapels_id)
        if args['name']:
            lapels.name = args['name']
        if args['picture']:
            lapels.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class LapelsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        lapels = session.query(Lapels).filter(Lapels.deleted == 0)
        if lapels:
            return jsonify({'lapels': [item.to_dict(
                only=('id', 'name', 'picture')) for item in lapels]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        lapels = Lapels(
            name=args['name'],
            picture=args['picture'])
        session.add(lapels)
        session.commit()
        return jsonify({'success': 'OK'})