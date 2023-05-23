from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[Email()])
    psw = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=100, message='Пароль должен содержать от 4 до 100 символов')])
    remember = BooleanField('Запомить', default=False)
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[Length(min=4, max=100, message='Имя должно быть от 4 до 30 символов')])
    email = StringField('Email:', validators=[Email('Некорректный email')])
    psw = PasswordField('Пароль:', validators=[DataRequired(), Length(min=4, max=100, message='Пароль должно быть от 4 до 30 символов')])
    psw2 = PasswordField('Повтор пароля:', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Регистрация')