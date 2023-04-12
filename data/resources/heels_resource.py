from flask import abort
from flask import jsonify
from data.models.simple_tables import Heels
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .simple_table_parser import parser, parser2


def abort_if_heels_not_found(heels_id):
    session = db_session.create_session()
    heels = session.query(Heels).get(heels_id)
    if not heels:
        abort(404, message=f"Heels {heels_id} not found")


class HeelsResource(Resource):
    def get(self, heels_id):
        abort_if_heels_not_found(heels_id)
        session = db_session.create_session()
        for _ in session.query(Heels).filter(Heels.deleted == 1, Heels.id == heels_id):
            return jsonify({f'heels {heels_id}': 'deleted'})
        else:
            heels = session.query(Heels).get(heels_id)
            return jsonify({'heels': heels.to_dict(
                only=('name', 'picture'))})

    def delete(self, heels_id):
        abort_if_heels_not_found(heels_id)
        session = db_session.create_session()
        heels = session.query(Heels).get(heels_id)
        session.delete(heels)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, heels_id):
        abort_if_heels_not_found(heels_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        heels = session.query(Heels).get(heels_id)
        if args['name']:
            heels.name = args['name']
        if args['picture']:
            heels.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class HeelsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        heels = session.query(Heels).filter(Heels.deleted == 0)
        if heels:
            return jsonify({'heels': [item.to_dict(
                only=('id', 'name', 'picture')) for item in heels]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        heels = Heels(
            name=args['name'],
            picture=args['picture'])
        session.add(heels)
        session.commit()
        return jsonify({'success': 'OK'})