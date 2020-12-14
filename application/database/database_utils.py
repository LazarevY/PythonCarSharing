from app_context import db
from application.database.modeles.status_of_auto import StatusOfAuto
from application.database.modeles.RentStatus import RentStatus
from application.database.modeles.auto import Auto
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.client import Client
from application.database.modeles.drive_category import DriveCategory
from application.database.modeles.violation_type import ViolationType

rent_statuses = {
    r.status_name: r.status_id for r in db().execute_query(lambda d: d
                                                           .query(RentStatus)
                                                           .with_entities(RentStatus.status_id, RentStatus.status_name)
                                                           .all())
}

auto_statuses = {
    r.status_name: r.status_id for r in db().execute_query(lambda d: d
                                                           .query(StatusOfAuto)
                                                           .with_entities(StatusOfAuto.status_id,
                                                                          StatusOfAuto.status_name)
                                                           .all())
}

violation_types = {
    r.violation_type: r.violation_id for r in db().execute_query(lambda d: d
                                                                 .query(StatusOfAuto)
                                                                 .with_entities(ViolationType.violation_id,
                                                                                ViolationType.violation_type)
                                                                 .all())
}


def get_brand_id(brand_name: str) -> int:
    brand_id = db().execute_query(lambda d: d
                                  .query(AutoBrand)
                                  .filter(AutoBrand.brand_name == brand_name)
                                  .with_entities(AutoBrand.brand_id)
                                  .one())
    return None if brand_id is None else brand_id


def get_model_id(brand_name: str, model_name: str) -> int:
    model_id = db().execute_query(lambda d: d
                                  .query(AutoModel)
                                  .join(AutoBrand, AutoModel.brand_id == AutoModel.brand_id)
                                  .filter(AutoBrand.brand_name == brand_name, AutoModel.model_name == model_name)
                                  .with_entities(AutoModel.model_id)
                                  .one())
    return None if model_id is None else model_id


def get_category_id(category_name: str) -> int:
    category_id = db().execute_query(lambda d: d
                                     .query(DriveCategory)
                                     .filter(DriveCategory.category_name == category_name)
                                     .with_entities(DriveCategory.category_id)
                                     .one())
    return None if category_id is None else category_id


def get_auto_id(number):
    auto_id = db().execute_query(lambda d: d
                                 .query(Auto)
                                 .filter(Auto.registration_number == number)
                                 .with_entities(Auto.auto_id)
                                 .one())
    return auto_id


def get_client_id(phone_number: int) -> int:
    client_id = db().execute_query(lambda d: d
                                   .query(Client)
                                   .filter(Client.client_phone == phone_number)
                                   .with_entities(Client.client_id)
                                   .one())
    return None if client_id is None else client_id


def get_rent_status_id_by_name(name):
    return rent_statuses[name]


def get_auto_status_id_by_name(name):
    return auto_statuses[name]


def get_violation_id(name):
    return violation_types[name]
