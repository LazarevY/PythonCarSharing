from datetime import datetime, timedelta

from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from sqlalchemy import and_, desc

from app_context import app, db
from application.database.database_utils import get_client_id, get_auto_id, get_auto_status_id_by_name, \
    get_rent_status_id_by_name, get_violation_id
from application.database.modeles.AutoTrack import AutoTrack
from application.database.modeles.RentContract import RentContract
from application.database.modeles.RentHistory import RentHistory
from application.database.modeles.RentStatus import RentStatus
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_in_office import AutoInOffice
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.branch_office import BranchOffice
from application.database.modeles.model_price import ModelPrice
from application.database.modeles.status_of_auto import StatusOfAuto
from application.database.modeles.violation import Violation

a = app()


@a.route('/main/rent/track', methods=['POST'])
@jwt_required
def rent_add_track_info():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        track = AutoTrack(contract_id=data['contract_id'],
                          state_id=get_auto_status_id_by_name(data['status_name']),
                          duration=data['duration'])
        db().execute_add(track, True)
    return jsonify(response_object)


@a.route('/main/rent/track', methods=['GET'])
@jwt_required
def rent_load_data():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        response_object['states'] = \
            [
                {
                    'state_id': get_auto_status_id_by_name('wait'),
                    'state_name': 'wait'
                },
                {
                    'state_id': get_auto_status_id_by_name('active'),
                    'state_name': 'active'
                }
            ]
    return jsonify(response_object)


@a.route('/main/rent/track/history', methods=['POST'])
@jwt_required
def track_history():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        response_object['history'] = get_track_history(data['contract_id'])
    return jsonify(response_object)


def get_track_history(contract_id):
    return [
        {
            'duration': t.duration,
            'state_name': t.status_name
        }

        for t in db().execute_query(lambda d: d
                                    .query(AutoTrack)
                                    .join(StatusOfAuto, StatusOfAuto.status_id == AutoTrack.state_id)
                                    .filter(AutoTrack.contract_id == contract_id)
                                    .with_entities(StatusOfAuto.status_name, AutoTrack.duration)
                                    .all())
    ]


@a.route('/main/rent/end', methods=['POST'])
@jwt_required
def end_client_rent():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        hist = get_track_history(data['contract_id'])
        rent_minutes = sum(t['duration'] for t in hist)

        model_price = db().execute_query(lambda d: d
                                         .query(RentContract)
                                         .filter(RentContract.contract_id == data['contract_id'])
                                         .join(Auto, Auto.auto_id == RentContract.auto_id)
                                         .join(AutoModel, AutoModel.model_id == Auto.model_id)
                                         .join(ModelPrice, ModelPrice.model_id == AutoModel.model_id)
                                         .with_entities(ModelPrice.price)
                                         .one())

        rent_price = model_price.price * sum(t['duration']
                                             for t in filter(lambda item: item['state_name'] == 'active', hist))
        contract_data = db().execute_query(lambda d: d
                                           .query(RentContract)
                                           .filter(RentContract.contract_id == data['contract_id'])
                                           .one())
        end_data = contract_data.rent_begin_date + timedelta(minutes=rent_minutes)
        db().execute_query(lambda d: d
                           .query(RentContract)
                           .filter(RentContract.contract_id == data['contract_id'])
                           .update({'rent_end_date': end_data,
                                    'rent_status_id': get_rent_status_id_by_name('completed_successfully'),
                                    'rent_price': rent_price,
                                    'mileage': data['mileage']})
                           , True)

        db().execute_query(lambda d: d
                           .query(Auto)
                           .filter(Auto.auto_id == contract_data.auto_id)
                           .update({'status_id': get_auto_status_id_by_name('available')}),
                           True)
        auto_id = db().execute_query(lambda d: d
                                     .query(RentContract)
                                     .filter(RentContract.contract_id == data['contract_id'])
                                     .with_entities(RentContract.auto_id)
                                     .one())
        office = db().execute_query(lambda d: d
                                    .query(BranchOffice)
                                    .filter(BranchOffice.office_address == data['address'])
                                    .with_entities(BranchOffice.office_id)
                                    .one())

        aio = AutoInOffice(auto_id=auto_id.auto_id, receipt_date=end_data, office_id=office.office_id)
        db().execute_add(aio, True)

        auto_mileage = db().execute_query(lambda d: d
                                          .query(Auto)
                                          .filter(Auto.auto_id == auto_id)
                                          .with_entities(Auto.mileage)
                                          .one())
        db().execute_query(lambda d: d
                           .query(Auto)
                           .filter(Auto.auto_id == auto_id)
                           .update({'mileage': auto_mileage.mileage + int(data['mileage'])}),
                           True)
        overlimit = int(data['mileage']) - 100
        if overlimit > 0:
            viol = Violation(contract_id=data['contract_id'],
                             violation_id=get_violation_id('mileage_limit'),
                             note=f"Upper limit - {overlimit} km")
            db().execute_add(viol, True)

    return jsonify(response_object)
