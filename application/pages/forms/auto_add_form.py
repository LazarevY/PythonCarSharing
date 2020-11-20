from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Regexp, NumberRange

from app_context import db
from application.database.modeles.auto_brand import AutoBrand
from application.extend.EscapeStringField import EscapeStringField


class AutoAdd(FlaskForm):
    brand_select = QuerySelectField('Brand',
                                    query_factory=lambda: db().query(AutoBrand).all(),
                                    get_pk=lambda brand: brand.brand_id,
                                    get_label=lambda brand: brand.brand_name)
    model_select = SelectField(coerce=int, validators=[DataRequired()], validate_choice=False)
    number = EscapeStringField(validators=[DataRequired(), Regexp(r'[а-я]\d\d\d[а-я][а-я]\d\dRUS', message='Regex')])
    mileage = IntegerField(validators=[DataRequired()])
    quality = IntegerField(validators=[DataRequired(), NumberRange(min=0, max=50, message="Quality")])
    submit = SubmitField('Add auto')

