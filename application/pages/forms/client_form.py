from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label, DecimalField
from wtforms.validators import DataRequired, Optional, NumberRange

from application.extend.EscapeStringField import EscapeStringField


class ClientForm(FlaskForm):
    name = EscapeStringField('Your name', validators=[DataRequired()])
    surname = EscapeStringField('Your surname', validators=[DataRequired()])
    passport = DecimalField('Passport serial and number',
                            validators=[DataRequired(),
                                        NumberRange(min=10**9, max=10**10 - 1, message='This field must contain 10 digits')])
    drive_license = DecimalField('Drive license serial and number',
                                 validators=[DataRequired(),
                                             NumberRange(min=10**9, max=10**10 - 1, message='This field must contain 10 digits')])
    submit = SubmitField('Register')
