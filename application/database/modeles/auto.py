from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey


class Auto(BaseModel):
    __tablename__ = 'autos'
    auto_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    status_id = Column(Integer, ForeignKey('status_of_auto.status_id'))
    current_office_id = Column(Integer, ForeignKey('branch_offices.office_id'))
    model_id = Column(Integer, ForeignKey('autos_models.model_id'))
    registration_number = Column(VARCHAR(20), unique=True, nullable=False)
    mileage = Column(Integer)
    quality = Column(Integer)
