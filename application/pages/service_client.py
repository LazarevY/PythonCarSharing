from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from sqlalchemy import and_, desc, func

from app_context import app, db
from application.database.database_utils import get_client_id, get_auto_id, get_auto_status_id_by_name, \
    get_rent_status_id_by_name, get_category_id
from application.database.modeles.RentContract import RentContract
from application.database.modeles.RentHistory import RentHistory
from application.database.modeles.RentStatus import RentStatus
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_in_office import AutoInOffice
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.branch_office import BranchOffice
from application.database.modeles.client import Client
from application.database.modeles.client_category import ClientCategory
from application.database.modeles.drive_category import DriveCategory
from application.database.modeles.violation import Violation
from application.database.modeles.violation_type import ViolationType

a = app()


@a.route('/services/client', methods=['GET'])
def service_client_load_data():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        clients = db().execute_query(lambda d: d
                                     .query(Client)
                                     .with_entities(Client.client_phone)
                                     .all())
        response_object['clients'] = \
            [
                {
                    'phone': t.client_phone
                }
                for t in clients
            ]
    return jsonify(response_object)


@a.route('/services/client', methods=['POST'])
def service_client_load_client_data():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()

        client = db().execute_query(lambda d: d
                                    .query(Client)
                                    .filter(Client.client_phone == data['phone'])
                                    .one())
        all_categories = db().execute_query(lambda d: d
                                            .query(DriveCategory)
                                            .with_entities(DriveCategory.category_name)
                                            .all())
        client_categories = db().execute_query(lambda d: d
                                               .query(ClientCategory)
                                               .join(DriveCategory,
                                                     DriveCategory.category_id == ClientCategory.category_id)
                                               .filter(ClientCategory.client_id == client.client_id)
                                               .with_entities(DriveCategory.category_name)
                                               .all())
        client_categories_set = {ac.category_name for ac in client_categories}
        response_object['client_data'] = \
            {
                'name': client.client_name,
                'lastName': client.client_second_name,
                'phone': client.client_phone,
                'license': client.client_drive_license,
                'categories':
                    {
                        c.category_name: True if c.category_name in client_categories_set
                        else False for c in all_categories
                    }

            }
    return jsonify(response_object)


@a.route('/services/client/categories', methods=['POST'])
def service_client_update_categories():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        client_id = get_client_id(data['phone'])

        db().execute_query(lambda d: d
                           .query(ClientCategory)
                           .filter(ClientCategory.client_id == client_id)
                           .delete())

        for name, have in data['categories'].items():
            if have:
                category = ClientCategory(client_id=client_id, category_id=get_category_id(name))
                db().execute_add(category)
        db().commit_session()
    return jsonify(response_object)


@a.route('/services/client/violations', methods=['POST'])
def service_client_load_violation_data():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()

        violations = db().execute_query(lambda d: d
                                        .query(ViolationType)
                                        .all())
        contract_dates = db().execute_query(lambda d: d
                                            .query(RentContract)
                                            .join(Client, and_(Client.client_id == RentContract.client_id,
                                                               Client.client_phone == data['client_phone']))
                                            .with_entities(RentContract.contract_id, RentContract.rent_begin_date)
                                            .all())
        response_object['violations'] = \
            [
                {
                    'violation_id': v.violation_id,
                    'violation_type': v.violation_type,
                    'violation_desc': v.desc
                }
                for v in violations
            ]

        response_object['contracts'] = \
            [
                {
                    'contract_id': r.contract_id,
                    'contract_date': r.rent_begin_date,
                }
                for r in contract_dates
            ]

    return jsonify(response_object)


@a.route('/services/client/violations/add', methods=['POST'])
def service_client_add_violation():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        data = request.get_json()
        violation = Violation(contract_id=data['contract_id'],
                              violation_id=data['violation_id'],
                              fine=data['price'],
                              note=data['note'])
        db().execute_add(violation, True)
    return jsonify(response_object)
