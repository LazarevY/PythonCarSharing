from flask import request, jsonify

from app_context import app, db
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel

a = app()


@a.route('/services/auto/autos', methods=['GET'])
def service_auto():
    response_object = {'status': 'success'}
    if request.method == "GET":
        autos = db().execute_query(lambda d: d
                                   .query(Auto)
                                   .join(AutoModel, AutoModel.model_id == Auto.model_id)
                                   .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id)
                                   .with_entities(AutoBrand.brand_name, AutoModel.model_name,
                                                  Auto.registration_number, Auto.mileage, Auto.quality).all())
        ats = [{
            'brand_name': auto.brand_name,
            'model_name': auto.model_name,
            'number': auto.registration_number,
            'mileage': auto.mileage,
            'quality': auto.quality
        } for auto in autos]
        response_object['autos'] = ats
    return jsonify(response_object)
