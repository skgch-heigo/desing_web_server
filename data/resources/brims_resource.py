from flask import abort
from flask import jsonify
from data.models.simple_tables import Brims
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .simple_table_parser import parser, parser2


def abort_if_brims_not_found(brims_id):
    session = db_session.create_session()
    brims = session.query(Brims).get(brims_id)
    if not brims:
        abort(404, message=f"Brims {brims_id} not found")


class BrimsResource(Resource):
    def get(self, brims_id):
        abort_if_brims_not_found(brims_id)
        session = db_session.create_session()
        for _ in session.query(Brims).filter(Brims.deleted == 1, Brims.id == brims_id):
            return jsonify({f'brim {brims_id}': 'deleted'})
        else:
            brims = session.query(Brims).get(brims_id)
            return jsonify({'brim': brims.to_dict(
                only=('name', 'picture'))})

    def delete(self, brims_id):
        abort_if_brims_not_found(brims_id)
        session = db_session.create_session()
        brims = session.query(Brims).get(brims_id)
        session.delete(brims)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, brims_id):
        abort_if_brims_not_found(brims_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        brims = session.query(Brims).get(brims_id)
        if args['name']:
            brims.name = args['name']
        if args['picture']:
            brims.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class BrimsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        brims = session.query(Brims).filter(Brims.deleted == 0)
        if brims:
            return jsonify({'brims': [item.to_dict(
                only=('id', 'name', 'picture')) for item in brims]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        brims = Brims(
            name=args['name'],
            picture=args['picture'])
        session.add(brims)
        session.commit()
        return jsonify({'success': 'OK'})