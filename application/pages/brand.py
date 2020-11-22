from flask import Flask, jsonify, request

from app_context import app, db
from application.database.modeles.auto_brand import AutoBrand

a = app()


@a.route('/services/auto/brands', methods=['GET', 'POST', 'PUT'])
def service_brand():
    response_object = {'status': 'success'}

    if request.method == 'POST':
        post_data = request.get_json()
        brand = AutoBrand(brand_name=post_data.get('brand_name'))
        db().add_entity_object(brand)
        db().commit_session()
    elif request.method == 'PUT':
        post_data = request.get_json()
        old = post_data.get('old_name')
        new_name = post_data.get('new_name')
        db().query(AutoBrand).filter(AutoBrand.brand_name == old).update({'brand_name': new_name})
        db().commit_session()
    else:
        brands_q = db().query(AutoBrand)
        brands = [{'name': brand.brand_name} for brand in brands_q.all()]
        response_object['brands'] = brands
    return jsonify(response_object)


@a.route('/services/auto/brands/remove', methods=['POST'])
def service_brand_remove():
    if request.method == 'POST':
        brand_name = request.get_json().get('brand_name')
        db().query(AutoBrand).filter(AutoBrand.brand_name == brand_name).delete()
        db().commit_session()
    return jsonify({
        'status': 'success'
    })
