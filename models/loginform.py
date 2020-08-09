from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    id = StringField('ID', [
        DataRequired(message='ID는 필수 항목입니다.'),

    ])
    pw = PasswordField('Password', [
        DataRequired(message='Password는 필수 항목입니다.'),
    ])
    submit = SubmitField('로그인')


class SignupForm(FlaskForm):
    id = StringField('ID', [
        DataRequired(message='ID는 필수 항목입니다.'),
        Length(min=6, message='%(min)d글자 이상 입력해주세요.')
    ])
    pw = PasswordField('Password', [
        DataRequired(message='Password는 필수 항목입니다.'),
        Length(min=6, message='%(min)d글자 이상 입력해주세요.')
    ])
    email = StringField('Email', [
        DataRequired(message="Email은 필수 항목입니다.")
    ])
    submit = SubmitField('회원가입')