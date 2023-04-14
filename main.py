import datetime
import os
import random

from flask import jsonify, url_for
from flask import Flask, render_template, redirect, request, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from flask_restful import abort, Api

from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from data.forms.NoPictureForm import NoPictureForm
from data.forms.clothes_forms import HatsForm, BootsForm, LowerBodyForm, UpperBodyForm
from data.forms.fabrics_form import FabricsForm
from data.forms.filter_form import FilterForm
from data.forms.simple_table_form import SimpleForm
from data.forms.wardrobe_form import WardrobeForm
from data.models.additional import Countries, Types, Sizes, Seasons, Fits
from data.models.fabrics import Fabrics
from data.models.main_tables import Hats, Boots, LowerBody, UpperBody
from data.models.simple_tables import Patterns, Brims, Heels, Clasps, TrouserLengths, Sleeves, Collars, Lapels
from data.models.user import User

from data.models import db_session
from data.models.wardrobe import Wardrobe
from data.resources import collars_resource, brims_resource, heels_resource, clasps_resource, \
    lapels_resource, sleeves_resource, patterns_resource, trouser_lengths_resource, \
    countries_resource, fits_resource, seasons_resource, sizes_resource, types_resource, \
    users_resource, \
    boots_resource, hats_resource, lower_body_resource, upper_body_resource, \
    fabrics_resource, wardrobe_resource

from data.constants.tables_inf import TABLES, TABLES_CLASSES, FIELDS, RELATIONS, NO_PICTURE, SIMPLE, TRANSLATION

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
    api.add_resource(collars_resource.CollarsListResource, '/api/collars')
    api.add_resource(brims_resource.BrimsListResource, '/api/brims')
    api.add_resource(clasps_resource.ClaspsListResource, '/api/clasps')
    api.add_resource(heels_resource.HeelsListResource, '/api/heels')
    api.add_resource(lapels_resource.LapelsListResource, '/api/lapels')
    api.add_resource(sleeves_resource.SleevesListResource, '/api/sleeves')
    api.add_resource(trouser_lengths_resource.TrouserLengthsListResource, '/api/trouserlengths')
    api.add_resource(patterns_resource.PatternsListResource, '/api/patterns')
    api.add_resource(users_resource.UsersListResource, '/api/users')
    api.add_resource(fits_resource.FitsListResource, '/api/fits')
    api.add_resource(seasons_resource.SeasonsListResource, '/api/seasons')
    api.add_resource(countries_resource.CountriesListResource, '/api/countries')
    api.add_resource(sizes_resource.SizesListResource, '/api/sizes')
    api.add_resource(types_resource.TypesListResource, '/api/types')
    api.add_resource(boots_resource.BootsListResource, '/api/boots')
    api.add_resource(hats_resource.HatsListResource, '/api/hats')
    api.add_resource(lower_body_resource.LowerBodyListResource, '/api/lower_body')
    api.add_resource(upper_body_resource.UpperBodyListResource, '/api/upper_body')
    api.add_resource(fabrics_resource.FabricsListResource, '/api/fabrics')
    api.add_resource(wardrobe_resource.WardrobeListResource, '/api/wardrobe')

    # для одного объекта
    api.add_resource(collars_resource.CollarsResource, '/api/collars/<int:collars_id>')
    api.add_resource(brims_resource.BrimsResource, '/api/brims/<int:brims_id>')
    api.add_resource(clasps_resource.ClaspsResource, '/api/clasps/<int:clasps_id>')
    api.add_resource(heels_resource.HeelsResource, '/api/heels/<int:heels_id>')
    api.add_resource(lapels_resource.LapelsResource, '/api/lapels/<int:lapels_id>')
    api.add_resource(sleeves_resource.SleevesResource, '/api/sleeves/<int:sleeves_id>')
    api.add_resource(trouser_lengths_resource.TrouserLengthsResource, '/api/trouserlengths/<int:trouserlengths_id>')
    api.add_resource(patterns_resource.PatternsResource, '/api/patterns/<int:patterns_id>')
    api.add_resource(users_resource.UsersResource, '/api/users/<int:users_id>')
    api.add_resource(countries_resource.CountriesResource, '/api/countries/<int:countries_id>')
    api.add_resource(fits_resource.FitsResource, '/api/fits/<int:fits_id>')
    api.add_resource(seasons_resource.SeasonsResource, '/api/seasons/<int:seasons_id>')
    api.add_resource(sizes_resource.SizesResource, '/api/sizes/<int:sizes_id>')
    api.add_resource(types_resource.TypesResource, '/api/types/<int:types_id>')
    api.add_resource(boots_resource.BootsResource, '/api/boots/<int:boots_id>')
    api.add_resource(hats_resource.HatsResource, '/api/hats/<int:hats_id>')
    api.add_resource(lower_body_resource.LowerBodyResource, '/api/lower_body/<int:lower_body_id>')
    api.add_resource(upper_body_resource.UpperBodyResource, '/api/upper_body/<int:upper_body_id>')
    api.add_resource(fabrics_resource.FabricsResource, '/api/fabrics/<int:fabrics_id>')
    api.add_resource(wardrobe_resource.WardrobeResource, '/api/wardrobe/<int:wardrobe_id>')

    app.run()


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    # if current_user.is_authenticated:
    #     jobs = db_sess.query(Jobs).filter((Jobs.user == current_user) | (Jobs.is_finished != True))
    # else:
    #     jobs = db_sess.query(Jobs).filter(Jobs.is_finished != True)
    return render_template("index.html", title="Designer help", music=url_for("static", filename="music/ragtime.mp3"))


