from flask import abort
from flask import jsonify
from data.models.simple_tables import TrouserLengths
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .simple_table_parser import parser, parser2


def abort_if_trouserlengths_not_found(trouserlengths_id):
    session = db_session.create_session()
    trouserlengths = session.query(TrouserLengths).get(trouserlengths_id)
    if not trouserlengths:
        abort(404, message=f"TrouserLengths {trouserlengths_id} not found")


class TrouserLengthsResource(Resource):
    def get(self, trouserlengths_id):
        abort_if_trouserlengths_not_found(trouserlengths_id)
        session = db_session.create_session()
        for _ in session.query(TrouserLengths).filter(TrouserLengths.deleted == 1, TrouserLengths.id == trouserlengths_id):
            return jsonify({f'trouser lengths {trouserlengths_id}': 'deleted'})
        else:
            trouserlengths = session.query(TrouserLengths).get(trouserlengths_id)
            return jsonify({'trouser lengths': trouserlengths.to_dict(
                only=('name', 'picture'))})

    def delete(self,trouserlengths_id):
        abort_if_trouserlengths_not_found(trouserlengths_id)
        session = db_session.create_session()
        trouserlengths = session.query(TrouserLengths).get(trouserlengths_id)
        session.delete(trouserlengths)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, trouserlengths_id):
        abort_if_trouserlengths_not_found(trouserlengths_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        trouserlengths = session.query(TrouserLengths).get(trouserlengths_id)
        if args['name']:
            trouserlengths.name = args['name']
        if args['picture']:
            trouserlengths.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class TrouserLengthsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        trouserlengths = session.query(TrouserLengths).filter(TrouserLengths.deleted == 0)
        if trouserlengths:
            return jsonify({'trouserlengths': [item.to_dict(
                only=('id', 'name', 'picture')) for item in trouserlengths]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        trouserlengths = TrouserLengths(
            name=args['name'],
            picture=args['picture'])
        session.add(trouserlengths)
        session.commit()
        return jsonify({'success': 'OK'})