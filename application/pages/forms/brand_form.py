from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label
from wtforms.validators import DataRequired

from application.extend.EscapeStringField import EscapeStringField


class BrandForm(FlaskForm):
    new_brand_name = EscapeStringField('Brand Name', validators=[DataRequired()])
    brand_submit = SubmitField('Add new Brand', _name="brand_submit")
    error_string = ""
