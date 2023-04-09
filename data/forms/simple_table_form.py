from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired, EqualTo


class SimpleForm(FlaskForm):
    name = StringField("Название")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')