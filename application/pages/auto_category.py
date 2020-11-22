from flask import Flask, jsonify, request

from app_context import app, db
from application.database.modeles.auto_brand import AutoBrand
from application.database.modeles.drive_category import DriveCategory

a = app()


@a.route('/services/auto/categories', methods=['GET'])
def service_auto_category():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        categories = db().execute_query(lambda d:
                                        d.query(DriveCategory).all())
        if categories is None:
            response_object['status'] = 'fail'
            return jsonify(response_object)
        cts = [{'name': category.category_name} for category in categories]
        response_object['categories'] = cts

    return response_object
