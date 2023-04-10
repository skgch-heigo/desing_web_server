from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField, SelectField
from wtforms.validators import DataRequired, EqualTo


class WardrobeForm(FlaskForm):
    name = SelectField("Название")
    color = StringField("Цвет")
    size = SelectField("Размер")
    fabric = SelectField("Ткань")
    pattern = SelectField("Узор")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')
