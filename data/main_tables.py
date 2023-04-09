import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class Boots(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Boots'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    season = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Seasons.id"), nullable=True)
    origin = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Countries.id"), nullable=True)
    appearance_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_end = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    heel = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Heels.id"), nullable=True)
    clasp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Clasps.id"), nullable=True)
    features = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class Hats(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Hats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    season = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Seasons.id"), nullable=True)
    origin = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Countries.id"), nullable=True)
    appearance_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_end = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    brim = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Brims.id"), nullable=True)
    features = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class LowerBody(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Lower_body'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    season = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Seasons.id"), nullable=True)
    origin = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Countries.id"), nullable=True)
    appearance_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_end = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    fit = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Fits.id"), nullable=True)
    clasp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Clasps.id"), nullable=True)
    length = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Trouser_lengths.id"), nullable=True)
    features = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)


class UpperBody(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Upper_body'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    season = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Seasons.id"), nullable=True)
    origin = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Countries.id"), nullable=True)
    appearance_year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_start = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    popularity_end = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sleeves = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Sleeves.id"), nullable=True)
    clasp = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Clasps.id"), nullable=True)
    collar = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Collars.id"), nullable=True)
    hood = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    lapels = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Lapels.id"), nullable=True)
    pockets = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    fitted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    features = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    deleted = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
