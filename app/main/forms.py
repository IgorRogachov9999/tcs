from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Find')
