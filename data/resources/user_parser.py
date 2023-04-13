from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('email', required=True)
parser.add_argument("hashed_password", required=True)

parser2 = reqparse.RequestParser()
parser2.add_argument('name', required=False)
parser2.add_argument('email', required=False)
parser2.add_argument("hashed_password", required=False)