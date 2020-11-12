from flask import render_template

import app_context as a
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.model_price import ModelPrice

app = a.app()

db = a.db()


@app.route('/view/models')
def view_models():
    models_q = db \
        .query(AutoModel) \
        .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id) \
        .join(ModelPrice, ModelPrice.model_id == AutoModel.model_id) \
        .with_entities(AutoModel.model_name, AutoBrand.brand_name, ModelPrice.price)

    models = models_q.all()
    return render_template("model_view.html", models=models)


@app.route('/view/autos')
def view_autos():
    autos_q = db \
        .query(Auto).join(AutoModel, Auto.model_id == AutoModel.model_id) \
        .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id) \
        .join(ModelPrice, ModelPrice.model_id == Auto.model_id) \
        .with_entities(AutoModel.model_name, AutoBrand.brand_name, Auto.registration_number, Auto.mileage, Auto.quality)
    autos = autos_q.all()
    return render_template("auto_view.html", autos=autos)
