from flask import abort
from flask import jsonify
from data.models.wardrobe import Wardrobe
from data.models import db_session
from flask_restful import abort, Resource, reqparse

from .wardrobe_parser import parser, parser2


def abort_if_wardrobe_not_found(wardrobe_id):
    session = db_session.create_session()
    wardrobe = session.query(Wardrobe).get(wardrobe_id)
    if not wardrobe:
        abort(404, message=f"Wardrobe {wardrobe_id} not found")


class WardrobeResource(Resource):
    def get(self, wardrobe_id):
        abort_if_wardrobe_not_found(wardrobe_id)
        session = db_session.create_session()
        for _ in session.query(Wardrobe).filter(Wardrobe.deleted == 1, Wardrobe.id == wardrobe_id):
            return jsonify({f'wardrobe {wardrobe_id}': 'deleted'})
        else:
            fabrics = session.query(Wardrobe).get(wardrobe_id)
            return jsonify({'wardrobe': fabrics.to_dict(
                only=('name', 'type_', 'color', 'size', 'fabric', 'pattern', 'owner', 'picture'))})

    def delete(self, wardrobe_id):
        abort_if_wardrobe_not_found(wardrobe_id)
        session = db_session.create_session()
        wardrobe = session.query(Wardrobe).get(wardrobe_id)
        session.delete(wardrobe)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, wardrobe_id):
        abort_if_wardrobe_not_found(wardrobe_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        wardrobe = session.query(Wardrobe).get(wardrobe_id)
        if args['name']:
            wardrobe.name = args['name']
        if args['type_']:
            wardrobe.type_ = args['type_']
        if args['color']:
            wardrobe.color = args['color']
        if args['size']:
            wardrobe.size = args['size']
        if args['fabric']:
            wardrobe.fabric = args['fabric']
        if args['pattern']:
            wardrobe.pattern = args['pattern']
        if args['owner']:
            wardrobe.owner = args['owner']
        if args['picture']:
            wardrobe.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class WardrobeListResource(Resource):
    def get(self):
        session = db_session.create_session()
        wardrobe = session.query(Wardrobe).filter(Wardrobe.deleted == 0)
        if wardrobe:
            return jsonify({'wardrobe': [item.to_dict(
                only=('name', 'type_', 'color', 'size', 'fabric', 'pattern', 'owner', 'picture')) for item in
                wardrobe]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        wardrobe = Wardrobe(
            name=args['name'],
            type_=args['type_'],
            color=args['color'],
            size=args['size'],
            fabric=args['fabric'],
            pattern=args['pattern'],
            owner=args['owner'],
            picture=args['picture'])
        session.add(wardrobe)
        session.commit()
        return jsonify({'success': 'OK'})
