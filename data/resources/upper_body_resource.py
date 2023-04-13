from flask import abort
from flask import jsonify
from data.models.main_tables import UpperBody
from data.models import db_session
from .upper_body_parser import parser, parser2
from flask_restful import reqparse, abort, Api, Resource


def abort_if_upper_body_not_found(upper_body_id):
    session = db_session.create_session()
    upper_body = session.query(UpperBody).get(upper_body_id)
    if not upper_body:
        abort(404, message=f"Upper body {upper_body_id} not found")


class UpperBodyResource(Resource):
    def get(self, upper_body_id):
        abort_if_upper_body_not_found(upper_body_id)
        session = db_session.create_session()
        for _ in session.query(UpperBody).filter(UpperBody.deleted == 1, UpperBody.id == upper_body_id):
            return jsonify({f'upper body {upper_body_id}': 'deleted'})
        else:
            upper_body = session.query(UpperBody).get(upper_body_id)
            return jsonify({'upper_body': upper_body.to_dict(
                only=('name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'clasp', 'sleeves', 'collar', 'hood', 'lapels',
                      'pockets', 'fitted', 'features', 'picture'))})

    def delete(self, upper_body_id):
        abort_if_upper_body_not_found(upper_body_id)
        session = db_session.create_session()
        upper_body = session.query(UpperBody).get(upper_body_id)
        session.delete(upper_body)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, upper_body_id):
        abort_if_upper_body_not_found(upper_body_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        upper_body = session.query(UpperBody).get(upper_body_id)
        if args['name']:
            upper_body.name = args['name']
        if args['season']:
            upper_body.season = args['season']
        if args['origin']:
            upper_body.origin = args['origin']
        if args['appearance_year']:
            upper_body.appearance_year = args['appearance_year']
        if args['popularity_start']:
            upper_body.popularity_start = args['popularity_start']
        if args['popularity_end']:
            upper_body.popularity_end = args['popularity_end']
        if args['clasp']:
            upper_body.clasp = args['clasp']
        if args['sleeves']:
            upper_body.sleeves = args['sleeves']
        if args['collar']:
            upper_body.collar = args['collar']
        if args['hood']:
            upper_body.hood = args['hood']
        if args['lapels']:
            upper_body.lapels = args['lapels']
        if args['pockets']:
            upper_body.pockets = args['pockets']
        if args['fitted']:
            upper_body.fitted = args['fitted']
        if args['features']:
            upper_body.features = args['features']
        if args['picture']:
            upper_body.picture = args['picture']
        session.commit()
        return jsonify({'success': 'OK'})


class LowerBodyListResource(Resource):
    def get(self):
        session = db_session.create_session()
        upper_body = session.query(UpperBody).filter(UpperBody.deleted == 0)
        if upper_body:
            return jsonify({'upper_body': [item.to_dict(
                only=('id', 'name', 'season', 'origin', 'appearance_year', 'popularity_start',
                      'popularity_end', 'clasp', 'sleeves', 'collar', 'hood', 'lapels',
                      'pockets', 'fitted', 'features', 'picture',)) for item in upper_body]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        upper_body = UpperBody(
            id=args['id'],
            name=args['name'],
            season=args['season'],
            origin=args['origin'],
            appearance_year=args['appearance_year'],
            popularity_start=args['popularity_start'],
            popularity_end=args['popularity_end'],
            clasp=args['clasp'],
            sleeves=args['sleeves'],
            collar=args['collar'],
            hood=args['hood'],
            lapels=args['lapels'],
            pockets=args['pockets'],
            fitted=args['fitted'],
            features=args['features'],
            picture=args['picture'],
        )
        session.add(upper_body)
        session.commit()
        return jsonify({'success': 'OK'})