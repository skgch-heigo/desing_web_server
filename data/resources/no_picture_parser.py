from flask_restful import reqparse, abort, Api, Resource

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)

parser2 = reqparse.RequestParser()
parser2.add_argument('name', required=False, type=str)