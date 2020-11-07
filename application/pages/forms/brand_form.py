from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label
from wtforms.validators import DataRequired


class BrandForm(FlaskForm):
    new_brand_name = StringField('Brand Name', validators=[DataRequired()])
    brand_submit = SubmitField('Add new Brand', _name="brand_submit")
    error_string = ""
