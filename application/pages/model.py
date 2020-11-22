from flask import jsonify, request
from sqlalchemy import and_

from app_context import app, db
from application.database.database_utils import get_brand_id, get_category_id, get_model_id
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.auto_model import AutoModel
from application.database.modeles.drive_category import DriveCategory
from application.database.modeles.model_price import ModelPrice

a = app()


@a.route('/services/auto/models', methods=['GET', 'POST', 'PUT'])
def service_model():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()

        brand_id = db().execute_query(lambda db: db
                                      .query(AutoBrand)
                                      .filter(AutoBrand.brand_name == post_data.get('brand_name'))
                                      .with_entities(AutoBrand.brand_id)
                                      .one()
                                      )
        category_id = db().execute_query(lambda db: db
                                         .query(DriveCategory)
                                         .filter(DriveCategory.category_name == post_data.get('category_name'))
                                         .with_entities(DriveCategory.category_id)
                                         .one())
        if brand_id is None or category_id is None:
            response_object['status'] = 'fail'
            return response_object

        model = AutoModel(brand_id=brand_id, model_name=post_data.get('model_name'), category_id=category_id)

        if not db().execute_add(model, True):
            response_object['status'] = 'fail'
            return response_object

        model_id = db().execute_query(lambda db: db
                                      .query(AutoModel)
                                      .filter(AutoModel.model_name == model.model_name, AutoModel.brand_id == brand_id)
                                      .with_entities(AutoModel.model_id).one()
                                      )
        model_price = ModelPrice(model_id=model_id, price=post_data.get('price'))
        db().execute_add(model_price, True)

    elif request.method == 'PUT':
        post_data = request.get_json()

        brand_id = get_brand_id(post_data.get('old_brand_name'))
        category_id = get_category_id(post_data.get('new_category_name'))
        new_brand_id = get_brand_id(post_data.get('new_brand_name'))

        if brand_id is None or category_id is None:
            response_object['status'] = 'fail'
            return response_object

        db().execute_query(lambda d: d
                           .query(AutoModel)
                           .filter(and_(
            AutoModel.model_name == post_data.get('old_model_name'),
            AutoModel.brand_id == brand_id))
                           .update({
            'model_name': post_data.get('new_model_name'),
            'brand_id': new_brand_id,
            'category_id': category_id
        }), True)

        model_id = get_model_id(post_data.get('new_brand_name'), post_data.get('new_model_name'))

        db().execute_query(lambda d: d.query(ModelPrice).filter(ModelPrice.model_id == model_id).update(
            {'price': post_data.get('price')}), True)

    elif request.method == 'GET':
        models_q = db().execute_query(lambda db: db
                                      .query(AutoModel)
                                      .join(AutoBrand, AutoModel.brand_id == AutoBrand.brand_id)
                                      .join(ModelPrice, ModelPrice.model_id == AutoModel.model_id)
                                      .join(DriveCategory, DriveCategory.category_id == AutoModel.category_id)
                                      .with_entities(AutoBrand.brand_name, AutoModel.model_name,
                                                     ModelPrice.price, DriveCategory.category_name))
        if models_q is None:
            response_object['status'] = 'fail'
            return jsonify(response_object)
        models = [{
            'model_name': model.model_name,
            'brand_name': model.brand_name,
            'category_name': model.category_name,
            'price': int(model.price)
        } for model in models_q.all()]
        response_object['models'] = models
    return jsonify(response_object)


@a.route('/services/auto/models/remove', methods=['POST'])
def service_model_remove():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        brand_id = get_brand_id(post_data.get('brand_name'))
        if brand_id is None:
            response_object['status'] = 'fail'
            return response_object
        db().execute_query(lambda d: d
                           .query(AutoModel)
                           .filter(AutoModel.brand_id == brand_id, AutoModel.model_name == post_data.get('model_name'))
                           .delete(),
                           True)
    return response_object
