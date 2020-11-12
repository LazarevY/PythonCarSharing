from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class Client(BaseModel):
    __tablename__ = 'clients'
    client_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    client_name = Column(VARCHAR(60))
    client_second_name = Column(VARCHAR(60))
    client_father_name = Column(VARCHAR(60), nullable=True)
    client_passport = Column(VARCHAR(200), unique=True)
    client_drive_license = Column(VARCHAR(200), unique=True)