@app.route("/show/<table>/<int:id_>")
def element_information(table, id_):
    db_sess = db_session.create_session()
    if table not in TABLES:
        abort(404)
    obj = db_sess.query(TABLES_CLASSES[table]).filter(TABLES_CLASSES[table].id == id_).first()
    if not obj:
        abort(404)
    if table == "Wardrobe":
        if not current_user or not obj.owner == current_user.id and not current_user.access == 3:
            abort(403)
    if table == "users":
        if not current_user or current_user.access != 3:
            abort(403)
    fields = FIELDS[table]
    data = {}
    for i in fields:
        data[i] = getattr(obj, i)
    for i in fields:
        if i in RELATIONS:
            data[i] = db_sess.query(TABLES_CLASSES[RELATIONS[i]]).filter(TABLES_CLASSES[RELATIONS[i]].id ==
                                                                         data[i]).first()
    if "picture" in fields:
        data["picture"] = url_for('static', filename=f'img/{obj.picture}')
    if table in ["Upper_body", "Lower_body", "Hats", "Boots"]:
        country = db_sess.query(Countries).filter(Countries.id == obj.origin).first()
        ll_span = finder.get_ll_span(country.name)
        coords = finder.get_coords(country.name)
        map_pic = finder.get_map(*ll_span, (str(coords[0]) + "," + str(coords[1]), "pm2bll"))
        random_int = random.randint(0, 1000000)
        with open(f"temp/pictures/map_picture{random_int}.png", "wb") as f:
            f.write(map_pic)
        data["map"] = url_for('temp', filename=f'pictures/map_picture{random_int}.png')
    return render_template("elem_information", title="Информация", data=data)


@app.route("/info/<int:id>")
@login_required
def info(id_):
    if current_user and current_user.id == id_:
        return redirect("/show/users/" + str(id_))
    abort(403)


@app.route("/wardrobe/<sort_str>", methods=['GET', 'POST'])
@login_required
def wardrobe(sort_str):
    form = FilterForm()
    if form.validate_on_submit():
        return redirect("/wardrobe/" + (request.form["sort_str"] if "sort_str" in request.form else ""))
    db_sess = db_session.create_session()
    results = db_sess.query(Wardrobe).filter((Wardrobe.owner == current_user.id) & (Wardrobe.deleted == 0)).all()
    data = []
    for obj in results:
        if sort_str in db_sess.get(TABLES_CLASSES[db_sess.get(Types, obj.type_).name], obj.id):
            fields = FIELDS["Wardrobe"]
            del fields[-1]
            data = {}
            for i in fields:
                data[i] = getattr(obj, i)
            for i in fields:
                if i in RELATIONS:
                    data[i] = db_sess.query(TABLES_CLASSES[RELATIONS[i]]).filter(TABLES_CLASSES[RELATIONS[i]].id ==
                                                                                 data[i]).first()
    return render_template("wardrobe.html", data=data, title="Гардероб", form=form)


@app.route("/additional/<type_>/<sort_str>", methods=['GET', 'POST'])
def additional(type_, sort_str):
    if not (type_ in NO_PICTURE or type_ in SIMPLE or type_ == "Fabrics"):
        abort(404)
    form = FilterForm()
    if form.validate_on_submit():
        return redirect(f"/additional/{type_}/" + (request.form["sort_str"] if "sort_str" in request.form else ""))
    db_sess = db_session.create_session()
    table = TABLES_CLASSES[type_]
    results = db_sess.query(table).filter((table.deleted == 0) & (table.name.like(f'%{sort_str}%'))).all()
    data = []
    for obj in results:
        fields = FIELDS[type_]
        del fields[-1]
        data = {}
        for i in fields:
            data[i] = getattr(obj, i)
    if type_ in NO_PICTURE:
        return render_template("no_picture.html", data=data, title=TRANSLATION[type_], form=form)
    elif type_ in SIMPLE:
        return render_template("simple.html", data=data, title=TRANSLATION[type_], form=form)
    else:
        return render_template("fabrics.html", data=data, title=TRANSLATION[type_], form=form)


@login_required
@app.route("/users/<sort_str>", methods=['GET', 'POST'])
def users(sort_str):
    if current_user.access != 3:
        abort(403)
    form = FilterForm()
    if form.validate_on_submit():
        return redirect(f"/users/" + (request.form["sort_str"] if "sort_str" in request.form else ""))
    db_sess = db_session.create_session()
    results = db_sess.query(User).filter((User.deleted == 0) & (User.name.like(f'%{sort_str}%'))).all()
    data = []
    for obj in results:
        fields = FIELDS["users"]
        del fields[-1]
        del fields[2]
        data = {}
        for i in fields:
            data[i] = getattr(obj, i)
    return render_template("users.html", data=data, title="Пользователи", form=form)


