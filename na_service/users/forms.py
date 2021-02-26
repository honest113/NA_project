from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms import validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user

from na_service import bcrypt
from na_service.models import User




class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[validators.Regexp(r'^[\w.@+-]+$'), DataRequired(), Length(min=3, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message="Confirm Password must be same with Password!")])
    submit = SubmitField("Sign Up!")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.Regexp(r'^[\w.@+-]+$'), DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password', message="Confirm Password must be same with Password!")])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")
        
    def validate_password(self, password):
        if bcrypt.check_password_hash(current_user.password, password.data):
            raise ValidationError('Password must not be same old password')

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email! You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password!")