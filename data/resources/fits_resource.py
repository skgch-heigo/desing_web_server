# что делает эта таблица + она пустая
from flask import abort
from flask import jsonify
from data.models.additional import Fits
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .no_picture_parser import parser, parser2


def abort_if_fits_not_found(fits_id):
    session = db_session.create_session()
    fits = session.query(Fits).get(fits_id)
    if not fits:
        abort(404, message=f"Fits {fits_id} not found")


class FitsResource(Resource):
    def get(self, fits_id):
        abort_if_fits_not_found(fits_id)
        session = db_session.create_session()
        for _ in session.query(Fits).filter(Fits.deleted == 1, Fits.id == fits_id):
            return jsonify({f'fit {fits_id}': 'deleted'})
        else:
            fits = session.query(Fits).get(fits_id)
            return jsonify({'fits': fits.to_dict(
                only=('name',))})

    def delete(self, fits_id):
        abort_if_fits_not_found(fits_id)
        session = db_session.create_session()
        fits = session.query(Fits).get(fits_id)
        session.delete(fits)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, fits_id):
        abort_if_fits_not_found(fits_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        fits = session.query(Fits).get(fits_id)
        if args['name']:
            fits.name = args['name']
        session.commit()
        return jsonify({'success': 'OK'})


class FitsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        fits = session.query(Fits).filter(Fits.deleted == 0)
        if fits:
            return jsonify({'fits': [item.to_dict(
                only=('id', 'name')) for item in fits]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        fits = Fits(
            name=args['name'])
        session.add(fits)
        session.commit()
        return jsonify({'success': 'OK'})