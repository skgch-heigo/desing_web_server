from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField, IntegerField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField


class UpperBodyForm(FlaskForm):
    name = StringField("Название")
    season = SelectField("Сезон")
    origin = SelectField("Место происхождения")
    appearance_year = IntegerField("Год появления")
    popularity_start = IntegerField("Начало популярности")
    popularity_end = IntegerField("Конец популярности")
    sleeves = SelectField("Рукава")
    clasp = SelectField("Метод застегивания")
    collar = SelectField("Воротник")
    hood = BooleanField("Капюшон")
    lapels = SelectField("Лацканы")
    pockets = BooleanField("Карманы")
    fitted = BooleanField("Приталенный")
    features = StringField("Дополнительная информация")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')


class LowerBodyForm(FlaskForm):
    name = StringField("Название")
    season = SelectField("Сезон")
    origin = SelectField("Место происхождения")
    appearance_year = IntegerField("Год появления")
    popularity_start = IntegerField("Начало популярности")
    popularity_end = IntegerField("Конец популярности")
    fit = SelectField("Посадка")
    clasp = SelectField("Метод застегивания")
    length = SelectField("Длина")
    features = StringField("Дополнительная информация")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')


class BootsForm(FlaskForm):
    name = StringField("Название")
    season = SelectField("Сезон")
    origin = SelectField("Место происхождения")
    appearance_year = IntegerField("Год появления")
    popularity_start = IntegerField("Начало популярности")
    popularity_end = IntegerField("Конец популярности")
    heel = SelectField("Каблук")
    clasp = SelectField("Метод застегивания")
    features = StringField("Дополнительная информация")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')


class HatsForm(FlaskForm):
    name = StringField("Название")
    season = SelectField("Сезон")
    origin = SelectField("Место происхождения")
    appearance_year = IntegerField("Год появления")
    popularity_start = IntegerField("Начало популярности")
    popularity_end = IntegerField("Конец популярности")
    brim = SelectField("Поля")
    features = StringField("Дополнительная информация")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')
