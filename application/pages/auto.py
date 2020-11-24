from flask import request, jsonify

from app_context import app, db
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.status_of_auto import StatusOfAuto

_s = StatusOfAuto

a = app()


@a.route('/services/auto/autos', methods=['GET', 'POST', 'PUT'])
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
    elif request.method == "POST":
        post_data = request.get_json()

        auto = Auto(model_id=post_data.get('model_id'), registration_number=post_data.get('registration_number'),
                    mileage=post_data.get('mileage'), quality=post_data.get('quality'), status_id=0)
        db().execute_add(auto, True)
    elif request.method == 'PUT':
        data = request.get_json()
        db().execute_query(lambda d: d
                           .query(Auto)
                           .filter(Auto.registration_number == data.get('old_number'))
                           .update({'model_id': data.get('new_model_id'),
                                    'registration_number': data.get('new_number'),
                                    'mileage': data.get('mileage'),
                                    'quality': data.get('quality')}), True)

    return jsonify(response_object)


@a.route('/services/auto/autos/remove', methods=['POST'])
def service_auto_remove():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        number = request.get_json().get('number')
        db().execute_query(lambda d: d.query(Auto).filter(Auto.registration_number == number).delete(), True)
    return jsonify(response_object)
