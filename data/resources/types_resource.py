from flask import abort
from flask import jsonify
from data.models.additional import Types
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .no_picture_parser import parser, parser2


def abort_if_types_not_found(types_id):
    session = db_session.create_session()
    types = session.query(Types).get(types_id)
    if not types:
        abort(404, message=f"Type {types_id} not found")


class TypesResource(Resource):
    def get(self, types_id):
        abort_if_types_not_found(types_id)
        session = db_session.create_session()
        for _ in session.query(Types).filter(Types.deleted == 1, Types.id == types_id):
            return jsonify({f'type {types_id}': 'deleted'})
        else:
            types = session.query(Types).get(types_id)
            return jsonify({'type': types.to_dict(
                only=('name',))})

    def delete(self, types_id):
        abort_if_types_not_found(types_id)
        session = db_session.create_session()
        types = session.query(Types).get(types_id)
        session.delete(types)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, types_id):
        abort_if_types_not_found(types_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        types = session.query(Types).get(types_id)
        if args['name']:
            types.name = args['name']
        session.commit()
        return jsonify({'success': 'OK'})


class TypesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        types = session.query(Types).filter(Types.deleted == 0)
        if types:
            return jsonify({'types': [item.to_dict(
                only=('id', 'name')) for item in types]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        types = Types(
            name=args['name'])
        session.add(types)
        session.commit()
        return jsonify({'success': 'OK'})