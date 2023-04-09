import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    access = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)

    def check_password(self, password):
        # hasher.update(bytes(password, "utf-8"))
        passw = generate_password_hash(password)
        print([password], passw, self.hashed_password)
        if check_password_hash(self.hashed_password, password):
            return True
        return False
