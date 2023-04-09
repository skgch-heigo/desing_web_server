import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Fabrics(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Fabrics'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    warmth = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    washing = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
