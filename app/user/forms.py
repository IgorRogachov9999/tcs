from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], 
                            default=current_user.username)
    email = StringField('Email', validators=[DataRequired(), Email()],
                        default=current_user.email)
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
