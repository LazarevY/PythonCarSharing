from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP

from application.database.modeles.base import *


class RentContract(BaseModel):
    __tablename__ = 'rent_contracts'
    contract_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.client_id'))
    auto_id = Column(Integer, ForeignKey('autos.auto_id'))
    rent_begin_date = Column(TIMESTAMP(timezone=False), nullable=False)
    rent_end_date = Column(TIMESTAMP(timezone=False), nullable=True)
    rent_price = Column(Integer)
    actual_income = Column(Integer)
