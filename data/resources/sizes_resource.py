from flask import abort
from flask import jsonify
from data.models.additional import Sizes
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .no_picture_parser import parser, parser2


def abort_if_sizes_not_found(sizes_id):
    session = db_session.create_session()
    sizes = session.query(Sizes).get(sizes_id)
    if not sizes:
        abort(404, message=f"Size {sizes_id} not found")


class SizesResource(Resource):
    def get(self, sizes_id):
        abort_if_sizes_not_found(sizes_id)
        session = db_session.create_session()
        for _ in session.query(Sizes).filter(Sizes.deleted == 1, Sizes.id == sizes_id):
            return jsonify({f'size {sizes_id}': 'deleted'})
        else:
            sizes = session.query(Sizes).get(sizes_id)
            return jsonify({'size': sizes.to_dict(
                only=('name',))})

    def delete(self, sizes_id):
        abort_if_sizes_not_found(sizes_id)
        session = db_session.create_session()
        sizes = session.query(Sizes).get(sizes_id)
        session.delete(sizes)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, sizes_id):
        abort_if_sizes_not_found(sizes_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        sizes = session.query(Sizes).get(sizes_id)
        if args['name']:
            sizes.name = args['name']
        session.commit()
        return jsonify({'success': 'OK'})


class SizesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        sizes = session.query(Sizes).filter(Sizes.deleted == 0)
        if sizes:
            return jsonify({'sizes': [item.to_dict(
                only=('id', 'name')) for item in sizes]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        sizes = Sizes(
            name=args['name'])
        session.add(sizes)
        session.commit()
        return jsonify({'success': 'OK'})