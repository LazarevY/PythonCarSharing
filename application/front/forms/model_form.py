from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label
from wtforms.validators import DataRequired


class ModelForm(FlaskForm):
    model_name = StringField('Model name')
    brand_name = SelectField('Select Brand', coerce=int)
    models = SelectField('Available models', choices=["1"])
    model_submit = SubmitField('Add Model', _name="model_submit")
    view_models = SubmitField('View models for brand', validators=None)

    def set_brands(self, brands: list):
        self.brand_name.choices = brands

    def set_models(self, models: list):
        self.models.choices = models
