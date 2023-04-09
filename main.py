from flask import Flask, render_template, redirect, request, abort, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import jsonify
from flask_restful import abort, Api

# from forms.jobs import JobsForm
# from forms.user import RegisterForm, LoginForm
from data.user import User
from data.simple_tables import Collars

from data import db_session
from data import collars_resource

app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/designer_base.db")
    # app.register_blueprint(users_api.blueprint)
    # app.register_blueprint(jobs_api.blueprint)
    # для списка объектов
    api.add_resource(collars_resource.CollarsListResource, '/api/v2/collars')
    # для одного объекта
    api.add_resource(collars_resource.CollarsResource, '/api/v2/collars/<int:collars_id>')
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     jobs = db_sess.query(Jobs).filter((Jobs.user == current_user) | (Jobs.is_finished != True))
    # else:
    #     jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)
    return render_template("index.html")


if __name__ == '__main__':
    main()
