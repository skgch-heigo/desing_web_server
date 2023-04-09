import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Countries(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Countries'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    type_ = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    color = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fabric = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    pattern = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
