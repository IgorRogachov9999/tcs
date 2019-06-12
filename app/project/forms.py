from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField


class ManagerForm(FlaskForm):
    manager = BooleanField('Manager')
    submit = SubmitField('Set')