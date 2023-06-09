from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, EqualTo, Email


class RegisterForm(FlaskForm):
    name = StringField("Имя", validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message="Пароли должны совпадать")])
    agreed = BooleanField("Прочел и согласен с Условиями пользования", validators=[DataRequired(message="Обязательно поле")])
    submit = SubmitField('Зарегистрироваться')
