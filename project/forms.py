from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SearchField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(min=2, max=20)], render_kw={"placeholder": "Enter username here.."})
    email = StringField('Email:', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter email here.."})
    password = PasswordField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Enter password here.."})
    confirm_password = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm password here.."})
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()], render_kw={"placeholder": "Enter username here.."})
    password = PasswordField('Password:', validators=[DataRequired()], render_kw={"placeholder": "Enter password here.."})
    remember = BooleanField('Remember Me:')
    submit = SubmitField('Log In')