@app.route("/clothes/<type_>/<sort_str>", methods=['GET', 'POST'])
def clothes(type_, sort_str):
    if type_ not in ["Boots", "Hats", "Lower_body", "Upper_body"]:
        abort(404)
    form = FilterForm()
    if form.validate_on_submit():
        return redirect(f"/clothes/{type_}/" + (request.form["sort_str"] if "sort_str" in request.form else ""))
    table = TABLES_CLASSES[type_]
    db_sess = db_session.create_session()
    results = db_sess.query(table).filter((table.deleted == 0) & (table.name.like(f'%{sort_str}%'))).all()
    data = []
    for obj in results:
        fields = FIELDS[type_]
        del fields[-1]
        data = {}
        for i in fields:
            data[i] = getattr(obj, i)
            if i in RELATIONS:
                data[i] = db_sess.query(TABLES_CLASSES[RELATIONS[i]]).filter(TABLES_CLASSES[RELATIONS[i]].id ==
                                                                             data[i]).first()
    if type_ == "Boots":
        return render_template("boots.html", data=data, title="Обувь", form=form)
    elif type_ == "Hats":
        return render_template("hats.html", data=data, title="Шляпы", form=form)
    elif type_ == "Upper_body":
        return render_template("upper_body.html", data=data, title="Верхняя одежда", form=form)
    return render_template("lower_body.html", data=data, title="Нижняя одежда", form=form)


@app.route("/additional/add/<type_>", methods=['GET', 'POST'])
@login_required
def additional_add(type_):
    if current_user.access < 2:
        abort(403)
    db_sess = db_session.create_session()
    if type_ in SIMPLE:
        form = SimpleForm()
        if form.validate_on_submit():
            obj = TABLES_CLASSES[type_]()
            obj.name = form.name.data
            if not os.path.exists(os.path.join("static", type_.lower())):
                os.mkdir(os.path.join("static", type_.lower()))
            where = "pic_" + obj.name
            if os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + obj.name)):
                i = 1
                while os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + obj.name + str(i))):
                    i += 1
                    where = "/pic_" + obj.name + str(i)
            with open(where, "wb") as f:
                f.write(form.picture.data)
            obj.picture = type_.lower() + where
            db_sess.add(obj)
            db_sess.commit()
            return redirect('/additional/' + type_)
        render_template("simple_add.html", form=form, title="Добавить " + TRANSLATION[type_])
    elif type_ in NO_PICTURE:
        form = NoPictureForm()
        if form.validate_on_submit():
            obj = TABLES_CLASSES[type_]()
            obj.name = form.name.data
            db_sess.add(obj)
            db_sess.commit()
            return redirect('/additional/' + type_)
        render_template("no_picture_add.html", form=form, title="Добавить " + TRANSLATION[type_])
    elif type_ == "Fabrics":
        form = FabricsForm()
        if form.validate_on_submit():
            obj = TABLES_CLASSES[type_]()
            obj.name = form.name.data
            obj.warmth = form.warmth.data
            obj.washing = form.washing.data
            if not os.path.exists(os.path.join("static", type_.lower())):
                os.mkdir(os.path.join("static", type_.lower()))
            where = "pic_" + obj.name
            if os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + obj.name)):
                i = 1
                while os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + obj.name + str(i))):
                    i += 1
                    where = "/pic_" + obj.name + str(i)
            with open(where, "wb") as f:
                f.write(form.picture.data)
            obj.picture = type_.lower() + where
            db_sess.add(obj)
            db_sess.commit()
            return redirect('/additional/' + type_)
        return render_template("fabrics_add.html", form=form, title="Добавить " + TRANSLATION[type_])
    abort(404)


@app.route("/additional/edit/<type_>/<int:id_>", methods=['GET', 'POST'])
@login_required
def additional_edit(type_, id_):
    if current_user.access < 2:
        abort(403)
    db_sess = db_session.create_session()
    old_obj = db_sess.get(TABLES_CLASSES[type_], id_)
    if not old_obj:
        abort(404)
    if type_ in SIMPLE:
        form = SimpleForm()
        if form.validate_on_submit():
            old_obj.name = form.name.data
            if os.path.exists("static/img/" + old_obj.picture):
                os.remove("static/img/" + old_obj.picture)
            if not os.path.exists(os.path.join("static", type_.lower())):
                os.mkdir(os.path.join("static", type_.lower()))
            where = "pic_" + old_obj.name
            if os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + old_obj.name)):
                i = 1
                while os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + old_obj.name + str(i))):
                    i += 1
                    where = "/pic_" + old_obj.name + str(i)
            with open(where, "wb") as f:
                f.write(form.picture.data)
            old_obj.picture = type_.lower() + where
            db_sess.commit()
            return redirect('/additional/' + type_)
        render_template("simple_edit.html", form=form, title="Изменить " + TRANSLATION[type_], old_oj=old_obj)
    elif type_ in NO_PICTURE:
        form = NoPictureForm()
        if form.validate_on_submit():
            old_obj.name = form.name.data
            db_sess.commit()
            return redirect('/additional/' + type_)
        render_template("no_picture_edit.html", form=form, title="Изменить " + TRANSLATION[type_], old_oj=old_obj)
    elif type_ == "Fabrics":
        form = FabricsForm()
        if form.validate_on_submit():
            old_obj.name = form.name.data
            old_obj.warmth = form.warmth.data
            old_obj.washing = form.washing.data
            if os.path.exists("static/img/" + old_obj.picture):
                os.remove("static/img/" + old_obj.picture)
            if not os.path.exists(os.path.join("static", type_.lower())):
                os.mkdir(os.path.join("static", type_.lower()))
            where = "pic_" + old_obj.name
            if os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + old_obj.name)):
                i = 1
                while os.path.exists(os.path.join("static/img", type_.lower() + "/pic_" + old_obj.name + str(i))):
                    i += 1
                    where = "/pic_" + old_obj.name + str(i)
            with open(where, "wb") as f:
                f.write(form.picture.data)
            old_obj.picture = type_.lower() + where
            db_sess.commit()
            return redirect('/additional/' + type_)
        return render_template("fabrics_edit.html", form=form, title="Изменить " + TRANSLATION[type_], old_oj=old_obj)
    abort(404)


