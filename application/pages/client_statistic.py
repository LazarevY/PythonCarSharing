from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from sqlalchemy import and_, desc, func

from app_context import app, db
from application.database.database_utils import get_client_id, get_auto_id, get_auto_status_id_by_name, \
    get_rent_status_id_by_name
from application.database.modeles.RentContract import RentContract
from application.database.modeles.RentHistory import RentHistory
from application.database.modeles.RentStatus import RentStatus
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_in_office import AutoInOffice
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.branch_office import BranchOffice
from application.database.modeles.violation import Violation

a = app()


@a.route('/main/client/statistic', methods=['GET'])
@jwt_required
def client_statistic_load():
    response_object = {'status': 'success', 'logined': True}
    userphone = get_jwt_identity()
    client_id = get_client_id(userphone)
    if request.method == 'GET':
        rents = func.count(RentContract.contract_id)
        top = db().execute_query(lambda d: d
                                 .query(Auto)
                                 .join(RentContract, and_(RentContract.auto_id == Auto.auto_id,
                                                          RentContract.client_id == client_id))
                                 .join(AutoModel, AutoModel.model_id == Auto.model_id)
                                 .join(AutoBrand, AutoModel.brand_id == AutoBrand.brand_id)
                                 .with_entities(AutoBrand.brand_name, AutoModel.model_name, rents)
                                 .group_by(AutoBrand.brand_name, AutoModel.model_name)
                                 .limit(3)
                                 .all())
        response_object['top_models'] = \
            [
                {
                    'brand_name': t.brand_name,
                    'model_name': t.model_name,
                    'rents': t[2]
                }
                for t in top
            ]

        primary = db().execute_query(lambda d: d
                                     .query(Auto)
                                     .join(RentContract, and_(RentContract.auto_id == Auto.auto_id,
                                                              RentContract.client_id == client_id))
                                     .join(AutoModel, AutoModel.model_id == Auto.model_id)
                                     .join(AutoBrand, AutoModel.brand_id == AutoBrand.brand_id)
                                     .with_entities(AutoBrand.brand_name, AutoModel.model_name, rents)
                                     .group_by(AutoBrand.brand_name, AutoModel.model_name)
                                     .order_by(desc(rents))
                                     .limit(1)
                                     .one())
        all_rents = db().execute_query(lambda d: d
                                       .query(Auto)
                                       .join(RentContract, and_(RentContract.auto_id == Auto.auto_id,
                                                                RentContract.client_id == client_id))
                                       .with_entities(rents)
                                       .one())

        violates = func.count(Violation.violation_id)
        violates_count = db().execute_query(lambda d: d
                                            .query(Violation)
                                            .join(RentContract,
                                                  and_(RentContract.contract_id == Violation.contract_id,
                                                       RentContract.client_id == client_id))
                                            .with_entities(violates)
                                            .one())
        response_object['violates'] = {
            'count': violates_count[0]
        }

        response_object['rents'] = {
            'primary_brand': primary.brand_name,
            'primary_model': primary.model_name,
            'count': all_rents[0]
        }

        rents_data = db().execute_query(lambda d: d
                                        .query(RentContract)
                                        .join(Auto, Auto.auto_id == RentContract.auto_id)
                                        .join(AutoModel, AutoModel.model_id == Auto.model_id)
                                        .join(AutoBrand, AutoBrand.brand_id == AutoModel.brand_id)
                                        .filter(RentContract.client_id == client_id)
                                        .with_entities(RentContract.contract_id,
                                                       AutoBrand.brand_name,
                                                       AutoModel.model_name,
                                                       Auto.registration_number,
                                                       RentContract.rent_begin_date,
                                                       RentContract.rent_end_date)
                                        .order_by(RentContract.rent_begin_date)
                                        .all())

        response_object['rents_data'] = \
            [
                {
                    'contract_id': t.contract_id,
                    'brand_name': t.brand_name,
                    'model_name': t.model_name,
                    'number': t.registration_number,
                    'rent_begin_date': str(t.rent_begin_date),
                    'rent_end_date': str(t.rent_end_date)
                }
                for t in rents_data
            ]

    return jsonify(response_object)
