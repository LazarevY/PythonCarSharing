from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label
from wtforms.validators import DataRequired, Optional

from application.extend.EscapeStringField import EscapeStringField


class ModelForBrand(FlaskForm):
    brand = EscapeStringField('Brand', validators=[DataRequired()])
    submit = SubmitField('Test')
