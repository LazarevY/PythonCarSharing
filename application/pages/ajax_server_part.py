from flask import request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from app_context import app, db
from application.database.modeles.auto import Auto
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.model_price import ModelPrice

appl = app()


@appl.route('/model_for_brand', methods=['POST'])
def get_models_for_brand():
    brand_id = int(request.form['brand_id'])
    models_q = db() \
        .query(AutoModel) \
        .filter(AutoModel.brand_id == brand_id) \
        .with_entities(AutoModel.model_id, AutoModel.model_name)

    models = models_q.all()

    models_dict = dict()
    for m in models:
        models_dict[int(m.model_id)] = m.model_name

    return jsonify(models_dict)


@appl.route('/model_data', methods=['POST'])
def get_model_data():
    model_id = int(request.form['model_id'])
    model_q = db() \
        .query(AutoModel) \
        .filter(AutoModel.model_id == model_id) \
        .with_entities(AutoModel.model_id, AutoModel.brand_id, AutoModel.model_name)
    model = model_q.one()
    price_q = db().query(ModelPrice).filter(ModelPrice.model_id == model_id)
    price = 0
    try:
        price = int(price_q.one().price)
    except SQLAlchemyError:
        price = 0

    d = {
        "model_id": model.model_id,
        "model_brand": model.brand_id,
        "model_name": model.model_name,
        "model_price": price
    }
    return jsonify(d)


@appl.route('/auto_for_model', methods=['POST'])
def get_autos_for_model():
    model_id = int(request.form['model_id'])
    autos_q = db().query(Auto).filter(Auto.model_id == model_id)
    autos = autos_q.all()

    d = dict()

    for a in autos:
        d[a.auto_id] = a.registration_number
    return jsonify(d)


@appl.route('/auto_data', methods=['POST'])
def get_auto_data():
    id = request.form['auto_id']
    auto_q = db().query(Auto).filter(Auto.auto_id == id).one()
    return jsonify({
        "number": auto_q.registration_number,
        "mileage": auto_q.mileage,
        "quality": auto_q.quality
    })
