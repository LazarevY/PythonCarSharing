from app_context import db
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.drive_category import DriveCategory


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
