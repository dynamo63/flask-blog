from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileField
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flaskBlog.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data)
        if user:
            raise ValidationError('This username exists already!!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data)
        if user:
            raise ValidationError('This email is already taken !')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'],'Images Only!!(jpg or png)')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username exists already!!')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already taken !')