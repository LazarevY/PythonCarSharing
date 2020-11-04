#from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.database.session.session import DBSession
from application.database.modeles.auto_brand import AutoBrand

import config

#app = Flask(__name__)


# @app.route('/')
# def hello_world():
#     return 'Hello World!'


if __name__ == '__main__':
    dbschema = 'car_sharing_schema'
    engine = create_engine(
        f'postgresql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}:{config.DATABASE_PORT}/{config.DATABASE_NAME}',
        pool_pre_ping=True,
        connect_args={'options': '-csearch_path={}'.format(dbschema)}
    )
    session_factory = sessionmaker(bind=engine)
    db_session = DBSession(session_factory())

    brands = db_session.query(AutoBrand).all()

    for brand in brands:
        print(brand)
