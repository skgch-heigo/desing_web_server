from flask import abort
from flask import jsonify
from data.models.simple_tables import Patterns
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .simple_table_parser import parser, parser2


def abort_if_patterns_not_found(patterns_id):
    session = db_session.create_session()
    patterns = session.query(Patterns).get(patterns_id)
    if not patterns:
        abort(404, message=f"Patterns {patterns_id} not found")


class PatternsResource(Resource):
    def get(self, patterns_id):
        abort_if_patterns_not_found(patterns_id)
        session = db_session.create_session()
        for _ in session.query(Patterns).filter(Patterns.deleted == 1, Patterns.id == patterns_id):
            return jsonify({f'patterns {patterns_id}': 'deleted'})
        else:
            patterns = session.query(Patterns).get(patterns_id)
            return jsonify({'patterns': patterns.to_dict(
                only=('name', 'picture'))})

    def delete(self, patterns_id):
        abort_if_patterns_not_found(patterns_id)
        session = db_session.create_session()
        patterns = session.query(Patterns).get(patterns_id)
        session.delete(patterns)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, patterns_id):
        abort_if_patterns_not_found(patterns_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        patterns = session.query(Patterns).get(patterns_id)
        if args['name']:
            patterns.name = args['name']
        if args['picture']:
            patterns.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class PatternsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        patterns = session.query(Patterns).filter(Patterns.deleted == 0)
        if patterns:
            return jsonify({'patterns': [item.to_dict(
                only=('id', 'name', 'picture')) for item in patterns]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        patterns = Patterns(
            name=args['name'],
            picture=args['picture'])
        session.add(patterns)
        session.commit()
        return jsonify({'success': 'OK'})