from flask_restful import reqparse, abort, Api, Resource


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)
parser.add_argument('season', required=True, type=int)
parser.add_argument("origin", required=True, type=int)
parser.add_argument('appearance_year', required=True, type=int)
parser.add_argument('popularity_start', required=True, type=int)
parser.add_argument('popularity_end', required=True, type=int)
parser.add_argument('sleeves', required=True, type=int)
parser.add_argument('clasp', required=True, type=int)
parser.add_argument('collar', required=True, type=int)
parser.add_argument('hood', required=True, type=bool)
parser.add_argument('lapels', required=True, type=int)
parser.add_argument('pockets', required=True, type=bool)
parser.add_argument('fitted', required=True, type=bool)
parser.add_argument('features', required=True, type=str)
parser.add_argument('picture', required=True, type=str)

parser2 = reqparse.RequestParser()
parser2.add_argument('name', required=False, type=str)
parser2.add_argument('season', required=False, type=int)
parser2.add_argument("origin", required=False, type=int)
parser2.add_argument('appearance_year', required=False, type=int)
parser2.add_argument('popularity_start', required=False, type=int)
parser2.add_argument('popularity_end', required=False, type=int)
parser2.add_argument('sleeves', required=False, type=int)
parser2.add_argument('clasp', required=False, type=int)
parser2.add_argument('collar', required=False, type=int)
parser2.add_argument('hood', required=False, type=bool)
parser2.add_argument('lapels', required=False, type=int)
parser2.add_argument('pockets', required=False, type=bool)
parser2.add_argument('fitted', required=False, type=bool)
parser2.add_argument('features', required=False, type=str)
parser2.add_argument('picture', required=False, type=str)