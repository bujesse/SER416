from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Optional, InputRequired


class DonationForm(FlaskForm):
    donation_amount = StringField('Donation Amount*', validators=[InputRequired()])
    card_number = StringField('Credit Card Number', validators=[InputRequired()])
    exp_date = StringField('Expiration Date', validators=[InputRequired()])
    cvv = StringField('CVV*', validators=[InputRequired()])
    submit = SubmitField('Submit')
