import sqlalchemy
from data.models.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Countries(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Countries'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Fits(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Fits'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Seasons(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Seasons'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Sizes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Sizes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    

class Types(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Types'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)