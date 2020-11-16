from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Regexp, NumberRange, Optional

from app_context import db
from application.database.modeles.auto_brand import AutoBrand


class AutoEdit(FlaskForm):
    brand_select = QuerySelectField('Brand',
                                    query_factory=lambda: db().query(AutoBrand).all(),
                                    get_pk=lambda brand: brand.brand_id,
                                    get_label=lambda brand: brand.brand_name)
    model_select = SelectField(coerce=int, validate_choice=False)
    number_select = SelectField(coerce=int, validate_choice=False)
    number = StringField(validators=[DataRequired()])
    mileage = IntegerField(validators=[DataRequired()])
    quality = IntegerField(validators=[DataRequired()])
    update_submit = SubmitField('Edit auto')
    delete_submit = SubmitField('Delete auto')
