from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label
from wtforms.validators import DataRequired, Optional

from application.extend.EscapeStringField import EscapeStringField


class ModelForm(FlaskForm):
    model_name = EscapeStringField('Model name', validators=[Optional()])
    brand_name = SelectField('Select Brand', coerce=int)
    models = SelectField('Available models', choices=[], validators=[Optional()])
    categories = SelectField('Model category', coerce=int, validators=[Optional()])
    model_submit = SubmitField('Add Model')
    view_models = SubmitField('View models for brand')
    delete_submit = SubmitField('Delete model')

    def set_brands(self, brands: list):
        self.brand_name.choices = brands
        self.brand_name.default = next(self.brand_name.iter_choices())

    def set_models(self, models: list):
        self.models.choices = models
