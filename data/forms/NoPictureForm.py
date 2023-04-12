from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired, EqualTo


class NoPictureForm(FlaskForm):
    name = StringField("Название")
    submit = SubmitField('Сохранить')
