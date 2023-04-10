import datetime
import os
import random

from flask import jsonify, url_for
from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import abort, Api

from werkzeug.security import generate_password_hash

from data.models.additional import Countries
from data.models.user import User

from data.models import db_session
from data.resources import collars_resource

from data.constants.tables_inf import TABLES, TABLES_CLASSES, FIELDS

from data.forms.login_in import LoginInForm
from data.forms.registration_form import RegisterForm

from data.maps import finder


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


def main():
    for i in os.listdir(os.path.join('temp', "pictures")):
        if i != "information.txt":
            os.remove("temp/pictures/" + i)
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
    db_sess = db_session.create_session()
    if table not in TABLES:
        abort(404)
    obj = db_sess.query(TABLES_CLASSES[table]).filter(TABLES_CLASSES[table].id == id_).first()
    if table == "Wardrobe":
        if not current_user or not obj.owner == current_user.id:
            abort(403)
    if table == "users":
        if not current_user or current_user.access != 3:
            abort(403)
    fields = FIELDS[table]
    data = {}
    for i in fields:
        data[i] = getattr(obj, i)
    if table in ["Upper_body", "Lower_body", "Hats", "Boots"]:
        country = db_sess.query(Countries).filter(Countries.id == obj.origin).first()
        ll_span = finder.get_ll_span(country.name)
        coords = finder.get_coords(country.name)
        map_pic = finder.get_map(*ll_span, (str(coords[0]) + "," + str(coords[1]), "pm2bll"))
        random_int = random.randint(0, 1000000)
        with open(f"temp/pictures/map_picture{random_int}.png", "wb") as f:
            f.write(map_pic)
        data["map"] = url_for('temp', filename='pictures/map_picture{random_int}.png')
    return render_template("elem_information", title="Информация", data=data)


@app.route("/info/<int:id>")
@login_required
def info(id_):
    if current_user and current_user.id == id_:
        return redirect("/show/users/" + str(id_))
    abort(403)


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
                               form=form, title="Неудача")
    return render_template('login_in.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
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


@app.errorhandler(403)
def access_denied(_):
    return make_response(jsonify({'error': 'Access denied 403'}), 403)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Not found 404'}), 404)


@app.errorhandler(405)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request 405'}), 405)


if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
