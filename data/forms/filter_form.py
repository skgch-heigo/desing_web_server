from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Email


class FilterForm(FlaskForm):
    sort_str = StringField("Фильтрация по подстроке")
    submit = SubmitField('Фильтровать')
