from flask import abort
from flask import jsonify
from data.models.main_tables import LowerBody
from data.models import db_session
from .lower_body_parser import parser, parser2
from flask_restful import reqparse, abort, Api, Resource


def abort_if_lower_body_not_found(lower_body_id):
    session = db_session.create_session()
    lower_body = session.query(LowerBody).get(lower_body_id)
    if not lower_body:
        abort(404, message=f"Lower body {lower_body_id} not found")


class LowerBodyResource(Resource):
    def get(self, lower_body_id):
        abort_if_lower_body_not_found(lower_body_id)
        session = db_session.create_session()
        for _ in session.query(LowerBody).filter(LowerBody.deleted == 1, LowerBody.id == lower_body_id):
            return jsonify({f'lower body {lower_body_id}': 'deleted'})
        else:
            lower_body = session.query(LowerBody).get(lower_body_id)
            return jsonify({'lower_body': lower_body.to_dict(
                only=('name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'clasp', 'fit', 'length', 'features', 'picture'))})

    def delete(self, lower_body_id):
        abort_if_lower_body_not_found(lower_body_id)
        session = db_session.create_session()
        lower_body = session.query(LowerBody).get(lower_body_id)
        session.delete(lower_body)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, lower_body_id):
        abort_if_lower_body_not_found(lower_body_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        lower_body = session.query(LowerBody).get(lower_body_id)
        if args['name']:
            lower_body.name = args['name']
        if args['season']:
            lower_body.season = args['season']
        if args['origin']:
            lower_body.origin = args['origin']
        if args['appearance_year']:
            lower_body.appearance_year = args['appearance_year']
        if args['popularity_start']:
            lower_body.popularity_start = args['popularity_start']
        if args['popularity_end']:
            lower_body.popularity_end = args['popularity_end']
        if args['clasp']:
            lower_body.clasp = args['clasp']
        if args['fit']:
            lower_body.fit = args['fit']
        if args['length']:
            lower_body.length = args['length']
        if args['features']:
            lower_body.features = args['features']
        if args['picture']:
            lower_body.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class LowerBodyListResource(Resource):
    def get(self):
        session = db_session.create_session()
        lower_body = session.query(LowerBody).filter(LowerBody.deleted == 0)
        if lower_body:
            return jsonify({'lower_body': [item.to_dict(
                only=('id', 'name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'clasp', 'fit', 'length', 'features', 'picture',)) for item in lower_body]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        lower_body = LowerBody(
            id=args['id'],
            name=args['name'],
            season=args['season'],
            origin=args['origin'],
            appearance_year=args['appearance_year'],
            popularity_start=args['popularity_start'],
            popularity_end=args['popularity_end'],
            clasp=args['clasp'],
            fit=args['fit'],
            length=args['length'],
            features=args['features'],
            picture=args['picture'],
        )
        session.add(lower_body)
        session.commit()
        return jsonify({'success': 'OK'})