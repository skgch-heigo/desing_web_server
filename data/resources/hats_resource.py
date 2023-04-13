from flask import abort
from flask import jsonify
from data.models.main_tables import Hats
from data.models import db_session
from .hats_parser import parser, parser2
from flask_restful import reqparse, abort, Api, Resource


def abort_if_hats_not_found(hats_id):
    session = db_session.create_session()
    hats = session.query(Hats).get(hats_id)
    if not hats:
        abort(404, message=f"Hat {hats_id} not found")


class HatsResource(Resource):
    def get(self, hats_id):
        abort_if_hats_not_found(hats_id)
        session = db_session.create_session()
        for _ in session.query(Hats).filter(Hats.deleted == 1, Hats.id == hats_id):
            return jsonify({f'hat {hats_id}': 'deleted'})
        else:
            hats = session.query(Hats).get(hats_id)
            return jsonify({'hats': hats.to_dict(
                only=('name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'brim', 'features', 'picture'))})

    def delete(self, hats_id):
        abort_if_hats_not_found(hats_id)
        session = db_session.create_session()
        hats = session.query(Hats).get(hatsv_id)
        session.delete(hats)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, hats_id):
        abort_if_hats_not_found(hats_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        hats = session.query(Hats).get(hats_id)
        if args['name']:
            hats.name = args['name']
        if args['season']:
            hats.season = args['season']
        if args['origin']:
            hats.origin = args['origin']
        if args['appearance_year']:
            hats.appearance_year = args['appearance_year']
        if args['popularity_start']:
            hats.popularity_start = args['popularity_start']
        if args['popularity_end']:
            hats.popularity_end = args['popularity_end']
        if args['brim']:
            hats.brim = args['brim']
        if args['features']:
            hats.features = args['features']
        if args['picture']:
            hats.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class HatsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        hats = session.query(Hats).filter(Hats.deleted == 0)
        if hats:
            return jsonify({'hats': [item.to_dict(
                only=('id', 'name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'brim', 'features', 'picture',)) for item in hats]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        hats = Hats(
            id=args['id'],
            name=args['name'],
            season=args['season'],
            origin=args['origin'],
            appearance_year=args['appearance_year'],
            popularity_start=args['popularity_start'],
            popularity_end=args['popularity_end'],
            brim=args['brim'],
            features=args['features'],
            picture=args['picture']
        )
        session.add(hats)
        session.commit()
        return jsonify({'success': 'OK'})
