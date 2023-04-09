import datetime
import json
import os

from flask import Flask, url_for, render_template, redirect, request, make_response, session, jsonify
import flask
from flask import Flask, url_for, render_template, redirect, request, make_response, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import reqparse, abort, Api, Resource

from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session


db_session.global_init("db/designer_base.db")
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def index():
    # return render_template('base.html')
    return "Hello!"


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found 404'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 400'}), 400)


@app.errorhandler(405)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 405'}), 405)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
