from flask import abort
from flask import jsonify
from data.models.additional import Countries
from data.models import db_session
from flask_restful import abort, Resource, reqparse
from .no_picture_parser import parser, parser2


def abort_if_countries_not_found(countries_id):
    session = db_session.create_session()
    countries = session.query(Countries).get(countries_id)
    if not countries:
        abort(404, message=f"Country {countries_id} not found")


class CountriesResource(Resource):
    def get(self, countries_id):
        abort_if_countries_not_found(countries_id)
        session = db_session.create_session()
        for _ in session.query(Countries).filter(Countries.deleted == 1, Countries.id == countries_id):
            return jsonify({f'country {countries_id}': 'deleted'})
        else:
            countries = session.query(Countries).get(countries_id)
            return jsonify({'country': countries.to_dict(
                only=('name',))})

    def delete(self, countries_id):
        abort_if_countries_not_found(countries_id)
        session = db_session.create_session()
        countries = session.query(Countries).get(countries_id)
        session.delete(countries)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, countries_id):
        abort_if_countries_not_found(countries_id)
        args = parser2.parse_args()
        session = db_session.create_session()
        countries = session.query(Countries).get(countries_id)
        if args['name']:
            countries.name = args['name']
        session.commit()
        return jsonify({'success': 'OK'})


class CountriesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        countries = session.query(Countries).filter(Countries.deleted == 0)
        if countries:
            return jsonify({'countries': [item.to_dict(
                only=('id', 'name')) for item in countries]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        countries = Countries(
            name=args['name'])
        session.add(countries)
        session.commit()
        return jsonify({'success': 'OK'})