@app.route("/wardrobe/add/<type_>", methods=['GET', 'POST'])
@login_required
def wardrobe_add(type_):
    if type_ not in TABLES:
        abort(404)
    table = TABLES_CLASSES[type_]
    if current_user.access < 2:
       abort(403)
    db_sess = db_session.create_session()
    names_opt = [i.name for i in db_sess.query(table).filter(table.deleted == 0).all()]
    size_opt = [i.name for i in db_sess.query(Sizes).filter(Sizes.deleted == 0).all()]
    fabric_opt = [i.name for i in db_sess.query(Fabrics).filter(Fabrics.deleted == 0).all()]
    pattern_opt = [i.name for i in db_sess.query(Patterns).filter(Patterns.deleted == 0).all()]
    form = WardrobeForm()
    form.name.choices = names_opt
    form.size.choices = size_opt
    form.fabric.choices = fabric_opt
    form.pattern.choices = pattern_opt
    if form.validate_on_submit():
        obj = Wardrobe()
        obj.type_ = type_
        obj.name = db_sess.query(table).filter(table.name == form.name.data, table.deleted == 0).first().id
        obj.color = form.color.data
        obj.size = db_sess.query(Sizes).filter(Sizes.name == form.size.data, Sizes.deleted == 0).first().id
        obj.fabric = db_sess.query(Fabrics).filter(Fabrics.name == form.fabric.data,
                                                   Fabrics.deleted == 0).first().id
        obj.pattern = db_sess.query(Patterns).filter(Patterns.name == form.pattern.data,
                                                     Patterns.deleted == 0).first().id
        obj.owner = current_user.id
        filename = secure_filename(form.picture.data.filename)
        if form.picture.data:
            print("!!")
            if not os.path.exists(os.path.join("static", "img/wardrobe")):
                os.mkdir(os.path.join("static", "img/wardrobe"))
            where = "pic_" + form.name.data + ".png"
            if os.path.exists(os.path.join("static/img", "wardrobe" + "/pic_" + form.name.data + ".png")):
                i = 1
                while os.path.exists(os.path.join("static/img", "wardrobe" + "/pic_" +
                                                                form.name.data + str(i) + ".png")):
                    i += 1
                    where = "/pic_" + form.name.data + str(i) + ".png"
            f = form.picture.data
            f.save(os.path.join("static/img/wardrobe", where))
            obj.picture = "wardrobe/" + where
        db_sess.add(obj)
        db_sess.commit()
        return redirect('/wardrobe/')
    return render_template("wardrobe_add.html", form=form, title="Добавить в гардероб")


@app.route("/wardrobe/edit/<int:id_>", methods=['GET', 'POST'])
@login_required
def wardrobe_edit(id_):
    db_sess = db_session.create_session()
    old_obj = db_sess.get(Wardrobe, id_)
    if not old_obj:
        abort(404)
    if current_user.access < 2:
        abort(403)
    table = TABLES_CLASSES[db_sess.get(Types, old_obj.type).name]
    old = {"name": db_sess.get(table, old_obj.name).name, "size": db_sess.get(Sizes, old_obj.size).name,
           "fabric": db_sess.get(Fabrics, old_obj.fabric).name, "pattern": db_sess.get(Patterns, old_obj.pattern).name}
    names_opt = [i.name for i in db_sess.query(table).filter(table.deleted == 0).all()]
    size_opt = [i.name for i in db_sess.query(Sizes).filter(Sizes.deleted == 0).all()]
    fabric_opt = [i.name for i in db_sess.query(Fabrics).filter(Fabrics.deleted == 0).all()]
    pattern_opt = [i.name for i in db_sess.query(Patterns).filter(Patterns.deleted == 0).all()]
    form = WardrobeForm()
    form.name.choices = names_opt
    form.size.choices = size_opt
    form.fabric.choices = fabric_opt
    form.pattern.choices = pattern_opt
    if form.validate_on_submit():
        old_obj.name = db_sess.query(table).filter(table.name == form.name.data, table.deleted == 0).first().id
        old_obj.color = form.color.data
        old_obj.size = db_sess.query(Sizes).filter(Sizes.name == form.size.data, Sizes.deleted == 0).first().id
        old_obj.fabric = db_sess.query(Fabrics).filter(Fabrics.name == form.fabric.data,
                                                       Fabrics.deleted == 0).first().id
        old_obj.pattern = db_sess.query(Patterns).filter(Patterns.name == form.pattern.data,
                                                         Patterns.deleted == 0).first().id
        if os.path.exists("static/img/" + old_obj.picture):
            os.remove("static/img/" + old_obj.picture)
        if not os.path.exists(os.path.join("static", "wardrobe")):
            os.mkdir(os.path.join("static", "wardrobe"))
        where = "pic_" + form.name.data
        if os.path.exists(os.path.join("static/img", "wardrobe" + "/pic_" + form.name.data)):
            i = 1
            while os.path.exists(os.path.join("static/img", "wardrobe" + "/pic_" + form.name.data + str(i))):
                i += 1
                where = "/pic_" + form.name.data + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        old_obj.picture = "wardrobe" + where
        db_sess.commit()
        return redirect('/wardrobe/')
    return render_template("wardrobe_edit.html", form=form, title="Изменить в гардеробе", old=old)


