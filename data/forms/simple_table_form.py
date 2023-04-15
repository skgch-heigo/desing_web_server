from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo
from flask_wtf.file import FileField


class SimpleForm(FlaskForm):
    name = StringField("Название")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')