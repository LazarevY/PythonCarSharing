from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from sqlalchemy import and_, desc

from app_context import app, db
from application.database.database_utils import get_client_id, get_auto_id, get_auto_status_id_by_name, \
    get_rent_status_id_by_name
from application.database.modeles.AutoTrack import AutoTrack
from application.database.modeles.RentContract import RentContract
from application.database.modeles.RentHistory import RentHistory
from application.database.modeles.RentStatus import RentStatus
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_in_office import AutoInOffice
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.branch_office import BranchOffice

a = app()


@a.route('/main', methods=['GET'])
@jwt_required
def client_main_load():
    response_object = {'status': 'success', 'logined': True}
    userphone = get_jwt_identity()
    response_object['userdata'] = {'name': userphone, 'phone': userphone}

    points = db().execute_query(lambda d: d
                                .query(BranchOffice)
                                .with_entities(BranchOffice.office_id, BranchOffice.office_address)
                                .all())

    client_id = get_client_id(userphone)

    active_contracts = db().execute_query(lambda d: d
                                          .query(RentHistory)
                                          .join(RentContract, RentHistory.contract_id == RentContract.contract_id)
                                          .join(RentStatus, RentHistory.status_id == RentStatus.status_id)
                                          .filter(and_(RentContract.client_id == client_id,
                                                       RentStatus.status_name == 'in_force'))
                                          .all())

    response_object['isActiveContract'] = True if len(active_contracts) > 0 else False

    response_object['points'] = [{'code': p.office_id, 'label': p.office_address} for p in points]

    return jsonify(response_object)


@a.route('/main/autos_for_point', methods=['POST'])
@jwt_required
def client_autos_for_point_load():
    response_object = {'status': 'success', 'logined': True}
    data = request.get_json()

    autos = db().execute_query(lambda d: d
                               .query(Auto)
                               .filter(Auto.status_id == 0)
                               .join(AutoInOffice,
                                     and_(
                                         AutoInOffice.auto_id == Auto.auto_id,
                                         AutoInOffice.office_id ==
                                         data['point_id'],
                                         AutoInOffice.departure_date == None))
                               .join(AutoModel, AutoModel.model_id == Auto.model_id)
                               .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id)
                               .with_entities(
        AutoBrand.brand_name,
        AutoModel.model_name,
        Auto.registration_number,
        Auto.mileage)
                               .all()
                               )
    response_object['autos'] = [{
        'brand_name': auto.brand_name,
        'model_name': auto.model_name,
        'mileage': auto.mileage,
        'number': auto.registration_number
    } for auto in autos]

    return jsonify(response_object)


@a.route('/main/rent/create', methods=['POST'])
@jwt_required
def create_rent():
    response_object = {'status': 'success', 'logined': True}
    userphone = get_jwt_identity()
    response_object['userdata'] = {'name': userphone, 'phone': userphone}
    data = request.get_json()
    client_id = get_client_id(data['phone'])
    auto_id = get_auto_id(data['auto_number'])
    date = datetime.now()
    contract = RentContract(client_id=client_id, auto_id=auto_id, rent_begin_date=date, rent_price=1)

    db().execute_add(contract, True)

    contract_data = db().execute_query(lambda d: d
                                     .query(RentContract)
                                     .filter(RentContract.client_id == client_id)
                                     .order_by(desc(RentContract.rent_begin_date))
                                     .limit(1)
                                     .with_entities(RentContract.contract_id, RentContract.client_id)
                                     .one())
    db().execute_query(lambda d: d.query(Auto).filter(Auto.auto_id == auto_id).update(
        {'status_id': get_auto_status_id_by_name('free_wait')}), True)
    rent_note = RentHistory(contract_id=contract_data.contract_id,
                            status_id=get_rent_status_id_by_name('in_force'),
                            note='',
                            note_date=date)
    db().execute_add(rent_note, True)
    return jsonify(response_object)