@app.route("/clothes/Hats/add", methods=['GET', 'POST'])
@login_required
def hats_add():
    if current_user.access < 2:
        abort(403)
    db_sess = db_session.create_session()
    form = HatsForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    brims_opt = db_sess.query(Brims).filter(Brims.deleted == 0).all()
    if form.validate_on_submit():
        obj = Hats()
        obj.name = form.name.data
        obj.appearance_year = int(form.appearance_year.data)
        obj.popularity_start = int(form.popularity_start.data)
        obj.popularity_end = int(form.popularity_end.data)
        obj.features = form.features.data
        obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data, Seasons.deleted == 0).first().id
        obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                     Countries.deleted == 0).first().id
        obj.brim = db_sess.query(Brims).filter(Brims.name == form.brim.data, Brims.deleted == 0).first().id
        if not os.path.exists(os.path.join("static", "hats")):
            os.mkdir(os.path.join("static", "hats"))
        where = "pic_" + obj.name
        if os.path.exists(os.path.join("static/img", "hats" + "/pic_" + obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "hats" + "/pic_" + obj.name + str(i))):
                i += 1
                where = "/pic_" + obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        obj.picture = "hats" + where
        db_sess.add(obj)
        db_sess.commit()
        return redirect('/clothes/hats/')
    return render_template("hats_add.html", form=form, title="Добавить Шляпы", brims=brims_opt,
                           origins=origin_opt, seasons=seasons_opt)


@app.route("/clothes/Hats/edit/<int:id_>", methods=['GET', 'POST'])
@login_required
def hats_edit(id_):
    db_sess = db_session.create_session()
    if current_user.access < 2:
        abort(403)
    old_obj = db_sess.get(Hats, id_)
    if not old_obj:
        abort(404)
    form = HatsForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    brims_opt = db_sess.query(Brims).filter(Brims.deleted == 0).all()
    if form.validate_on_submit():
        old_obj.name = form.name.data
        old_obj.appearance_year = int(form.appearance_year.data)
        old_obj.popularity_start = int(form.popularity_start.data)
        old_obj.popularity_end = int(form.popularity_end.data)
        old_obj.features = form.features.data
        old_obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data,
                                                       Seasons.deleted == 0).first().id
        old_obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                         Countries.deleted == 0).first().id
        old_obj.brim = db_sess.query(Brims).filter(Brims.name == form.brim.data, Brims.deleted == 0).first().id
        if os.path.exists("static/img/" + old_obj.picture):
            os.remove("static/img/" + old_obj.picture)
        if not os.path.exists(os.path.join("static", "hats")):
            os.mkdir(os.path.join("static", "hats"))
        where = "pic_" + old_obj.name
        if os.path.exists(os.path.join("static/img", "hats" + "/pic_" + old_obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "hats" + "/pic_" + old_obj.name + str(i))):
                i += 1
                where = "/pic_" + old_obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        old_obj.picture = "hats" + where
        db_sess.commit()
        return redirect('/clothes/hats/')
    return render_template("hats_edit.html", form=form, title="Изменить Шляпы", brims=brims_opt, old_obj=old_obj,
                           origins=origin_opt, seasons=seasons_opt)


