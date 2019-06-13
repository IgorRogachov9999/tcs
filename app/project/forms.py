from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField, SelectField, \
                    StringField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from wtforms.fields.html5 import DateTimeLocalField


class ManagerForm(FlaskForm):
    manager = BooleanField('Manager')
    submit = SubmitField('Set')


class AddTaskForm(FlaskForm):
    description = TextAreaField('Description', validators=[
        DataRequired(), Length(min=1, max=250)])
    deathline = DateTimeLocalField('Dethline', 
                        format='%m/%d/%y', validators=[DataRequired()])
    user = SelectField('Developer', choices=[])
    submit = SubmitField('Add')

    