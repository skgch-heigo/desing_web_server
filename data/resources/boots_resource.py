from flask import abort
from flask import jsonify
from data.models.main_tables import Boots
from data.models import db_session
from .boots_parser import parser, parser2
from flask_restful import reqparse, abort, Api, Resource


def abort_if_boots_not_found(boots_id):
    session = db_session.create_session()
    boots = session.query(Boots).get(boots_id)
    if not boots:
        abort(404, message=f"Boots {boots_id} not found")


class BootsResource(Resource):
    def get(self, boots_id):
        abort_if_boots_not_found(boots_id)
        session = db_session.create_session()
        for _ in session.query(Boots).filter(Boots.deleted == 1, Boots.id == boots_id):
            return jsonify({f'boots {boots_id}': 'deleted'})
        else:
            boots = session.query(Boots).get(boots_id)
            return jsonify({'boots': boots.to_dict(
                only=('name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'clasp', 'heel', 'features', 'picture'))})

    def delete(self, boots_id):
        abort_if_boots_not_found(boots_id)
        session = db_session.create_session()
        boots = session.query(Boots).get(boots_id)
        session.delete(boots)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, boots_id):
        abort_if_boots_not_found(boots_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        boots = session.query(Boots).get(boots_id)
        if args['name']:
            boots.name = args['name']
        if args['season']:
            boots.season = args['season']
        if args['origin']:
            boots.origin = args['origin']
        if args['appearance_year']:
            boots.appearance_year = args['appearance_year']
        if args['popularity_start']:
            boots.popularity_start = args['popularity_start']
        if args['popularity_end']:
            boots.popularity_end = args['popularity_end']
        if args['clasp']:
            boots.clasp = args['clasp']
        if args['heel']:
            boots.heel = args['heel']
        if args['features']:
            boots.features = args['features']
        if args['picture']:
            boots.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class BootsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        boots = session.query(Boots).filter(Boots.deleted == 0)
        if boots:
            return jsonify({'boots': [item.to_dict(
                only=('id', 'name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'clasp', 'heel', 'features', 'picture',)) for item in boots]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        boots = Boots(
            id=args['id'],
            name=args['name'],
            season=args['season'],
            origin=args['origin'],
            appearance_year=args['appearance_year'],
            popularity_start=args['popularity_start'],
            popularity_end=args['popularity_end'],
            clasp=args['clasp'],
            heel=args['heel'],
            features=args['features'],
            picture=args['picture'],
        )
        session.add(boots)
        session.commit()
        return jsonify({'success': 'OK'})