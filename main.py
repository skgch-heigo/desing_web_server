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

from data.user import User
from data.simple_tables import Collars

from data import db_session
from data import collars_resource


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

def main():
    db_session.global_init("db/designer_base.db")
    # app.register_blueprint(users_api.blueprint)
    # app.register_blueprint(jobs_api.blueprint)
    # для списка объектов
    api.add_resource(collars_resource.CollarsListResource, '/api/v2/collars')
    # для одного объекта
    api.add_resource(collars_resource.CollarsResource, '/api/v2/collars/<int:collars_id>')
    app.run()



@app.route("/")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     jobs = db_sess.query(Jobs).filter((Jobs.user == current_user) | (Jobs.is_finished != True))
    # else:
    #     jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)
    return render_template("index.html")


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 400'}), 400)


@app.errorhandler(405)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 405'}), 405)


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
