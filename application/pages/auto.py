from datetime import datetime

from flask import request, jsonify
from sqlalchemy import and_

from app_context import app, db
from application.database.database_utils import get_auto_status_id_by_name, get_auto_id
from application.database.modeles.RentContract import RentContract
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_in_office import AutoInOffice
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.branch_office import BranchOffice
from application.database.modeles.client import Client
from application.database.modeles.status_of_auto import StatusOfAuto

_s = StatusOfAuto

a = app()


@a.route('/services/auto/autos', methods=['POST', 'PUT'])
def service_auto():
    response_object = {'status': 'success'}
    if request.method == "POST":
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
        old_location = db().execute_query(lambda d: d
                                          .query(Auto)
                                          .filter(Auto.registration_number == data.get('new_number'))
                                          .with_entities(Auto.current_office_id)
                                          .one())
        if old_location.current_office_id != data['new_office_id']:
            date = datetime.now()
            db().execute_query(lambda d: d
                               .query(Auto)
                               .filter(Auto.registration_number == data['new_number'])
                               .update({'current_office_id': data['new_office_id']}),
                               True)
            auto_id = get_auto_id(data['new_number'])
            db().execute_query(lambda d: d
                               .query(AutoInOffice)
                               .filter(and_(AutoInOffice.auto_id == auto_id,
                                            AutoInOffice.departure_date == None))
                               .update({'departure_date': date}),
                               True)
            aio = AutoInOffice(auto_id=auto_id,
                               office_id=data['new_office_id'],
                               receipt_date=date)
            db().execute_add(aio, True)

    return jsonify(response_object)


@a.route('/services/auto/autos/get', methods=['POST'])
def service_autos_get_filtered():
    response_object = {'status': 'success'}
    if request.method == "POST":
        data = request.get_json()
        autos = db().execute_query(lambda d: d
                                   .query(Auto)
                                   .join(AutoModel, AutoModel.model_id == Auto.model_id)
                                   .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id)
                                   .join(BranchOffice, BranchOffice.office_id == Auto.current_office_id)
                                   .filter(AutoBrand.brand_id != None if data['brand'] is None else AutoBrand.brand_id == data['brand'])
                                   .filter(AutoModel.model_id != None if data['model'] is None else AutoModel.model_id == data['model'])
                                   .filter(Auto.registration_number != None if data['number'] is None else Auto.registration_number == data['number'])
                                   .order_by(AutoBrand.brand_name)
                                   .with_entities(AutoBrand.brand_name,
                                                  AutoModel.model_name,
                                                  Auto.registration_number,
                                                  Auto.mileage,
                                                  Auto.quality,
                                                  Auto.status_id,
                                                  BranchOffice.office_address,
                                                  BranchOffice.office_id).all())
        ats = [{
            'brand_name': auto.brand_name,
            'model_name': auto.model_name,
            'number': auto.registration_number,
            'mileage': auto.mileage,
            'available': True if auto.status_id == get_auto_status_id_by_name('available') else False,
            'current_office': auto.office_address,
            'current_office_id': auto.office_id,
            'quality': auto.quality
        } for auto in autos]
        response_object['autos'] = ats
    return jsonify(response_object)


@a.route('/services/auto/autos/remove', methods=['POST'])
def service_auto_remove():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        number = request.get_json().get('number')
        db().execute_query(lambda d: d.query(Auto).filter(Auto.registration_number == number).delete(), True)
    return jsonify(response_object)


@a.route('/services/auto/autos/location', methods=['POST', 'PUT'])
def service_auto_update_location():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        offices = db().execute_query(lambda d: d
                                     .query(BranchOffice)
                                     .all())
        response_object['locations'] = \
            [
                {
                    'office_label': f"{l.office_name}: {l.office_address}",
                    'office_id': l.office_id
                }
                for l in offices
            ]

    return jsonify(response_object)


@a.route('/services/auto/autos/history', methods=['POST'])
def service_auto_update_history():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        auto_id = get_auto_id(data['number'])
        history = db().execute_query(lambda d: d
                                     .query(RentContract)
                                     .filter(RentContract.auto_id == auto_id)
                                     .join(Client, RentContract.client_id == Client.client_id)
                                     .with_entities(Client.client_name,
                                                    Client.client_second_name,
                                                    RentContract.rent_begin_date,
                                                    RentContract.rent_end_date,
                                                    RentContract.mileage)
                                     .all())
        response_object['history'] = \
            [
                {
                    'client': f"{c.client_name} {c.client_second_name}",
                    'begin_date': str(c.rent_begin_date),
                    'end_date': str(c.rent_end_date),
                    'mileage': c.mileage
                }
                for c in history
            ]
    return jsonify(response_object)


@a.route('/services/auto/autos/filter', methods=['POST'])
def service_auto_load_filter_data():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()

        brands = db().execute_query(lambda d: d.query(AutoBrand).all())

        models = []
        if data['brand_id'] is not None:
            models = db().execute_query(lambda d: d
                                        .query(AutoModel)
                                        .filter(AutoModel.brand_id == data['brand_id'])
                                        .all())
        else:
            models = db().execute_query(lambda d: d
                                        .query(AutoModel)
                                        .all())

        numbers = []
        if data['model_id'] is not None:
            numbers = db().execute_query(lambda d: d
                                         .query(Auto)
                                         .filter(Auto.model_id == data['model_id'])
                                         .with_entities(Auto.registration_number)
                                         .all())
        else:
            numbers = db().execute_query(lambda d: d
                                         .query(Auto)
                                         .with_entities(Auto.registration_number)
                                         .all())

        response_object['brands'] = \
            [
                {
                    'brand_name': b.brand_name,
                    'brand_id': b.brand_id,
                }
                for b in brands
            ]
        response_object['models'] = \
            [
                {
                    'model_name': m.model_name,
                    'model_id': m.model_id,
                }
                for m in models
            ]
        response_object['numbers'] = \
            [
                {
                    'number': n.registration_number
                }
                for n in numbers
            ]
    return jsonify(response_object)
