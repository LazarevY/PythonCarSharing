import html

import flask
from flask import jsonify
from application.pages.front import *

import app_context

flask_app = app_context.app()


@flask_app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


if __name__ == '__main__':
    flask_app.run()
