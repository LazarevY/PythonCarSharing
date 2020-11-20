from flask import Flask
from flask_cors import CORS
from flask_wtf import CsrfProtect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.database.session.session import DBSession
import os
import config

_app = Flask("Car Sharing")
CORS(_app)
# csrf = CsrfProtect()
# SECRET_KEY = os.urandom(32)
# _app.config['SECRET_KEY'] = SECRET_KEY
# csrf.init_app(_app)


def app():
    return _app


dbschema = 'car_sharing_schema'
engine = create_engine(
    f'postgresql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}',
    pool_pre_ping=True,
    connect_args={'options': '-csearch_path={}'.format(dbschema)}
)
session_factory = sessionmaker(bind=engine)
db_session = DBSession(session_factory())


def db():
    return db_session