@app.route("/clothes/Boots/add", methods=['GET', 'POST'])
@login_required
def boots_add():
    if current_user.access < 2:
        abort(403)
    db_sess = db_session.create_session()
    form = BootsForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    heel_opt = db_sess.query(Heels).filter(Heels.deleted == 0).all()
    clasp_opt = db_sess.query(Clasps).filter(Clasps.deleted == 0).all()
    if form.validate_on_submit():
        obj = Boots()
        obj.name = form.name.data
        obj.appearance_year = int(form.appearance_year.data)
        obj.popularity_start = int(form.popularity_start.data)
        obj.popularity_end = int(form.popularity_end.data)
        obj.features = form.features.data
        obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data, Seasons.deleted == 0).first().id
        obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                     Countries.deleted == 0).first().id
        obj.heel = db_sess.query(Heels).filter(Heels.name == form.heel.data, Heels.deleted == 0).first().id
        obj.clasp = db_sess.query(Clasps).filter(Clasps.name == form.clasp.data, Clasps.deleted == 0).first().id
        if not os.path.exists(os.path.join("static", "boots")):
            os.mkdir(os.path.join("static", "boots"))
        where = "pic_" + obj.name
        if os.path.exists(os.path.join("static/img", "boots" + "/pic_" + obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "boots" + "/pic_" + obj.name + str(i))):
                i += 1
                where = "/pic_" + obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        obj.picture = "boots" + where
        db_sess.add(obj)
        db_sess.commit()
        return redirect('/clothes/boots/')
    return render_template("boots_add.html", form=form, title="Добавить Обувь", heels=heel_opt, clasps=clasp_opt,
                           origins=origin_opt, seasons=seasons_opt)


@app.route("/clothes/Boots/edit/<int:id_>", methods=['GET', 'POST'])
@login_required
def boots_edit(id_):
    db_sess = db_session.create_session()
    if current_user.access < 2:
        abort(403)
    old_obj = db_sess.get(Boots, id_)
    if not old_obj:
        abort(404)
    form = BootsForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    heel_opt = db_sess.query(Heels).filter(Heels.deleted == 0).all()
    clasp_opt = db_sess.query(Clasps).filter(Clasps.deleted == 0).all()
    if form.validate_on_submit():
        old_obj.name = form.name.data
        old_obj.appearance_year = int(form.appearance_year.data)
        old_obj.popularity_start = int(form.popularity_start.data)
        old_obj.popularity_end = int(form.popularity_end.data)
        old_obj.features = form.features.data
        old_obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data,
                                                       Seasons.deleted == 0).first().id
        old_obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                         Countries.deleted == 0).first().id
        old_obj.heel = db_sess.query(Heels).filter(Heels.name == form.heel.data, Heels.deleted == 0).first().id
        old_obj.clasp = db_sess.query(Clasps).filter(Clasps.name == form.clasp.data, Clasps.deleted == 0).first().id
        if os.path.exists("static/img/" + old_obj.picture):
            os.remove("static/img/" + old_obj.picture)
        if not os.path.exists(os.path.join("static", "boots")):
            os.mkdir(os.path.join("static", "boots"))
        where = "pic_" + old_obj.name
        if os.path.exists(os.path.join("static/img", "boots" + "/pic_" + old_obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "boots" + "/pic_" + old_obj.name + str(i))):
                i += 1
                where = "/pic_" + old_obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        old_obj.picture = "boots" + where
        db_sess.commit()
        return redirect('/clothes/boots/')
    return render_template("boots_edit.html", form=form, title="Изменить Обувь", heels=heel_opt,
                           clasps=clasp_opt, old_obj=old_obj, origins=origin_opt, seasons=seasons_opt)


@app.route("/clothes/Lower_body/add", methods=['GET', 'POST'])
@login_required
def lower_body_add():
    if current_user.access < 2:
        abort(403)
    db_sess = db_session.create_session()
    form = LowerBodyForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    clasp_opt = db_sess.query(Clasps).filter(Clasps.deleted == 0).all()
    fit_opt = db_sess.query(Fits).filter(Fits.deleted == 0).all()
    length_opt = db_sess.query(TrouserLengths).filter(TrouserLengths.deleted == 0).all()
    if form.validate_on_submit():
        obj = LowerBody()
        obj.name = form.name.data
        obj.appearance_year = int(form.appearance_year.data)
        obj.popularity_start = int(form.popularity_start.data)
        obj.popularity_end = int(form.popularity_end.data)
        obj.features = form.features.data
        obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data, Seasons.deleted == 0).first().id
        obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                     Countries.deleted == 0).first().id
        obj.clasp = db_sess.query(Clasps).filter(Clasps.name == form.clasp.data, Clasps.deleted == 0).first().id
        obj.length = db_sess.query(TrouserLengths).filter(TrouserLengths.name == form.lengh.data,
                                                          TrouserLengths.deleted == 0).first().id
        obj.fit = db_sess.query(Fits).filter(Fits.name == form.fit.data, Fits.deleted == 0).first().id
        if not os.path.exists(os.path.join("static", "lower_body")):
            os.mkdir(os.path.join("static", "lower_body"))
        where = "pic_" + obj.name
        if os.path.exists(os.path.join("static/img", "lower_body" + "/pic_" + obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "lower_body" + "/pic_" + obj.name + str(i))):
                i += 1
                where = "/pic_" + obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        obj.picture = "lower_body" + where
        db_sess.add(obj)
        db_sess.commit()
        return redirect('/clothes/lower_body/')
    return render_template("lower_body_add.html", form=form, title="Добавить Нижнюю Одежду", clasps=clasp_opt,
                           fits=fit_opt, lengths=length_opt, origins=origin_opt, seasons=seasons_opt)


