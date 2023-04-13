from flask import abort
from flask import jsonify
from data.models.additional import Seasons
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .no_picture_parser import parser, parser2


def abort_if_seasons_not_found(seasons_id):
    session = db_session.create_session()
    seasons = session.query(Seasons).get(seasons_id)
    if not seasons:
        abort(404, message=f"Season {seasons_id} not found")


class SeasonsResource(Resource):
    def get(self, seasons_id):
        abort_if_seasons_not_found(seasons_id)
        session = db_session.create_session()
        for _ in session.query(Seasons).filter(Seasons.deleted == 1, Seasons.id == seasons_id):
            return jsonify({f'season {seasons_id}': 'deleted'})
        else:
            seasons = session.query(Seasons).get(seasons_id)
            return jsonify({'season': seasons.to_dict(
                only=('name',))})

    def delete(self, seasons_id):
        abort_if_seasons_not_found(seasons_id)
        session = db_session.create_session()
        seasons = session.query(Seasons).get(seasons_id)
        session.delete(seasons)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, seasons_id):
        abort_if_seasons_not_found(seasons_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        seasons = session.query(Seasons).get(seasons_id)
        if args['name']:
            seasons.name = args['name']
        session.commit()
        return jsonify({'success': 'OK'})


class SeasonsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        seasons = session.query(Seasons).filter(Seasons.deleted == 0)
        if seasons:
            return jsonify({'seasons': [item.to_dict(
                only=('id', 'name')) for item in seasons]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        seasons = Seasons(
            name=args['name'])
        session.add(seasons)
        session.commit()
        return jsonify({'success': 'OK'})