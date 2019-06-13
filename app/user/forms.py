from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import BooleanField, SubmitField, SelectField, \
                    StringField, TextAreaField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Edit')


    def validate_username(self, username):
        if username != current_user.username:
            user = User.get_user_by_username(username)
            if user is not None:
                raise ValidationError('Please use a different username.')


    def validate_email(self, email):
        if email != current_user.email:
            user = User.get_user_by_email()
            if user is not None:
                raise ValidationError('Please use a different email address.')


class AddToProjectForm(FlaskForm):
    project = SelectField('Project', choices=[])
    submit = SubmitField('Add')