@app.route("/clothes/Lower_body/edit/<int:id_>", methods=['GET', 'POST'])
@login_required
def lower_body_edit(id_):
    db_sess = db_session.create_session()
    if current_user.access < 2:
        abort(403)
    old_obj = db_sess.get(LowerBody, id_)
    if not old_obj:
        abort(404)
    form = LowerBodyForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    clasp_opt = db_sess.query(Clasps).filter(Clasps.deleted == 0).all()
    fit_opt = db_sess.query(Fits).filter(Fits.deleted == 0).all()
    length_opt = db_sess.query(TrouserLengths).filter(TrouserLengths.deleted == 0).all()
    if form.validate_on_submit():
        old_obj.name = form.name.data
        old_obj.appearance_year = int(form.appearance_year.data)
        old_obj.popularity_start = int(form.popularity_start.data)
        old_obj.popularity_end = int(form.popularity_end.data)
        old_obj.features = form.features.data
        old_obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data,
                                                       Seasons.deleted == 0).first().id
        old_obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                         Countries.deleted == 0).first().id
        old_obj.clasp = db_sess.query(Clasps).filter(Clasps.name == form.clasp.data, Clasps.deleted == 0).first().id
        old_obj.length = db_sess.query(TrouserLengths).filter(TrouserLengths.name == form.lengh.data,
                                                              TrouserLengths.deleted == 0).first().id
        old_obj.fit = db_sess.query(Fits).filter(Fits.name == form.fit.data, Fits.deleted == 0).first().id
        if os.path.exists("static/img/" + old_obj.picture):
            os.remove("static/img/" + old_obj.picture)
        if not os.path.exists(os.path.join("static", "lower_body")):
            os.mkdir(os.path.join("static", "lower_body"))
        where = "pic_" + old_obj.name
        if os.path.exists(os.path.join("static/img", "lower_body" + "/pic_" + old_obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "lower_body" + "/pic_" + old_obj.name + str(i))):
                i += 1
                where = "/pic_" + old_obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        old_obj.picture = "lower_body" + where
        db_sess.commit()
        return redirect('/clothes/lower_body/')
    return render_template("lower_body_edit.html", form=form, title="Изменить Нижнюю Одежду", clasps=clasp_opt,
                           fits=fit_opt, lengths=length_opt, old_obj=old_obj, origins=origin_opt, seasons=seasons_opt)


@app.route("/clothes/Upper_body/add", methods=['GET', 'POST'])
@login_required
def upper_body_add():
    if current_user.access < 2:
        abort(403)
    db_sess = db_session.create_session()
    form = UpperBodyForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    clasp_opt = db_sess.query(Clasps).filter(Clasps.deleted == 0).all()
    sleeves_opt = db_sess.query(Sleeves).filter(Sleeves.deleted == 0).all()
    collar_opt = db_sess.query(Collars).filter(Collars.deleted == 0).all()
    lapel_opt = db_sess.query(Lapels).filter(Lapels.deleted == 0).all()
    if form.validate_on_submit():
        obj = UpperBody()
        obj.name = form.name.data
        obj.appearance_year = int(form.appearance_year.data)
        obj.popularity_start = int(form.popularity_start.data)
        obj.popularity_end = int(form.popularity_end.data)
        obj.features = form.features.data
        obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data, Seasons.deleted == 0).first().id
        obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                     Countries.deleted == 0).first().id
        obj.clasp = db_sess.query(Clasps).filter(Clasps.name == form.clasp.data, Clasps.deleted == 0).first().id
        obj.sleeves = db_sess.query(Sleeves).filter(Sleeves.name == form.sleeves.data, Sleeves.deleted == 0).first().id
        obj.collar = db_sess.query(Collars).filter(Collars.name == form.collar.data, Collars.deleted == 0).first().id
        obj.lapels = db_sess.query(Lapels).filter(Lapels.name == form.lapels.data, Lapels.deleted == 0).first().id
        obj.hood = int(form.hood.data)
        obj.fitted = int(form.fitted.data)
        obj.pockets = int(form.pockets.data)
        if not os.path.exists(os.path.join("static", "upper_body")):
            os.mkdir(os.path.join("static", "upper_body"))
        where = "pic_" + obj.name
        if os.path.exists(os.path.join("static/img", "upper_body" + "/pic_" + obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "upper_body" + "/pic_" + obj.name + str(i))):
                i += 1
                where = "/pic_" + obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        obj.picture = "upper_body" + where
        db_sess.add(obj)
        db_sess.commit()
        return redirect('/clothes/upper_body/')
    return render_template("upper_body_add.html", form=form, title="Добавить Верхнюю Одежду", clasps=clasp_opt,
                           origins=origin_opt, seasons=seasons_opt, sleeves=sleeves_opt,
                           collars=collar_opt, lapels=lapel_opt)


