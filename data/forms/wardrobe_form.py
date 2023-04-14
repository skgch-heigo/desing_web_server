from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, EqualTo


class WardrobeForm(FlaskForm):
    name = SelectField("Название")
    color = StringField("Цвет")
    size = SelectField("Размер")
    fabric = SelectField("Ткань")
    pattern = SelectField("Узор")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')
