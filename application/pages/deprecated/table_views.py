from flask import render_template

import app_context as a
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_in_office import AutoInOffice
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.branch_office import BranchOffice
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
    autos_q = db\
        .query(AutoInOffice)\
        .filter(AutoInOffice.departure_date == None)\
        .join(Auto, AutoInOffice.auto_id == Auto.auto_id)\
        .join(BranchOffice, AutoInOffice.office_id == BranchOffice.office_id)\
        .with_entities(Auto.registration_number, AutoInOffice.receipt_date, BranchOffice.office_name, BranchOffice.office_address)

    autos = autos_q.all()
    return render_template("auto_view.html", autos=autos)
