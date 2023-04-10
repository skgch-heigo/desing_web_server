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

from data.constants.tables_inf import TABLES

from data.forms.login_in import LoginInForm
from data.forms.registration_form import RegisterForm


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=365
)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


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
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     jobs = db_sess.query(Jobs).filter((Jobs.user == current_user) | (Jobs.is_finished != True))
    # else:
    #     jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)
    return render_template("index.html", title="Designer help")


@app.route("/show/<table>/<int:id_>")
def element_information(table, id_):
    if table not in TABLES:
        abort(404)
    if table == "Wardrobe":
        pass
    if table == "users":
        pass
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginInForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        # print(form.password.data)
        # если вам скучно, то разкомментируйте эту^ строку
        # запустите сервер и отправьте ссылку в классный чат с просьбой потестить
        # 100% кто-нибудь зарегистрируется с настоящими почтой и паролем (уже такое было)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login_in.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reg():
    form = RegisterForm()
    if form.validate_on_submit():
        ans = {"name": "", "email": "", "password": ""}
        for i in ans:
            if i in request.form:
                ans[i] = request.form[i]
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('used_email.html')  # если пытаться зарегистрироваться с почтой, которая уже есть
        user = User()
        user.name = ans["name"]
        user.email = ans["email"]
        user.hashed_password = generate_password_hash(ans["password"])
        # print([ans["password"]], user.hashed_password, generate_password_hash(ans["password"]))
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect("/")
    return render_template('user_form.html', title='Регистрация', form=form)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 400'}), 400)


@app.errorhandler(405)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 405'}), 405)


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
