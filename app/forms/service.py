from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField, SubmitField
from wtforms.validators import ValidationError, Optional, InputRequired


TYPE_CHOICES = [
    ('outdoor', 'Outdoor'),
    ('indoor', 'Indoor'),
]


class ServiceForm(FlaskForm):
    name = StringField('Title*', validators=[InputRequired()])
    description = StringField('Description', validators=[Optional()])
    location = StringField('Location*', validators=[InputRequired()])
    type = SelectField('Type*', choices=TYPE_CHOICES, validators=[InputRequired()])
    workers_needed = IntegerField('Workers Needed*', validators=[InputRequired()])
    start_date = StringField('Start Date*', validators=[InputRequired()])
    end_date = StringField('End Date*', validators=[InputRequired()])
    submit = SubmitField('Submit')
