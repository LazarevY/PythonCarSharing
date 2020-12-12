from flask import request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from app_context import app, db
from application.database.database_utils import get_client_id
from application.database.modeles.client import Client
from application.database.modeles.client_autorize import ClientLogin

a = app()


def check_client_property_unique_func(name, value):
    if name == 'phone':
        vals = db().execute_query(lambda d: d.query(Client).filter(Client.client_phone == value).all())
        return True if len(vals) == 0 else False
    elif name == 'passport':
        vals = db().execute_query(lambda d: d.query(Client).filter(Client.client_passport == str(value)).all())
        return True if len(vals) == 0 else False
    elif name == 'drive_license':
        vals = db().execute_query(lambda d: d.query(Client).filter(Client.client_drive_license == str(value)).all())
        return True if len(vals) == 0 else False
    else:
        return False


@a.route('/register/check_unique', methods=['GET'])
def check_client_property_unique():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        name = post_data['name']
        value = post_data['value']

        if name == 'phone':
            vals = db().execute_query(lambda d: d.query(Client).filter(Client.client_phone == value).all())
            response_object["result"] = True if len(vals) == 0 else False
        elif name == 'passport':
            vals = db().execute_query(lambda d: d.query(Client).filter(Client.client_passport == str(value)).all())
            response_object["result"] = True if len(vals) == 0 else False
        elif name == 'drive_license':
            vals = db().execute_query(lambda d: d.query(Client).filter(Client.client_drive_license == str(value)).all())
            response_object["result"] = True if len(vals) == 0 else False
        else:
            response_object["result"] = False
    return jsonify(response_object)


@a.route('/register', methods=['POST'])
def register_client():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()

        response_object['unique'] = {
            'phone': check_client_property_unique_func('phone', post_data['phone']),
            'passport': check_client_property_unique_func('passport', post_data['passport']),
            'drive_license': check_client_property_unique_func('drive_license', post_data['drive_license'])
        }

        if not response_object['unique']['phone'] \
                or not response_object['unique']['passport'] \
                or not response_object['unique']['drive_license']:
            print("not unique")
            response_object['status'] = "fail"
            return jsonify(response_object)

        client = Client(
            client_name=post_data['name'],
            client_second_name=post_data['lastName'],
            client_drive_license=str(post_data['drive_license']),
            client_phone=post_data['phone'],
            client_passport=str(post_data['passport'])
        )
        db().execute_add(client, True)
        client_id = get_client_id(post_data['phone'])
        if client_id is None:
            return jsonify(response_object)
        pass_hash = generate_password_hash(post_data['password'])
        client_login = ClientLogin(client_id=client_id, password_hash=pass_hash)
        db().execute_add(client_login, True)
        return response_object


@a.route('/login', methods=['POST'])
def client_log_in():
    response_object = {'status': 'success',
                       'logined': True}
    if request.method == 'POST':
        post_data = request.get_json()
        client_id = get_client_id(post_data['phone'])
        if client_id is None:
            response_object['logined'] = False
            response_object['message'] = 'Phone is not registered'
            return jsonify(response_object)

        login_data = db().execute_query(lambda d: d.query(ClientLogin).filter(ClientLogin.client_id == client_id).one())
        if check_password_hash(login_data.password_hash, post_data['password']):
            response_object['status'] = 'success'
            response_object['logined'] = True
            client_data = db().execute_query(lambda d: d.query(Client).filter(Client.client_id == client_id).one())
            response_object['userdata'] = {
                'name': client_data.client_phone,
                'lastName': client_data.client_second_name,
            }
            access_token = create_access_token(identity=client_data.client_phone)
            response_object['token'] = access_token
        else:
            response_object['logined'] = False
            response_object['message'] = 'Wrong password'

    return jsonify(response_object)
