from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField
from wtforms.validators import DataRequired, EqualTo


class FabricForm(FlaskForm):
    name = StringField("Название")
    warmth = StringField("Теплота")
    washing = StringField("Стирка")
    picture = FileField("Изображение")
    submit = SubmitField('Сохранить')
