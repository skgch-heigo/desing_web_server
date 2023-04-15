from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField


class FabricsForm(FlaskForm):
    name = StringField("Название")
    warmth = StringField("Теплота")
    washing = StringField("Стирка")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')