@app.route("/clothes/Upper_body/edit/<int:id_>", methods=['GET', 'POST'])
@login_required
def upper_body_edit(id_):
    db_sess = db_session.create_session()
    if current_user.access < 2:
        abort(403)
    old_obj = db_sess.get(UpperBody, id_)
    if not old_obj:
        abort(404)
    form = UpperBodyForm()
    seasons_opt = db_sess.query(Seasons).filter(Seasons.deleted == 0).all()
    origin_opt = db_sess.query(Countries).filter(Countries.deleted == 0).all()
    clasp_opt = db_sess.query(Clasps).filter(Clasps.deleted == 0).all()
    sleeves_opt = db_sess.query(Sleeves).filter(Sleeves.deleted == 0).all()
    collar_opt = db_sess.query(Collars).filter(Collars.deleted == 0).all()
    lapel_opt = db_sess.query(Lapels).filter(Lapels.deleted == 0).all()
    if form.validate_on_submit():
        old_obj.name = form.name.data
        old_obj.appearance_year = int(form.appearance_year.data)
        old_obj.popularity_start = int(form.popularity_start.data)
        old_obj.popularity_end = int(form.popularity_end.data)
        old_obj.features = form.features.data
        old_obj.season = db_sess.query(Seasons).filter(Seasons.name == form.season.data,
                                                       Seasons.deleted == 0).first().id
        old_obj.origin = db_sess.query(Countries).filter(Countries.name == form.origin.data,
                                                         Countries.deleted == 0).first().id
        old_obj.clasp = db_sess.query(Clasps).filter(Clasps.name == form.clasp.data, Clasps.deleted == 0).first().id
        old_obj.sleeves = db_sess.query(Sleeves).filter(Sleeves.name == form.sleeves.data,
                                                        Sleeves.deleted == 0).first().id
        old_obj.collar = db_sess.query(Collars).filter(Collars.name == form.collar.data,
                                                       Collars.deleted == 0).first().id
        old_obj.lapels = db_sess.query(Lapels).filter(Lapels.name == form.lapels.data, Lapels.deleted == 0).first().id
        old_obj.hood = int(form.hood.data)
        old_obj.fitted = int(form.fitted.data)
        old_obj.pockets = int(form.pockets.data)
        if os.path.exists("static/img/" + old_obj.picture):
            os.remove("static/img/" + old_obj.picture)
        if not os.path.exists(os.path.join("static", "upper_body")):
            os.mkdir(os.path.join("static", "upper_body"))
        where = "pic_" + old_obj.name
        if os.path.exists(os.path.join("static/img", "upper_body" + "/pic_" + old_obj.name)):
            i = 1
            while os.path.exists(os.path.join("static/img", "upper_body" + "/pic_" + old_obj.name + str(i))):
                i += 1
                where = "/pic_" + old_obj.name + str(i)
        with open(where, "wb") as f:
            f.write(form.picture.data)
        old_obj.picture = "upper_body" + where
        db_sess.commit()
        return redirect('/clothes/upper_body/')
    return render_template("upper_body_edit.html", form=form, title="Изменить Верхнюю Одежду", clasps=clasp_opt,
                           origins=origin_opt, seasons=seasons_opt, sleeves=sleeves_opt,
                           collars=collar_opt, lapels=lapel_opt, old_obj=old_obj)


@app.route("/wardrobe/<int:id_>")
@login_required
def wardrobe_del(id_):
    db_sess = db_session.create_session()
    obj = db_sess.get(Wardrobe, id_)
    if not obj:
        abort(404)
    if obj.owner != current_user.id and not current_user.access == 3:
        abort(403)
    if os.path.exists("static/img/" + obj.picture):
        os.remove("static/img/" + obj.picture)
    db_sess.delete(obj)
    db_sess.commit()
    return redirect("/wardrobe/")


@app.route("/clothes/<type_>/<int:id_>")
@login_required
def clothes_del(type_, id_):
    db_sess = db_session.create_session()
    if type_ not in ["Boots", "Hats", "Lower_body", "Upper_body"]:
        abort(404)
    obj = db_sess.get(TABLES_CLASSES[type_], id_)
    if not obj:
        abort(404)
    if not current_user.access >= 2:
        abort(403)
    if os.path.exists("static/img/" + obj.picture):
        os.remove("static/img/" + obj.picture)
    db_sess.delete(obj)
    db_sess.commit()
    return redirect("/clothes/" + type_ + "/")


@app.route("/additional/<type_>/<int:id_>")
@login_required
def additional_del(type_, id_):
    db_sess = db_session.create_session()
    if not (type_ in NO_PICTURE or type_ in SIMPLE or type_ == "Fabrics"):
        abort(404)
    obj = db_sess.get(TABLES_CLASSES[type_], id_)
    if not obj:
        abort(404)
    if not current_user.access >= 2:
        abort(403)
    if (type_ in SIMPLE or type_ == "Fabrics") and os.path.exists("static/img/" + obj.picture):
        os.remove("static/img/" + obj.picture)
    db_sess.delete(obj)
    db_sess.commit()
    return redirect("/additional/" + type_ + "/")


@app.route("/users/<int:id_>")
@login_required
def users_del(id_):
    db_sess = db_session.create_session()
    obj = db_sess.get(User, id_)
    if not obj:
        abort(404)
    if not current_user.access == 3:
        abort(403)
    db_sess.delete(obj)
    db_sess.commit()
    return redirect("/users/")


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
