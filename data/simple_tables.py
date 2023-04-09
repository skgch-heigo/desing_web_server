import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Brims(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Brims'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Clasps(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Clasps'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Collars(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Collars'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Heels(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Heels'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Lapels(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Lapels'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Patterns(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Patterns'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Sleeves(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Sleeves'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class TrouserLengths(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Trouser_lengths'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Lapels(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Lapels'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
