from flask import abort

from flask import jsonify

from data.models.simple_tables import Collars
from data.models import db_session

from flask_restful import abort, Resource, reqparse
parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('picture', required=True)
parser.add_argument('deleted', required=True, type=bool)


def abort_if_collars_not_found(collars_id):
    session = db_session.create_session()
    collars = session.query(Collars).get(collars_id)
    if not collars:
        abort(404, message=f"Collar {collars_id} not found")


class CollarsResource(Resource):
    def get(self, collars_id):
        abort_if_collars_not_found(collars_id)
        session = db_session.create_session()
        collars = session.query(Collars).get(collars_id)
        return jsonify({'collar': collars.to_dict(
            only=('name', 'picture', 'deleted'))})

    def delete(self, collars_id):
        abort_if_collars_not_found(collars_id)
        session = db_session.create_session()
        collars = session.query(Collars).get(collars_id)
        session.delete(collars)
        session.commit()
        return jsonify({'success': 'OK'})


class CollarsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        collars = session.query(Collars).all()
        return jsonify({'collars': [item.to_dict(
            only=('id', 'name', 'picture', 'deleted')) for item in collars]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        collars = Collars(
            name=args['name'],
            picture=args['picture'],
            deleted=args['deleted'])
        session.add(collars)
        session.commit()
        return jsonify({'success': 'OK'})