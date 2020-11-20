from application.database.modeles.base import *
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TIMESTAMP


class AutoInOffice(BaseModel):
    __tablename__ = 'auto_in_office'
    note_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    auto_id = Column(Integer, ForeignKey('autos.auto_id'))
    office_id = Column(Integer, ForeignKey('branch_offices.office_id'))
    receipt_date = Column(TIMESTAMP, nullable=False)
    departure_date = Column(TIMESTAMP, nullable=True)
