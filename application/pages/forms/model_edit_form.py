from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, Label, DecimalField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Optional
from app_context import app, db
from application.database.modeles.auto_brand import AutoBrand
from application.extend.EscapeStringField import EscapeStringField


class ModelEditForm(FlaskForm):
    brand_select = QuerySelectField('Brand',
                                    query_factory=lambda: db().query(AutoBrand).all(),
                                    get_pk=lambda brand: brand.brand_id,
                                    get_label=lambda brand: brand.brand_name)
    model_select = SelectField(coerce=int, validators=[DataRequired()])

    model_name = EscapeStringField('Model name', validators=[DataRequired()])
    model_brand = QuerySelectField('New brand',
                                   query_factory=lambda: db().query(AutoBrand).all(),
                                   get_pk=lambda brand: brand.brand_id,
                                   get_label=lambda brand: brand.brand_name)
    model_price = DecimalField('Price', validators=[DataRequired()])
    delete_submit = SubmitField('Delete model', validators=[Optional()])
    update_submit = SubmitField('Update model', validators=[Optional()])
