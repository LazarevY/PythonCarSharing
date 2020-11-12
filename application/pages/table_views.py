from flask import render_template

import app_context as a
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
