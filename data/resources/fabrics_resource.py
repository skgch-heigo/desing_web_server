from flask import abort
from flask import jsonify
from data.models.fabrics import Fabrics
from data.models import db_session
from flask_restful import abort, Resource, reqparse

from .fabrics_parser import parser, parser2


def abort_if_fabrics_not_found(fabrics_id):
    session = db_session.create_session()
    fabrics = session.query(Fabrics).get(fabrics_id)
    if not fabrics:
        abort(404, message=f"Fabric {fabrics_id} not found")


class FabricsResource(Resource):
    def get(self, fabrics_id):
        abort_if_fabrics_not_found(fabrics_id)
        session = db_session.create_session()
        for _ in session.query(Fabrics).filter(Fabrics.deleted == 1, Fabrics.id == fabrics_id):
            return jsonify({f'fabric {fabrics_id}': 'deleted'})
        else:
            fabrics = session.query(Fabrics).get(fabrics_id)
            return jsonify({'fabric': fabrics.to_dict(
                only=('name', 'warmth', 'washing', 'picture'))})

    def delete(self, fabrics_id):
        abort_if_fabrics_not_found(fabrics_id)
        session = db_session.create_session()
        fabrics = session.query(Fabrics).get(fabrics_id)
        session.delete(fabrics)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, fabrics_id):
        abort_if_fabrics_not_found(fabrics_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        fabrics = session.query(Fabrics).get(fabrics_id)
        if args['name']:
            fabrics.name = args['name']
        if args['warmth']:
            fabrics.warmth = args['warmth']
        if args['washing']:
            fabrics.washing = args['washing']
        if args['picture']:
            fabrics.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class FabricsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        fabrics = session.query(Fabrics).filter(Fabrics.deleted == 0)
        if fabrics:
            return jsonify({'fabrics': [item.to_dict(
                only=('id', 'name', 'warmth', 'washing', 'picture')) for item in fabrics]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        fabrics = Fabrics(
            name=args['name'],
            warmth=args['warmth'],
            washing=args['washing'],
            picture=args['picture'])
        session.add(fabrics)
        session.commit()
        return jsonify({'success': 'OK'})
